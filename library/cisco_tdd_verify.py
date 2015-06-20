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
module: 
short_description: 
'''
EXAMPLES = '''

'''


class ResultCompare(object):

    def __init__(self, module):
        self.dest_host = module.params['dest_host']
        self.src_host = module.params['src_host']
        self.trace_path = module.params['path']
        self.ref_scenario = module.params['scenario']
        self.ip2host = module.params['ip2host']
        self.scenario_name = module.params['scenario_name']

    def compare(self):
        trace_path_new = list()
        # Lookup hostnames of all known IP addresses
        for dev in self.trace_path:
            if dev in self.ip2host:
                trace_path_new.append(self.ip2host[dev][0])
            else:
                trace_path_new.append(dev)
        print "name " + self.scenario_name
        print "from !!! " + str(self.src_host)
        print "dest !!! " + str(self.dest_host)
        print "ref_scenario !!! " + str(self.ref_scenario[self.src_host][self.dest_host])
        print "trace !!! " + str(self.trace_path)
        print "trace_new !!! " + str(trace_path_new)
        if self.src_host in self.ref_scenario:
            if self.dest_host in self.ref_scenario[self.src_host]:
                ref_path = self.ref_scenario[self.src_host][self.dest_host]
                if not self. __validatepath(trace_path_new):
                    msg = "Failed scenario " + self.scenario_name +  ".\r\nTraceroute from " + self.src_host + " to " + self.dest_host + " has not traversed " + str(ref_path)
                    msg += "\r\n Actual path taken: " + ' -> '.join([self.src_host] + trace_path_new) + "\r\n"
                    return 1, msg
        return 0, 'no error'

    def __validatepath(self, path):
        index = 0
        for device in path:
            if device == self.ref_scenario[self.src_host][self.dest_host][index]:
                index += 1
                if index == len(self.ref_scenario[self.src_host][self.dest_host]):
                    return True
        return False
        

def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict(
            dest_host=dict(required=True, type='str'),
            src_host=dict(required=True, type='str'),
            scenario=dict(required=True, type='dict'),
            ip2host=dict(required=True, type='dict'),
            path=dict(required=True, type='list'),
            scenario_name=dict(required=True, type='str')
        )
    )
    comparator = ResultCompare(module)
    rc, error = comparator.compare()
    if rc != 0:
        module.fail_json(msg=error)
    else:
        module.exit_json(changed=False)

# import module snippets
from ansible.module_utils.basic import *
main()
