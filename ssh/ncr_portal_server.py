#!/usr/bin/env python3
# Name:     ncr_portal_server.py
# Author:   Jared Knutson
# Use:      Allows users with authorization to interact with
#           their instances through Ganeti. Current options for interaction are 
#           reboot, shutdown, and start. Uses the netid exported from the 
#           ssh session, see authorized_keys file for example.

import os, subprocess
import sys
import re, json
import logging

class NCRPortalServer():

    def __init__(self):
        # Get environment vars for command, public key, netid, and create logger
        self.command = (os.getenv('SSH_ORIGINAL_COMMAND')).split()
        self.netid = os.getenv('NETID')
        self.logger1 = self.create_logger()
        (self.sanatized_command, self.sanatized_instance) = self.sanatize_input()
        self.authorized_user = False
        self.authorized_instances = []

    def run(self):
        return self.authorize_user()

    # Set up logger using python3 logging module
    def create_logger(self):
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M',filename='/home/cs447/log/ncr_portal.log')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        return logging.getLogger("{}".format(self.netid))



    # Sanatize user input command
    def sanatize_input(self):
        command_pattern = '[^\w\d]'
        instance_pattern = '[^\w\d-]'

        if len(self.command) == 1:
            self.logger1.debug("Sanatizing user input, user specified command only.")
            return (re.sub(command_pattern, '',self.command[0]), '')

        elif len(self.command) == 2:
            self.logger1.debug("Sanatizing user input, user specified command and instance.")
            return (re.sub(command_pattern, '',self.command[0]), re.sub(instance_pattern, '',self.command[1]))

        else:
            self.logger1.debug("Sanatizing user input, User specified incorrect amount of arguments.")
            self.logger1.debug("Incorrect Formatting, please see help menu for correct formatting.")
            sys.exit(1)




    # Use gnt-list to match users netid, public key, and instance name IOT authorize user
    def find_user_instance(self, string):
        found = None
        gnt_info = re.search("([a-zA-z0-9-]*)\s+({.*})", string)
        if gnt_info:
            # if no instance specified by user
            if self.sanatized_instance == "":

                instance = gnt_info.groups()[0]
                self.logger1.debug(f"checking {instance}")
                info = json.loads(gnt_info.groups()[1].replace('\'', '"'))

                # Add instance checking to if statement, to search for specific instance.
                if info and info['netid'] == self.netid:

                    self.logger1.debug(f"{instance}, Match found for instance owner and remote user {self.netid}")
                    found = instance

            # If user specifies instance to target
            else:

                instance = gnt_info.groups()[0]
                info = json.loads(gnt_info.groups()[1].replace('\'', '"'))

                if info and info['netid'] == self.netid and instance == self.sanatized_instance:

                    self.logger1.debug(f"{instance}, Match found for instance owner and remote user {self.netid}")
                    found = instance

        return found


    # Commands to pass to gnt-interface if user is authorized
    # Current Supported Commands: REBOOT, REINSTALL
    def gnt_interface(self, action):

        # If user specifies to reboot, run gnt-instance reboot
        if action == "REBOOT":
           #####
           # Example process of rebooting instnace in BASH:
           # /usr/sbin/gnt-instance reboot --shutdown-timeout=5 <instance>
           #####
           self.logger1.debug(f"Rebooting instance {self.instance}") 
           print(f"Rebooting instance {self.instance}") 
           subprocess.run(['/usr/sbin/gnt-instance', 'reboot', '--shutdown-timeout=5', f'{self.instance}'])

        # If user specifies to reinstall, run gnt-instance stop, reinstall, start
        #elif action == "REINSTALL":
            #####
            # Example process of reinstalling instance in BASH:
            # /usr/sbin/gnt-instance stop <instance>
            # /usr/sbin/gnt-instance reinstall -o netid=netid,publickey=priv_key,cs447=true <instnace>
            # /usr/sbin/gnt-instance start <instance>
            #####
           #self.logger1.info("Stopping instance {}".format(instance)) 
           #subprocess.run(['/usr/sbin/gnt-instance', 'stop', '--timeout=10', '{}'.format(instance)])
           #self.logger1.info("Reinstalling instance {}".format(instance)) 
           #subprocess.run(['/usr/sbin/gnt-instance', 'reinstall', '-O', 'netid={},publickey={},cs447=true'.format(netid,pub_key),'{}'.format(instance)])
           #self.logger1.info("Starting instance {}".format(instance)) 
           #subprocess.run(['/usr/sbin/gnt-instance', 'start', '{}'.format(instance)])

        elif action == "START":
            #####
            # Example process of starting instance in BASH:
            # /usr/sbin/gnt-instance start <instance>
            #####
           self.logger1.debug(f"Starting instance {self.instance}") 
           print(f"Starting instance {self.instance}") 
           subprocess.run(['/usr/sbin/gnt-instance', 'start', f'{self.instance}'])

        elif action == "SHUTDOWN":
            #####
            # Example process of stopping instance in BASH:
            # /usr/sbin/gnt-instance stop  --timeout=10 <instance>
            #####
           self.logger1.debug(f"Stopping instance {self.instance}") 
           print(f"Stopping instance {self.instance}") 
           subprocess.run(['/usr/sbin/gnt-instance', 'stop', '--timeout=10', f'{self.instance}'])

        elif action == "INFO":
            #####
            # Example process of getting info from instance in BASH:
            # /usr/sbin/gnt-instance info <instance>
            #####
           self.logger1.debug(f"Getting info instance {self.instance}") 
           print(f"Getting info instance {self.instance}") 
           subprocess.run(['/usr/sbin/gnt-instance', 'info', f'{self.instance}'])
           output = subprocess.Popen(["/usr/sbin/gnt-instance", "info", self.instance ],stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
           self.logger1.debug(output.stdout.read().decode('utf-8'))
           print(output.stdout.read().decode('utf-8'))

        else:
            self.logger1.error(f"NOT A COMMAND: {action}")

    def gnt_list(self):
        gnt_list = ['/usr/sbin/gnt-instance', 'list', '-o', 'name,custom_osparams', f'*{self.netid}']
        # Call gnt-instance list and parse into var 'output'
        p = subprocess.Popen(gnt_list,stdout=subprocess.PIPE)
        return str(p.communicate()[0]).split(r'\n')

    def authorize_user(self):
        output = self.gnt_list()
        # For each line in gnt-instnace list attempt to find specified instance associated with user
        for line in output:
            self.instance = self.find_user_instance(line)
            # If the instance is found belonging to user
            if self.instance:
                # netid and instance have been matched from gnt-instace list,
                # user is now authorized
                self.authorized_instances.append(self.instance)
                self.authorized_user = True
                if self.sanatized_command != "query":
                    break

        self.logger1.debug(f"INSTANCE LIST: {self.authorized_instances}")
        if self.authorized_user:
            if self.sanatized_command == "query":
                print(f"{self.authorized_instances}")
                return self.authorized_instances
            else:
                self.gnt_interface(self.sanatized_command.upper())
                return True
        else:
            return False


def main():
    portal = NCRPortalServer()
    portal.run()

if __name__ == '__main__':
    main()
