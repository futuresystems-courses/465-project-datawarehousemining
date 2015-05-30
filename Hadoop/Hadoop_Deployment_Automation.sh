#!/bin/bash
#commands used to Chef installation and configuration required for deploying Hadoop

apt-get update
cd /home/ubuntu
curl -L https://www.opscode.com/chef/install.sh | bash
wget http://github.com/opscode/chef-repo/tarball/master
tar -zxf master
mv *-chef-repo* chef-repo
rm master
cd chef-repo/
mkdir .chef
echo "cookbook_path [ '/home/ubuntu/chef-repo/cookbooks' ]" > .chef/knife.rb
cd cookbooks
knife cookbook site download java
knife cookbook site download apt
knife cookbook site download yum
knife cookbook site download hadoop
knife cookbook site download ohai
knife cookbook site download sysctl
tar -zxf java*
tar -zxf apt*
tar -zxf yum*
tar -zxf hadoop*
tar -zxf sysctl*
tar -zxf ohai*
rm *.tar.gz

#In /home/ubuntu/chef-repo/roles create java.rb -> contents are uploaded in github
cd /home/ubuntu/chef-repo/roles
echo "name "java"
description "Install Oracle Java"
default_attributes(
  "java" => {
    "install_flavor" => "oracle",
    "jdk_version" => "6",
    "set_etc_environment" => true,
    "oracle" => {
      "accept_oracle_download_terms" => true
    }
  }
)
run_list(
  "recipe[java]"
)" > java.rb

echo "name "hadoop"
description "set Hadoop attributes"
default_attributes(
  "hadoop" => {
    "distribution" => "bigtop",
    "core_site" => {
      "fs.defaultFS" => "hdfs://saksgupt-001"
    },
    "yarn_site" => {
      "yarn.resourcemanager.hostname" =>"saksgupt-001"
    }
  }
)
run_list(
  "recipe[hadoop]"
)
" > hadoop.rb

#In /home/ubuntu/chef-repo create solo.rb ->contents are uploaded in github
cd ..
echo "file_cache_path \"/home/ubuntu/chef-solo\"
cookbook_path \"/home/ubuntu/chef-repo/cookbooks\"
role_path \"/home/ubuntu/chef-repo/roles\"
verify_api_cert true" > solo.rb


#In /home/ubuntu/chef-repo create solo.json ->contents are uploaded in github
echo "{
  \"run_list\": [ \"role[java]\", \"recipe[java]\", \"role[hadoop]\", \"recipe[hadoop::hadoop_hdfs_namenode]\",
   \"recipe[hadoop::hadoop_yarn_nodemanager]\", \"recipe[hadoop::hadoop_yarn_resourcemanager]\",  \"recipe[hadoop::hadoop_hdfs_datanode]\" ]
}">solo.json

echo "127.0.0.1  saksgupt-001">> /etc/hosts

#install
chef-solo -j /home/ubuntu/chef-repo/solo.json -c /home/ubuntu/chef-repo/solo.rb

#initiate all node
#Data node needs to be start first if it is single node cluster

/etc/init.d/hadoop-hdfs-namenode init

service hadoop-hdfs-datanode start

service hadoop-hdfs-namenode start
/usr/lib/hadoop/libexec/init-hdfs.sh

service hadoop-yarn-resourcemanager start
service hadoop-yarn-nodemanager start

echo jps
