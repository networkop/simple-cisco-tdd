## SIMPLE NETWORK TDD FRAMEWORK


This framework creates a convenient way to test and verify routing within a redundant, highly-available network topology.
It tries to emulate behaviour of BDD frameworks like [Cucumber][cucumber-link] or [Lettuce][lettuce-link]. It uses business-friendly traffic scenarios to verify traffic flows within the network. Another use may be in network failover testing where it can verify traffic re-routing behaviour under specific network failure conditions. For example, a scenario to verify that a traffic from a Data Centre to Branch Office "A" will traverse routers R11 and R21 would look like `1.1 From DC-CORE to BR1-CORE via R11, R21`.  This network TDD framework uses Ansible to build a local IP-to-Hostname database and run multiple parallel traceroutes.  

This network TDD framework is designed with the following assumptions:

* All routing is performed within global VRFs 
* All devices are reachable
* ICMP responses are allowed throughout the network
* All network devices have ssh enabled

## QUICKSTART GUIDE

This guide assumes the following prerequisites have been met:

* Ansible is installed on the test machine
* Test machine has access to all network devices

### Clone git repository

``` bash
git clone https://github.com/networkop/simple-cisco-tdd.git tdd-network
cd tdd-network
```

### Populate local inventory

Edit `./myhosts` with information about all relevant network devices. Edit `hosts_var` directory files with host-specific authentication and IP address details ([full list of inventory options][ansible-inventory]). Verify that Ansible can talk to network devices:

``` bash
ansible R1 -u cisco -m raw -a "show clock"
R1 | success | rc=0 >>

*00:56:06.213 UTC Sat Jul 11 2015
```

### Create traffic scenarios

Edit `./scenarios/all.txt` file to match your environment. The file contains a list of scenarios representing a certain state in the network. Each scenario has one or more scenario steps, representing a particular traffic flow. The keywords in scenario steps are `From`, `To` and `Via`. The first two can only contain a single device name, while `Via` can contain a comma-separated ordered list of devices. The framework will verify that each of the devices in `Via` is traversed in the order specified in the list.

``` text
1. Testing of Primary Link
1.1 From R1 to R3 via R2
1.2 From R1 to R4 via R2, R3
1.3 From R2 to R4 via R3
1.4 From R1 to R2 via R2
2. Testing of Backup Link
2.1 From R1 to R3 via R4
2.2 From R1 to R2 via R4,R3
```

### Collect IP address information and process scenarios

Run `cisco-ip-collect.yml` playbook. This playbook contains two plays tagged `collect` and `scenario`. If either IP addressing or scenario file are changed the corresponding play needs to be re-run.
The result of the play is a new file `./group_vars/all.yml`

``` bash
ansible-playbook cisco-ip-collect.yml
```

### Run TDD play to verify a scenario

Select which scenario to run and watch for errors.

``` bash
ansible-playbook cisco_tdd.yml
Enter scenario number [1]: 1
```

If all scenarios were successful Ansible should return no errors. In case one or more scenario steps failed, the error will be displayed:

``` bash
msg: Failed scenario Primary WAN failed at Branch #2.
Traceroute from DC-CORE to BR2-CORE has not traversed ['DC-WAN1', 'BR1-WAN1']
 Actual path taken: DC-CORE -> DC-WAN1 -> 1.1.1.2 -> BR2-WAN1 -> BR2-CORE
```

[cucumber-link]: https://cucumber.io/
[lettuce-link]: http://lettuce.it/
[ansible-inventory]: http://docs.ansible.com/intro_inventory.html#list-of-behavioral-inventory-parameters
