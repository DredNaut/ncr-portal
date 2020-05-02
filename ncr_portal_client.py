#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import paramiko

class NCRPortalClient():

    def __init__(self):
        self.user = os.getenv('USER')
        self.server = 'ncr-0.ncr'
        self.instances = []

    def get_instances(self):
        ssh_cmd = ['ssh', '-q', '-i', f'/home/{self.user}/.ssh/server', f'ncr_portal@{self.server}', "query", '']
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

        ssh_cmd = ['ssh', '-q', '-i', f'/home/{self.user}/.ssh/server', f'ncr_portal@{self.server}', f"{task}", f'{instance}']
        proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE)
        return proc.stdout.read().decode("utf-8").strip('\n][\'').split(', ')


def main():
    portal = NCRPortalClient()
    portal.run()

if __name__ == '__main__':
    main()
