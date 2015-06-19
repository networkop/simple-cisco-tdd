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
module: cisco_ip_intf_facts
short_description: parses the results of show ip interface brief command 
'''
EXAMPLES = '''
- cisco_ip_intf_facts: output_text={{ siib_text.stdout }}
'''


class SIIBparse(object):

    def __init__(self, module):
        self.output_text = module.params['output_text']
        #  data structure to store IP to interface name mapping
        self.ip2intf = dict()

    def parse(self):
        # go through each line of text looking for interface in 'up' state
        for line in self.output_text.split("\n"):
            row = line.split()
            if len(row) > 0 and row[-1] == 'up':
                # ip address is in 2nd column 
                ipAddress = row[1]
                # interface name is in 1st column
                intfName = row[0]
                # store ip and interface pair in a hash 
                self.ip2intf[ipAddress] = intfName
        # Parsed output wil be accessible in ansible through 'IPs' host variable 
        result = {
            "IPs": self.ip2intf
        }
        rc = 0 if len(self.ip2intf) > 0 else 1
        return rc, result

def main():
    module = AnsibleModule(
        argument_spec=dict(
            output_text=dict(required=True, type='str')
        )
    )
    # instantiate command parser
    siib = SIIBparse(module)
    # parse the output of show ip interface brief command
    rc, result = siib.parse()
    # exiting module
    if rc != 0:
        module.fail_json(msg="Failed to parse. Incorrect input.")
    else:
        module.exit_json(changed=False, ansible_facts=result)

# import module snippets
from ansible.module_utils.basic import *
main()
