#!/usr/bin/python

"""
@author: Sharath Kumar Vijaya Kumar
@mail: svkumar2@ncsu.edu
@written on: 13th Sept, 2021

Lab Homework-1 (Q3)
This script is used to extract the interface details of a remote machine.
The details are limited to IP address, MAC address and Interface type.
The script expects 3 mandatory command line arguments in the order
username, hostname, password

Usage
-----
>>> python interface_details.py svkumar2, 152.7.176.80, password123
>>> Available interfaces on the machine:
>>> 0) lo
>>> 1) eth0
>>> 2) eth1
>>> Enter the interface name to get the corresponding detials / type 'all' for all interfaces: all
{
    "lo": {
        "ip-address": "127.0.0.1",
        "mac-address": "00:00:00:00:00:00",
        "interface-type": "link/loopback"
    },
    "eth0": {
        "ip-address": "10.25.11.111",
        "mac-address": "00:50:56:06:5e:14",
        "interface-type": "link/ether"
    },
    "eth1": {
        "ip-address": "152.7.176.80",
        "mac-address": "00:50:56:06:5e:15",
        "interface-type": "link/ether"
    }
}


"""

import argparse
import inspect
import json
import paramiko


def get_ip_address(ssh: paramiko.SSHClient, interface: str) -> str:
    """
    Returns IP address of a given interface

    Parameters
    ----------
    ssh : paramiko sshClient
    interface : str
        interface name. Eg: 'eth0'

    Returns
    -------
    IP address of the interface
    """
    sub_cmd1 = F"/usr/sbin/ip -o address | grep -w '{interface}' | grep -w 'inet' |"
    sub_cmd2 = R""" awk '{split($4, a, "/"); print a[1]}'"""
    stdin, stdout, stderr = ssh.exec_command(sub_cmd1 + sub_cmd2)
    ip_address = stdout.readlines()[0].replace('\n', '')
    return ip_address


def get_mac_address(ssh: paramiko.SSHClient, interface: str):
    """
    Returns MAC address of a given interface

    Parameters
    ----------
    ssh : paramiko sshClient
    interface : str
        interface name. Eg: 'eth0'

    Returns
    -------
    MAC address of the interface
    """
    sub_cmd1 = F"/usr/sbin/ip -o link | grep '{interface}' |"
    sub_cmd2 = R" awk '{print $(NF-2)}'"
    stdin, stdout, stderr = ssh.exec_command(sub_cmd1 + sub_cmd2)
    mac_address = stdout.readlines()[0].replace('\n', '')
    return mac_address


def get_interface_type(ssh: paramiko.SSHClient, interface: str):
    """
    Returns Interface type of a given interface

    Parameters
    ----------
    ssh : paramiko sshClient
    interface : str
        interface name. Eg: 'eth0'

    Returns
    -------
    Interface type of the interface
    """
    sub_cmd1 = F"/usr/sbin/ip -o link | grep '{interface}' |"
    sub_cmd2 = R" awk '{print $(NF-3)}'"
    stdin, stdout, stderr = ssh.exec_command(sub_cmd1 + sub_cmd2)
    interface_type = stdout.readlines()[0].replace('\n', '')
    return interface_type


def get_interface_details(ssh: paramiko.SSHClient):
    """
    Prints interface details in json format

    Parameters
    ----------
    ssh : paramiko sshClient
    """
    stdin, stdout, stderr = ssh.exec_command("/usr/sbin/ip -o link | awk {'print $2'}")
    interfaces = stdout.readlines()
    print("Available interfaces on the machine:")
    for i, interface in enumerate(interfaces):
        print("{}) {}".format(i, interface.replace(':\n', '')))
        interfaces[i] = interface.replace(':\n', '')
    int_name = input("Enter the interface name to get the corresponding details / type 'all' for all interfaces: ")
    if int_name == 'all':
        detail_dict = dict((key, {}) for key in interfaces)
        for _ in interfaces:
            detail_dict[_]['ip-address'] = get_ip_address(ssh, _)
            detail_dict[_]['mac-address'] = get_mac_address(ssh, _)
            detail_dict[_]['interface-type'] = get_interface_type(ssh, _)
    else:
        detail_dict = {int_name: {}}
        detail_dict[int_name]['ip_address'] = get_ip_address(ssh, int_name)
        detail_dict[int_name]['mac_address'] = get_mac_address(ssh, int_name)
        detail_dict[int_name]['interface_type'] = get_interface_type(ssh, int_name)
    detail_json = json.dumps(detail_dict, indent=4)
    print(detail_json)


def make_ssh_connection():
    """
    This method makes a SSH connection with the remote machine
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    try:
        ssh.connect(hostname=args.Hostname, port=args.port, username=args.Username, password=args.Password)
        if ssh.get_transport().is_active():
            get_interface_details(ssh)
    except paramiko.AuthenticationException as e:
        print(F"Function: {str(inspect.stack()[0][3])}, error: {e}")


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description="Get network interface details of a remote machine")
    my_parser.add_argument('Username', metavar='user', type=str, help="Login name")
    my_parser.add_argument('Hostname', metavar='host', type=str, help="Remote IP address")
    my_parser.add_argument('Password', metavar='password', type=str, help="Login password")
    my_parser.add_argument('-p', '--port', action='store', default=22, type=int, metavar='Port number',
                           help="Port number if default SSH port is not 22")
    args = my_parser.parse_args()
    make_ssh_connection()
