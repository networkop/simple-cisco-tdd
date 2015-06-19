#!/usr/bin/python
#coding: utf-8 -*-

# (c) 2015, Michael Kashin <m.kashin84@gmail.com>
#
# This file is part of Ansible
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
DOCUMENTATION = '''
---
module: cisco_ip_intf_facts_combine
short_description: parses and injects the results of show ip interface brief command of cisco cli
'''
EXAMPLES = '''
- cisco_ip_intf_facts: text={{ text_inventory.stdout }} command=siib
'''
import yaml

FILENAME="group_vars/all.yml"

class FactUpdater(object):

    def __init__(self, module):
        # ip2intf is a dictionary with IPs as keys and interface names as values
        self.ip2intf = module.params['ipTable']
        self.hostname = module.params['hostname']
        self.file_content = {'ip2host':{}} 

    def read(self):
        try:
            with open(FILENAME, 'r') as fileObj:
                self.file_content = yaml.load(fileObj)
        except:
            # in case there is no file - create it
            open(FILENAME, 'w').close()

    def write(self):
        with open(FILENAME, 'w') as fileObj:
            yaml.safe_dump(self.file_content, fileObj, explicit_start=True, indent=2, allow_unicode=True)


    def update(self):
        if not 'ip2host' in self.file_content:
            self.file_content['ip2host'] = dict()
        for ip in self.ip2intf:
            self.file_content['ip2host'][ip] = [self.hostname, self.ip2intf[ip]]



def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict(
            ipTable=dict(required=True, type='dict'),
            hostname=dict(required=True, type='str'),
        )
    )
    result = ''
    factUpdater = FactUpdater(module)
    try:
        factUpdater.read()
        factUpdater.update()
        factUpdater.write()
    except IOError as e:
        module.fail_json(msg="Unexpected error: " + str(e))

    module.exit_json(changed=False)

# import module snippets
from ansible.module_utils.basic import *
main()
