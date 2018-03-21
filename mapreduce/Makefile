HD=/opt/hadoop
JN=/opt/jena/lib
JARS=$(JN)/collection-0.6.jar,$(JN)/jackson-core-2.7.4.jar,$(JN)/jena-tdb-3.2.0.jar,$(JN)/commons-cli-1.3.jar,$(JN)/jackson-databind-2.7.4.jar,$(JN)/jsonld-java-0.9.0.jar,$(JN)/commons-codec-1.10.jar,$(JN)/jcl-over-slf4j-1.7.21.jar,$(JN)/libthrift-0.9.3.jar,$(JN)/commons-csv-1.3.jar,$(JN)/jena-arq-3.2.0.jar,$(JN)/log4j-1.2.17.jar,$(JN)/commons-io-2.5.jar,$(JN)/jena-base-3.2.0.jar,$(JN)/slf4j-api-1.7.21.jar,$(JN)/commons-lang3-3.4.jar,$(JN)/jena-cmds-3.2.0.jar,$(JN)/slf4j-log4j12-1.7.21.jar,$(JN)/httpclient-4.5.2.jar,$(JN)/jena-core-3.2.0.jar,$(JN)/xercesImpl-2.11.0.jar,$(JN)/httpclient-cache-4.5.2.jar,$(JN)/jena-iri-3.2.0.jar,$(JN)/xml-apis-1.4.01.jar,$(JN)/httpcore-4.4.4.jar,$(JN)/jena-rdfconnection-3.2.0.jar,$(JN)/jackson-annotations-2.7.0.jar,$(JN)/jena-shaded-guava-3.2.0.jar

#This is an example of how upload data to HDFS and run mapreduce tasks

example:
	$(HD)/bin/hdfs dfs -put wikidata-20170418-truthy-BETA.nt.bz2 /20170418
	$(HD)/bin/hadoop jar nt2cs.jar NT2CS -libjars $(JARS) \
              -D mapreduce.job.reduces=1 \
              /20170418/wikidata-20170418-truthy-BETA.nt.bz2 \
              $(P)/20170418/cs \
              > 20170418cs.log 2>&1
	$(HD)/bin/hadoop jar unics.jar UniCS -libjars $(JARS) \
              -D mapreduce.job.reduces=1 \
              $(P)/20170418/cs \
              $(P)/20170418/unics \
              > 20170418unics.log 2>&1

