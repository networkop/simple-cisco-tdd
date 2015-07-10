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
module: cisco_trace_parse
short_description: parses the results of traceroute command of cisco cli
'''
EXAMPLES = '''
      cisco_trace_parse:
        dest_host: "{{ item.item.key }}"
        std_out: "{{ item.stdout }}"
'''

class TraceParse(object):

    def __init__(self, module):
        self.std_out = module.params['std_out']
        self.dest_host = module.params['dest_host']

    def parse(self):
        result = dict()
        path = list()
        for line in self.std_out.split("\n"):
            if 'msec' in line:
                path.append(line.split()[1])
        result[self.dest_host] = path
        return result


def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict(
            std_out=dict(required=True, type='str'),
            dest_host=dict(required=True, type='str')
        )
    )
    # instantiate command parser
    traceParser = TraceParse(module)
    # parse the output of show ip interface brief command
    result = traceParser.parse()
    module.exit_json(changed=False, ansible_facts=result)

# import module snippets
from ansible.module_utils.basic import *
main()
