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


# def test_default_service(host):
#     if host.system_info.distribution == 'debian':
#         svc = 'iptables-persistent'
#     else:
#         svc = 'iptables'
#
#     s = host.service(svc)
#     assert s.is_running
#     assert s.is_enabled
