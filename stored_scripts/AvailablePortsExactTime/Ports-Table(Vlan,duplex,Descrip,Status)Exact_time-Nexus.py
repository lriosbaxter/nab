#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2021. PadronDenisse Baxter
"""
import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import (
    AuthenticationException,
    NetMikoTimeoutException,
    SSHException,
)
import csv
import sys


def get_info_ports(device, ipaddr):
    print(f"########## Connecting to Device {ipaddr} ############")
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        hostname = net_connect.find_prompt()
        hostname = hostname[:-1]
        ports = net_connect.send_command("sh int status", delay_factor=10)
        int_ports = ports.splitlines()
        write_cvs(hostname, 'Interface', 'Description', 'Status', 'Vlan',
                  'Duplex', 'Speed', 'Type', 'Used')
        # print (int_ports[1])

        print(f"########## Connecting to Hostname {hostname} ############")
        i = 0
        print(int_ports)
        for int in int_ports:
            try:
                intp = int.split()
                interface = intp[0]
                # print(intp)
                status = None
                if 'connected' in intp:
                    status = intp.index('connected')
                if 'notconnect' in intp:
                    status = intp.index('notconnect')
                if 'disabled' in intp:
                    status = intp.index('disable')
                if 'err' in intp:
                    status = intp.index('err-disable')
                if 'sfpAbsent' in intp:
                    status = intp.index('sfpAbsent')
                # print(status)
                stat = intp[status]
                vlan = intp[status + 1]
                duplex = intp[status + 2]
                speed = intp[status + 3]
                leng_1 = status + 4
                type_p = intp[leng_1:len(intp)]
                typep = convert(type_p)

                description = net_connect.send_command(
                    f"sh int {intp[0]} descrip", delay_factor=5)
                descri = description.split()
                descrip = descri[7:len(descri)]
                descrip = convert(descrip)

                """
                ports = net_connect.send_command(f"sh int {intp[0]} | in Last input",delay_factor=5)
                port = ports.split()
                ports_input = port[2]
                ports_output = port[4]
                """
                last_flap = net_connect.send_command(
                    f"sh int {intp[0]} | in flapped")

                interface_info = net_connect.send_command(f"sh int {intp[0]}")
                interface_info = interface_info.splitlines()
                if 'up' in interface_info[0]:
                    state = 'Up'
                elif 'down' in interface_info[0]:
                    state = 'Down'
                else:
                    state = 'Unknown'

                if state == 'Down' and 'never' in last_flap:
                    used = "No"
                elif state == 'Up':
                    used = "Yes"
                else:
                    used = "Need to review"

                print(hostname, interface, descrip, stat, vlan, duplex, speed,
                      typep, used)
                write_cvs(hostname, interface, descrip, stat, vlan, duplex,
                          speed, typep, used)

            except:
                continue

        net_connect.disconnect()


    except (AuthenticationException):
        label2 = "\n##### Authentication failure: " + device["ip"] + " #####\n"
        print(label2)
    except (NetMikoTimeoutException):
        label2 = "\n##### Time out to device: " + device["ip"] + " #####\n"
        print(label2)
    except (EOFError):
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

    """
    except:
        print('Something wrong happened')
        #write_cvs(hostname,interface,descrip,stat,vlan,duplex,speed,type_p,'Something wrong happened')
    """


def convert_week(week):
    week = int(week)
    print(f"In here is {week} weekkkkkkkkkkkkkkk")
    return week


def convert(s):
    str1 = " "
    return (str1.join(s))


# def write_cvs(hostname, interface, description, stat, vlan, duplex, speed,
#               type_p, used):
#     # try:
#     date = datetime.date.today()
#     with open(f"PuertosDisponibles_{hostname}_{date}.csv", "a",
#               newline='') as csvfile:
#         fieldnames = ['Interface', 'Description', 'Status', 'Vlan', 'Duplex',
#                       'Speed', 'Type', 'Used']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         print(
#             f"**************** Getting info from:  {interface} ********************")
#         writer.writerow({'Interface': interface,
#                          'Description': description,
#                          'Status': stat,
#                          'Vlan': vlan,
#                          'Duplex': duplex,
#                          'Speed': speed,
#                          'Type': type_p,
#                          'Used': used})
#     csvfile.close()
#     print(f"'''''''''''''''''''' Success  {interface} '''''''''''''''''''''")
#     # except:
#     #    print ("There's a problem when writing")


def main(args: dict):
    ip_address = args.get('ip')
    get_info_ports(args, ip_address)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
