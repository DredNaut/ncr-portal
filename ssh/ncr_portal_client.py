#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import paramiko

class NCRPortalClient():

    def __init__(self):
        self.user = os.getenv('NETID')
        self.DPORT = os.getenv('DPORT')
        self.server = 'localhost'
        self.instances = []
        self.debug = True

    def get_instances(self):
        if self.debug:
            ouput = ("TEST-jaredk", "jaredk")
        else:
            ssh_cmd = ['ssh', '-q', '-i', '/root/.ssh/test', 'root@172.18.0.2',  "query", '']
            proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE)
            output = proc.stdout.read().decode("utf-8")
            output = re.sub('[\n\[\]\']', '', output)
            output = output.split(', ')
            return output

    def run(self, task, instance):
        if task is None:
            self.parser.print_help()
            exit(1)
        if task.lower() == "query":
            self.instances = self.get_instances()
            print(f"{self.instances}")
        if self.debug:
            return (task, instance)
        else:
            ssh_cmd = ['ssh', '-q', '-i', f'/root/.ssh/test', f'root@172.18.0.2', f"{task}", f'{instance}']
            proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE)
            return proc.stdout.read().decode("utf-8").strip('\n][\'').split(', ')


def main():
    portal = NCRPortalClient()
    portal.run()

if __name__ == '__main__':
    main()
