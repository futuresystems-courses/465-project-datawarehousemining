#!bin/bash
#This script will compile and execute tha java map reduce program to show the analysis of wiki data

cd /home/ubuntu
sudo apt-get install -y mongodb-10gen
export PATH=$JAVA_HOME/bin:$PATH
export HADOOP_CLASSPATH=$JAVA_HOME/lib/tools.jar
wget https://oss.sonatype.org/content/repositories/releases/org/mongodb/mongo-java-driver/2.13.1/mongo-java-driver-2.13.1.jar
export HADOOP_CLASSPATH=`pwd`/mongo-java-driver-2.13.1.jar:/usr/lib/jvm/java-6-oracle-amd64/lib/tools.jar
echo $HADOOP_CLASSPATH
hadoop com.sun.tools.javac.Main WikiDataAnalysis.java
jar cf wiki_data_analysis.jar WikiDataAnalysis*.class
hadoop jar wiki_data_analysis.jar WikiDataAnalysis
