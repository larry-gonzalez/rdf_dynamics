import java.util.TreeSet;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;



public class NT2CS {



    public static class myMapper extends Mapper<Object, Text, Text, Text> {

        private Text sub = new Text(); // key
        private Text pre = new Text(); //value

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            String[] spo = value.toString().split(" ");
            sub.set(spo[0]);
            pre.set(spo[1]);
            context.write(sub, pre);
        }
    }



    public static class myCombinerReducer extends Reducer<Text, Text, Text, Text> {

        private Text predicates = new Text(); //key
        private TreeSet<String> set;

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            set = new TreeSet<String>();
            for (Text val : values) {
                String[] aux = val.toString().split(";");
                for (String s: aux) { set.add(s); }
            }

            String aux2[] = set.toArray(new String[set.size()]);
            String buff = String.join(";", aux2);
            predicates.set(buff);
            //write s \t p1;...;pn
            context.write(key, predicates);
        }
    }



    public static class mySecondCombiner extends Reducer<Text, Text, Text, Text> {

        private Text predicates = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            String buff = "";
            for (Text val : values) {
                buff += ";" + val.toString();
            }
            if (buff.length() > 0) {
                buff = buff.substring(1,buff.length());
            }

            predicates.set(buff);
            //write s \t p1;...;pn
            context.write(key, predicates);
        }
    }



    public static class mySecondReducer extends Reducer<Text, Text, Text, Text> {

        private Text predicates = new Text();
        private TreeSet<String> set;

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            set = new TreeSet<String>();
            for (Text val : values) {
                String[] aux = val.toString().split(";");
                for (String s: aux) { set.add(s); }
            }
            predicates.set(set.toString());
            //write s \t [p1, ..., pn]
            context.write(key, predicates);
        }
    }



    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: NT2CS <in> <out>");
            System.exit(2);
        }
        Job job = new Job(conf, "NT2CS");
        job.setJarByClass(NT2CS.class);

        job.setMapperClass(myMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

	//myCombinerReducer was faster
        job.setCombinerClass(myCombinerReducer.class);
        job.setReducerClass(myCombinerReducer.class);
        //job.setCombinerClass(mySecondCombiner.class);
        //job.setReducerClass(mySecondReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }



}

