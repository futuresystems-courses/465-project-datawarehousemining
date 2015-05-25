import subprocess
from pprint import pprint
import re
import os


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
        with open('inventory.txt', 'w') as f:
            f.write("[%s]\n" % "ansible-wikicount")
            for ip in ips:
                print ip
                f.write("%s\n" % str(ip))        
        if (exitCode == 0):
            return output
        else:
            raise Exception(command, exitCode, output)

    @classmethod
    def decomission_cluster(cls, name):
        subprocess.call("cm cluster remove %s"% (name), shell=True)
        print("removing inventory.txt file")
        subprocess.call("rm inventory.txt", shell=True)
    @classmethod
    def setup_environment(cls):
        print("setting up SSH to access multiple machines")
        os.system("eval $(ssh-agent -s);ssh-add ~/.ssh/id_rsa")
        return 1

