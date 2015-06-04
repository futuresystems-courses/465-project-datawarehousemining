# 465-project-datawarehousemining

Our project aim is to process a large data set and to transform that data to give a more enhanced view for insight and decision-making. Specifically, we are using big data tools that will turn a raw dump of wikimedia project page visits into useful information.   Wikimedia projects consists of many popular web sites including Wikipedia, Mediawiki, wikibooks, etc.

Below procedure is followd for project implementatio

1. Take raw data of page view statistics from wikimedia https://dumps.wikimedia.org/other/pagecounts-raw/ Dataset is related to page view statistics across all Wikimedia sites (ie Wikipedia, wikibooks, Wikimedia, etc.)  with respect to hour, day, month and year
2. Create multi-node cluster using OpenStack (scalable and configurable)
3. Deploy mongodb to all nodes in cluster (positioned for future sharding across cluster)
4. Extract, transfer, and load datasets to one of the MongoDB instances
5. Create single node Hadoop cluster
6. Clustering of dataset using Map Reduce java program 
7. Execute on a virtual cluster
8. Output on command line
9. Single CM command for installation

## Installation

#### Pre-requisites required for setup

Must have following components installed:

* provisioned VM
* cloudmesh
* ansible
* git
* virtualenv

Recommend setting up ssh correctly as follows from command line:
* `eval $(ssh-agent -s)`
* `ssh-add ~/.ssh/id_rsa`

#### Installation Instructions

1. `git clone https://github.com/futuresystems/465-project-datawarehousemining.git` 
2. `cd 465-project-datawarehousemining\cloudmesh_wikicount`
3. `python setup.py install`
4. `cd ..` 
5. `cm wikicount install` 

## Usage

`cm wikicount install`

The cm install command will deploy mongodb on a cluster (size is scalable).   Hadoop will be installed on one node within the cluster.    For future development, mongodb can be sharded to handle the full dataset.
After deploying the components, the data extraction, transformation, and import into mongodb is executed on a small subset of the data.   Finally, Hadoop mapreduce function is executed to display a sample result of counts on project/page visits.

If for some reason script gets interrupted or an error gets returned, recommend running `cm wikicount decomission_cluster test` and then executing `cm wikicount install` again

`cm wikicount decomission_cluster NAME`

Decomissions a cluster called NAME. 

`cm wikicount build_cluster NAME` 
* [--count=N]
* [--ln=S]
* [--cloud=S]
* [--flavor=S]
* [--image=S]

Build a cluster called NAME with the specified options below.   Create files for ansible to execute deployments on VM's created
          Options:
             --count=N  number of nodes to create
             --ln=S     login name
             --cloud=S  cloud to use
             --flavor=S flavor to use
             --image=S  image to use 


`cm wikicount install_mongodb`

Uses ansible to deploy mongodb on all nodes in a cluster.   References files created from build_cluster function



Loading Data into MongoDB using import_wiki_pagecounts_May2014_1.sh on one node
Hadoop Deployment on single node cluster using Hadoop_Deployment_Automation.sh “instance name”  
Map reduce java program- WikiDataAnalysis.java  that will analyse the data using key and value pairs
Execute java file using Wiki_Data_Analysis_Automation.sh 
(Prerequisite: Availability of mongodb = wikimedia_project  with collection = pagecounts_small_May14)


