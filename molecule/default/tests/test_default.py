import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_default_packages(host):
    if host.system_info.distribution == 'debian':
        pkg = 'iptables-persistent'
    else:
        pkg = 'iptables-services'

    p = host.package(pkg)
    assert p.is_installed


def test_default_config(host):
    if host.system_info.distribution == 'debian':
        conf = '/etc/iptables/rules.v4'
    else:
        conf = '/etc/sysconfig/iptables'

    f = host.file(conf)
    assert f.is_file

    rules = """*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]

# canned chains
-N STATE_CHECK
# allow related
-A STATE_CHECK -m state --state RELATED,ESTABLISHED -j ACCEPT
# drop invalid
-A STATE_CHECK -m state --state INVALID -j DROP

-N TCP_CHECK
# new packets must be syn
-A TCP_CHECK -m state --state NEW -p tcp ! --syn -j DROP
# no xmas packets
-A TCP_CHECK -p tcp --tcp-flags ALL ALL -j DROP
# no null packets
-A TCP_CHECK -p tcp --tcp-flags ALL NONE -j DROP

-N ACCEPT_ALL
-A ACCEPT_ALL -p tcp -j ACCEPT
-A ACCEPT_ALL -p udp -j ACCEPT

-N ICMP
-A ICMP -p icmp -m icmp --icmp-type address-mask-request -j DROP
-A ICMP -p icmp -m icmp --icmp-type timestamp-request -j DROP

COMMIT"""
    assert rules in f.content_string


def test_default_service(host):
    if host.system_info.distribution == 'debian':
        svc = 'netfilter-persistent'
    else:
        svc = 'iptables'

    s = host.service(svc)
    assert s.is_running
    assert s.is_enabled
