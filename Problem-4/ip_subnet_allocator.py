#!/usr/bin/python

"""
@author: Sharath Kumar Vijaya Kumar
@mail: svkumar2@ncsu.edu
@written on: 14th Sept, 2021

Lab Homework-1 (Q3)
This script is used to allocate IP subnetwork address based on
customer demand. The script uses pandas to maintain the assigned
IP subnets in an excel spreadsheet in the backend. The script asks
the user for 3 inputs
- customer name
-  desired network range from available options
- required number of hosts

Usage
-----
>>> python ip_subnet_allocator.py
******************************IP Subnet Allocator*******************************
List of available class B network addresses:
           network  avl_address  avl_percent
id
1   168.212.0.0/16        65024     99.21875
2   132.147.0.0/16        65536    100.00000
3   129.142.0.0/16        65536    100.00000
Enter customer name: skyworks
Choose your desired network address range, input 1 or 2 or ..: 1
Enter the required number of hosts: 12
Your assigned sub-network: 168.212.0.0/28

"""

import pandas as pd
from ipaddress import IPv4Network


if __name__ == '__main__':
    address_df = pd.read_excel('address_db.xlsx', sheet_name='available', converters={'avl_percent': float})
    address_df.set_index('id', inplace=True)
    print("IP Subnet Allocator".center(80, '*'))
    print("List of available class B network addresses:")
    print(address_df)
    customer_name = input("Enter customer name: ")
    selection = int(input("Choose your desired network address range, input 1 or 2 or ..: "))
    hosts = int(input("Enter the required number of hosts: "))
    net_add = address_df.at[selection, 'network']
    network = IPv4Network(net_add)
    if hosts < network.num_addresses and address_df.at[selection, 'avl_address'] != 0:
        for i in range(1, hosts):
            if 2 ** i >= hosts:
                host_bits = i
                break
        subnet_mask = 32 - host_bits
        used_df = pd.read_excel('address_db.xlsx', sheet_name='used', dtype=str)
        filtered_df = used_df[(used_df['network'] == net_add) & (used_df['subnet'].str.contains('/' + str(subnet_mask)))]
        if filtered_df.shape[0] > 0:
            assigned_subnet = list(network.subnets(new_prefix=subnet_mask))[filtered_df.shape[0]]
        else:
            assigned_subnet = list(network.subnets(new_prefix=subnet_mask))[0]
        print(F"Your assigned sub-network: {assigned_subnet}")
        new_row = {'customer': customer_name, 'network': net_add, 'subnet': str(assigned_subnet), 'hosts': hosts}
        used_df = used_df.append(new_row, ignore_index=True)
        address_df.at[selection, 'avl_address'] = int(address_df.at[selection, 'avl_address']) - assigned_subnet.num_addresses
        address_df.at[selection, 'avl_percent'] = (address_df.at[selection, 'avl_address'] / 65536)*100
        writer = pd.ExcelWriter('address_db.xlsx')
        used_df.to_excel(writer, sheet_name='used', index=False)
        address_df.to_excel(writer, sheet_name='available', index=True)
        writer.save()

    else:
        print("Required number of hosts exceed available addresses")

