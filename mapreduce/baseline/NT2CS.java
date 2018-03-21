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

        private Triple tri = new Triple();
        private Text sub = new Text(); // key
        private Text pre = new Text(); // value

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            tri.setLine(value.toString());
            sub.set(tri.getSub());
            pre.set(tri.getPre());
            context.write(sub, pre);
        }
    }


    public static class myReducer extends Reducer<Text, Text, Text, Text> {

        private Text predicates = new Text(); //value
        private TreeSet<String> set;

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            set = new TreeSet<String>();
            for (Text val : values) { set.add(val.toString()); }
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

        job.setReducerClass(myReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
