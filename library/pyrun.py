#!/usr/bin/python3

from subprocess import call

INPUT = """ \n
Interface                  IP-Address      OK? Method Status                Protocol \n
Ethernet0/0                12.12.12.1      YES NVRAM  up                    up \n
Ethernet0/1                14.14.14.1      YES NVRAM  up                    up \n
Ethernet0/2                192.168.247.25  YES NVRAM  up                    up \n
Ethernet0/3                unassigned      YES NVRAM  administratively down down \n
Serial1/0                  unassigned      YES NVRAM  up                    down \n
Serial1/1                  unassigned      YES NVRAM  administratively down down \n
Serial1/2                  unassigned      YES NVRAM  administratively down down \n
Serial1/3                  unassigned      YES NVRAM  administratively down down \n
Loopback0                  10.0.0.1        YES NVRAM  up                    up \n
Loopback999                10.0.0.4        YES manual up                    up \n
"""

call(["./test-module.py","-m","./cisco_ip_intf_facts_collect.py","-a",'output_text="{}"'.format(INPUT)])
