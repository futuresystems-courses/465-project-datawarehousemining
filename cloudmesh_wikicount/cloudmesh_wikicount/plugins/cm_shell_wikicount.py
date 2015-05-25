from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint

from cloudmesh_wikicount.command_wikicount import command_wikicount


class cm_shell_wikicount:

    def activate_cm_shell_wikicount(self):
        self.register_command_topic('mycommands', 'wikicount')

    @command
    def do_wikicount(self, args, arguments):
        """
        ::
          Usage:
              wikicount build_cluster NAME [--count=N] 
                                           [--ln=S] 
                                           [--cloud=S]
                                           [--flavor=S]
                                           [--image=S]
              wikicount decomission_cluster NAME
              wikicount setup_environment
              wikicount install_mongodb

          Arguments:
            NAME      Name of the wikicount cluster group
          Options:
             --count=N  number of nodes to create
             --ln=S     login name
             --cloud=S  cloud to use
             --flavor=S flavor to use
             --image=S  image to use
        """
        pprint(arguments)
        if arguments['build_cluster']:
            Console.ok("I want to build a cluster")
            name = arguments['NAME']
            count = arguments['--count'] or 3
            ln = arguments['--ln']
            cloud = arguments['--cloud']
            flavor = arguments['--flavor']
            image = arguments['--image']	
            command_wikicount.build_cluster(name, count)
        elif arguments['decomission_cluster']:
            Console.ok("I want to decomission a cluster")
            name = arguments['NAME']
            command_wikicount.decomission_cluster(name)
        elif arguments['setup_environment']:
            Console.ok("Initializing environment")
            command_wikicount.setup_environment()
        elif arguments['install_mongodb']: 
            Console.ok("Installing mongodb")
            command_wikicount.install_mongodb()
        elif arguments["NAME"] is None:
            Console.error("Please specify a name for the cluster")
        else:
            name = arguments["NAME"]
            Console.info("trying to reach {0}".format(name))
            status = command_wikicount.status(name)
            if status:
                Console.info("machine " + name + " has been found. ok.")
            else:
                Console.error("machine " + name + " not reachable. error.")
        pass

if __name__ == '__main__':
    command = cm_shell_wikicount()
    command.do_wikicount("iu.edu")
    command.do_wikicount("iu.edu-wrong")
