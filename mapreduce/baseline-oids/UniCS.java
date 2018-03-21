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



public class UniCS {

    // works on output of NT2CS <s [p1, ..., pn]
    public static class myMapper extends Mapper<Object, Text, Text, Text> {
        
        private Text subject    = new Text();
        private Text predicates = new Text();

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] data = value.toString().split("\t");
            subject.set(data[0]);
            predicates.set(data[1]);
            context.write(predicates, subject);
        }
    }



    public static class myReducer extends Reducer<Text, Text, Text, Text> {

        private Text subjects = new Text();
        private TreeSet<String> set;

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            set = new TreeSet<String>();
            for (Text val : values) { set.add(val.toString()); }
            subjects.set(set.toString());
            // write [p1, ..., pn] \t [s1, ..., sn]
            context.write(key, subjects);
        }
    }



    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: UniCS <in> <out>");
            System.exit(2);
        }
        Job job = new Job(conf, "UniCS");
        job.setJarByClass(UniCS.class);

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
