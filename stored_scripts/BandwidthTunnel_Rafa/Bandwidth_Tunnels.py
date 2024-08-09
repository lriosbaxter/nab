#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""

import getpass
import sys

import xlrd
import csv

from tools import Device


def get_evidence(device_connection, device_dictionary, i):
    device_connection.enable()

    hostname = device_connection.find_prompt()
    hostname = hostname[:-1]

    tunnels_int = device_connection.send_command("show ip int brief | in Tunnel")

    if tunnels_int:
        for tunnels in tunnels_int.splitlines():
            tunnels = tunnels.split()
            tunnel = tunnels[0]
            ip_tunnel = tunnels[1]

            bandwidth_info = device_connection.send_command(f"show run int {tunnel} | in bandwidth", delay_factor=5)
            if bandwidth_info:
                bandwidth = bandwidth_info.split()
                try:
                    bandwidth = bandwidth[1]
                except:
                    print('Error')

            else:
                bandwidth = ' '
            write_cvs(hostname, device_dictionary.get('ip'), tunnel, ip_tunnel, bandwidth)
    else:
        write_cvs(hostname, device_dictionary.get('ip'), 'No tunnel', '', '')
    device_connection.disconnect()


def write_cvs(hostname, ipaddr, tunnel, ip_tunnel, bandwidth):
    with open(f"Bandwidth_Tunnels(06-08-2021).csv", "a", newline='') as csvfile:
        fieldnames = ['Hostname', 'IP_Address', 'Tunnel', 'Tunnel_IP', 'Bandwidth']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # print (f"**************** Getting info from:  {interface} ********************")
        writer.writerow({'Hostname': hostname,
                         'IP_Address': ipaddr,
                         'Tunnel': tunnel,
                         'Tunnel_IP': ip_tunnel,
                         'Bandwidth': bandwidth})
    csvfile.close()


def main(args: dict):
    write_cvs('Hostname', 'IP_Address', 'Tunnel', 'Tunnel_IP', 'Bandwidth')

    workbook = xlrd.open_workbook(r"Router.xlsx")
    sheet = workbook.sheet_by_index(0)
    for index in range(1, sheet.nrows):
        i = 0
        ip_address = sheet.row(index)[1].value
        device_dictionary = Device.create_device_dictionary_from_params('cisco_ios', ip_address, args.get('username'),
                                                                        args.get('password'))
        device_connection = Device.connection(device_dictionary)
        get_evidence(device_connection, device_dictionary, i)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
