# Ansible role: IPTables

![Molecule Test](https://github.com/crgwilson/ansible-role-iptables/workflows/Molecule%20Test/badge.svg)

Install and manage legacy IPTables (non-nftables)

* Install IPTables packages
* Start & enable IPTables services
* Conditionally deploy some canned rules
* Configure IPTables rules & policies


## Variables

### iptables_configure_mangle

Boolean which determines whether the mangle table should be configured within the IPTables config file

NOTE: Similar variables exist for both the filter and nat tables (see `iptables_configure_filter` & `iptables_configure_nat`)

### iptables_mangle_policy

Dict containing configuration data for the default policies of the mangle table

Example:
```yaml
iptables_mangle_policy:
  PREROUTING: ACCEPT
  INPUT: ACCEPT
  FORWARD: ACCEPT
  OUTPUT: ACCEPT
  POSTROUTING: ACCEPT
```

NOTE: Similar variables exist for both the filter and nat tables (see `iptables_filter_policy` & `iptables_nat_policy`)

### iptables_mangle_rules

List containing raw IPTables rules be to dumped into the mangle table config

Example:
```yaml
-A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --set-mss 1300
```

NOTE: Similar variables exist for both the filter and nat tables (see `iptables_filter_rules` & `iptables_nat_rules`)

### iptables_filter_open_ports

If you're lazy (like me) and need to open some ports in your firewall, you can give this variable a list of port numbers. Each
port in this list will have `INPUT` accepted in the filter table

Example:
```yaml
iptables_filter_open_ports:
  - 22
  - 80
  - 443
```


## Testing

Unit tests for this project are setup using [Molecule](https://molecule.readthedocs.io/en/stable/) & [Docker](https://www.docker.com/).
Tests can be run using the below command:

```console
foo@bar:~$ molecule test --all
```
