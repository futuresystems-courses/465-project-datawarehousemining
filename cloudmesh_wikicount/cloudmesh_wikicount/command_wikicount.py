import subprocess
from pprint import pprint
import re


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
        print(output)
        print("helloooo")
        #ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', output )
        ips = re.findall( r'10.23.1.\d{1,3}', output)
        print(ips)
        if (exitCode == 0):
            return output
        else:
            raise Exception(command, exitCode, output)
        #subprocess.call("cm cluster create %s --count=%s --ln=%s --cloud=%s --flavor=%s --image=%s"% (name, count, login, cloud, flavor, image), shell=True)
       	#output = subprocess.check_output("cm cluster create %s --count=%s --ln=%s --cloud=%s --flavor=%s --image=%s"% (name, count, login, cloud, flavor, image), shell=True)
        #print('Have %d bytes in output' % len(output))
        print("hello world")
        # return output

    @classmethod
    def decomission_cluster(cls, name):
        subprocess.call("cm cluster remove %s"% (name), shell=True)
