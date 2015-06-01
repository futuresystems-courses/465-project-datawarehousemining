import subprocess
from pprint import pprint
import re
import os
import socket
import io


class command_wikicount(object):
    @classmethod
    def build_cluster(cls, name, count = 3, login = "ubuntu", cloud = "india", flavor = "m1.small", image = "futuresystems/ubuntu-14.04"): 
        process = subprocess.Popen("cm cluster create %s --count=%s --ln=%s --cloud=%s --flavor=%s --image=%s"% (name, count, login, cloud, flavor, image), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ''

  
        # Poll process for new output until finished
        for line in iter(process.stdout.readline, ""):
            print line,
            output += line

        process.wait()
        exitCode = process.returncode

          
        print("fetching ip addresses from output of cm cluster create")
        ips = re.findall( r'10.23.\d.\d{1,3}', output)
        print(ips)
        
        
        print("writing ip addreses to inventory.txt file")  
        with open('./ansible/inventory.txt', 'w') as f:
            f.write("[%s]\n" % "ansible-wikicount")
            for ip in ips:
                print ip
                f.write("%s\n" % str(ip))

        print("getting hostnames and writing to hostnames.txt file")
        hostnames = re.findall( '([\w]+)\s[\w.]+\W\s10.23.\d.\d{1,3}', output)
        print(hostnames)
        configdb_string= hostnames[0] + "-i:27019,"+ hostnames[1] + "-i:27019," + hostnames[2] + "-i:27019"
        print(configdb_string)
        os.system("configdb_string=%s" % str(configdb_string))
        os.system("echo $configdb_string")
        with open('./ansible/hostnames.txt', 'w') as f:
            for hostname in hostnames[:3]:
                print(hostname)
                f.write("%s" % hostname)
                #append port
                if hostname == hostnames[2]:
                    f.write("-i:27019")
                else:
                    f.write("-i:27019,")

        print("writing hostname for Hadoop instance")
        with open('./ansible/hadoop_hostname.txt', 'w') as f:
            f.write("%s" % hostnames[0])


        print("specifying config servers in inventory.txt file")
        with open("./ansible/inventory.txt", "a") as f:
            f.write("\n[config-servers]\n")
            for ip in ips[:3]:
                f.write("%s\n" % str(ip))

        print("specifying hadoop servers in inventory.txt file")
        with open("./ansible/inventory.txt", "a") as f:
            f.write("\n[hadoop]\n")
            f.write("%s\n" % ips[0])

        with open("./ansible/hadoop-ip.txt", 'w') as f:
            f.write("%s" % ips[0])

        print("enable root access on all machines in cluster using ansible")
        subprocess.call("ansible-playbook -i ./ansible/inventory.txt -c ssh ./ansible/enable-root-access.yaml", shell=True)

        if (exitCode == 0):
            return output
        else:
            raise Exception(command, exitCode, output)

    @classmethod
    def decomission_cluster(cls, name):
        subprocess.call("cm cluster remove %s"% (name), shell=True)
        print("removing inventory.txt file")
        subprocess.call("rm ./ansible/inventory.txt", shell=True)

    @classmethod
    def install(cls):
        print("setting up SSH to access multiple machines")
        os.system("eval $(ssh-agent -s)")
        os.system("ssh-add ~/.ssh/id_rsa")
        os.system("cm wikicount build_cluster test")
        command_wikicount.install_mongodb()
        os.system("ansible-playbook -i ./ansible/inventory.txt -c ssh ./ansible/hadoop.yaml")
        with open('ansible/hadoop-ip.txt', 'r') as content_file:
            hadoop_ip = content_file.read()
        with open('ansible/hadoop_hostname.txt', 'r') as content_file:
            hadoop_hostname= content_file.read()
        hadoop_command_line="ssh ubuntu@" + hadoop_ip + " bash -s < Hadoop/Hadoop_Deployment_Automation.sh " + hadoop_hostname
        print(hadoop_command_line)
        os.system(hadoop_command_line)
        print("running map reduce test case")
        hadoop_command_line="ssh ubuntu@" + hadoop_ip + " bash -s < Hadoop/Wiki_Data_Analysis_Automation.sh"
        os.system(hadoop_command_line)
        return 1

    @classmethod
    def install_mongodb(cls):
        subprocess.call("ansible-playbook -i ./ansible/inventory.txt -c ssh ./ansible/mongodb.yaml", shell=True)
        with open('ansible/hadoop-ip.txt', 'r') as content_file:
            hadoop_ip = content_file.read()
        hadoop_command_line="ssh ubuntu@" + hadoop_ip + " bash -s < bin/import_wiki_pagecounts_May2014_1.sh"
        os.system(hadoop_command_line)
        return 1

