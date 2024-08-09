#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import (
    AuthenticationException,
    NetMikoTimeoutException,
    SSHException,
)
import getpass
import csv
import xlrd
import sys


def get_info_ports(device):
    print(f"########## Connecting to Device {device.get('ipaddr')} ############")
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        cdp_n = net_connect.send_command("sh cdp n")
        cdpn_list = cdp_n.splitlines()
        print(cdpn_list[5].split())
        print(cdpn_list[6].split())
        print(cdpn_list[43].split())
        print(cdpn_list[44].split())
        print(cdpn_list[45].split())

        """
        for int in cdpn_list:
            try:
                int = int.split()
                hostname_int = int[0]
                interface = int[1]
                descrip = int[1]
                ports = net_connect.send_command(f"sh int {int[0]} | in Last input")
                port = ports.split()
                print (interface,descrip,ports)
                if ports:
                    #If never used
                    if 'never' in port[2] and 'never' in port[4]:
                        write_cvs(hostname,interface,descrip,'no')
                        continue
                   
                    #Hours since used
                    if ':' in ports:    
                        write_cvs(hostname,interface,descrip,'yes')
                        continue
                    #Days since used
                    if 'h' in port[2] or 'h' in port[4]:
                        write_cvs(hostname,interface,descrip,'yes')
                        continue
                    #Weeks since used
                    if 'w' in ports:
                        if 'w' in port[2]:
                            week = port[2]
                            index = week.find('w')
                            print (index)
                            w = convert_week(week[0:index])
                            if w > 5:
                                if 'w' in port [4]:
                                    week = port[4]
                                    index = week.find('w')
                                    w = convert_week(week[0:index])
                                    if w > 5:
                                        write_cvs(hostname,interface,descrip,'no')
                                        continue
                                    #If minor 
                                    else:
                                        write_cvs(hostname,interface,descrip,'yes')
                                        continue
                                #If w in second port
                                else:
                                    write_cvs(hostname,interface,descrip,'no')
                                    continue
                            #If minor of 5
                            else:
                                write_cvs(hostname,interface,descrip,'yes')
                                continue
                        #If w in firts port
                        else:
                            if 'w' in port [4]:
                                week = port[4]
                                index = week.find('w')
                                w = convert_week(week[0:index])
                                if w > 5:
                                    write_cvs(hostname,interface,descrip,'no')
                                    continue
                                else:
                                    write_cvs(hostname,interface,descrip,'yes')
                                    continue
                            else:
                                write_cvs(hostname,interface,descrip,'yes')
                                continue
                    #Years since used
                    if 'y' in port[2] or 'y' in port[4]:
                        write_cvs(hostname,interface,descrip,'no')
                        continue
                #If ports
                else:
                    write_cvs(hostname,interface,descrip,'yes')
                    continue
                    
            except:
                continue
        #"""
        net_connect.disconnect()


    except AuthenticationException:
        label2 = "\n##### Authentication failure: " + device["ip"] + " #####\n"
        print(label2)
    except NetMikoTimeoutException:
        label2 = "\n##### Time out to device: " + device["ip"] + " #####\n"
        print(label2)
    except EOFError:
        label3 = (
                "\n##### End of file while attempting device: " + device[
            "ip"] + " #####\n"
        )
        print(label3)
    except (SSHException):
        label4 = (
                "\n##### SSH issue. Check if SSHv2 is enabled: " + device[
            "ip"] + " #####\n"
        )
        print(label4)


def convert_week(week):
    week = int(week)
    print(f"In here is {week} weekkkkkkkkkkkkkkk")
    return week


def write_cvs(hostname, interface, description, status):
    with open(f"PuertosDisponibles_{hostname}.csv", "a",
              newline='') as csvfile:
        fieldnames = ['Interface', 'Description', 'Used']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print(
            f"**************** Getting info from:  {interface} ********************")
        writer.writerow({'Interface': interface,
                         'Description': description,
                         'Used': status})
    csvfile.close()
    print(f"'''''''''''''''''''' Success  {interface} '''''''''''''''''''''")


def create_dictionary(
        ip_address: str, device_os) -> dict:
    device = {
        "device_type": device_os,
        "ip": ip_address,
        "username": 'riosl11',
        "password": 'R1v3rs860@',
        "secret": 'R1v3rs860@',
    }
    return device


def main(args):
    device_dictionary = create_dictionary(args.get('ip'), args.get('device_type'))
    get_info_ports(device_dictionary)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
