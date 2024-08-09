#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""
import datetime
import sys

from netmiko import redispatch
import csv
import time

from tools import Device


def connection_jump_server(jumpserver_connection, args):
    jumpserver_connection.write_channel(f"ssh -l {args.get('username')} {args.get('ip')}\n")
    time.sleep(8)
    connection = jumpserver_connection.read_channel()

    if 'password' in connection:
        jumpserver_connection.write_channel(f"{args.get('password')}\n")

    redispatch(jumpserver_connection, device_type='cisco_ios')
    hostname = jumpserver_connection.find_prompt()
    hostname = hostname[:-1]
    # uptime = net_connect.send_command('sh version | in uptime')
    # print (f"Uptime {uptime}" )

    ports = jumpserver_connection.send_command("sh int status", delay_factor=10)
    int_ports = ports.splitlines()
    write_cvs(hostname, 'Interface', 'Description', 'Status', 'Vlan',
              'Duplex', 'Speed', 'Type', 'Last input', 'Last output')
    # print (int_ports[1])

    i = 0
    for interfaces in int_ports:
        try:
            intp = interfaces.split()
            interface = intp[0]
            status = None
            if 'connected' in intp:
                status = intp.index('connected')
            if 'notconnect' in intp:
                status = intp.index('notconnect')
            if 'disabled' in intp:
                status = intp.index('disabled')
            if 'err' in intp:
                status = intp.index('err-disable')
            # print(status)
            stat = intp[status]
            vlan = intp[status + 1]
            duplex = intp[status + 2]
            speed = intp[status + 3]
            leng_1 = status + 4
            type_p = intp[leng_1:len(intp)]
            typep = convert(type_p)

            description = jumpserver_connection.send_command(
                f"sh int {intp[0]} descrip", delay_factor=5)
            descri = description.split()
            # print (descri)
            descrip = descri[7:len(descri)]
            descrip = convert(descrip)

            ports = jumpserver_connection.send_command(
                f"sh int {intp[0]} | in Last input", delay_factor=5)
            port = ports.split()
            ports_input = port[2]
            ports_input = ports_input[:-1]
            ports_output = port[4]
            ports_output = ports_output[:-1]

            print(hostname, interface, descrip, stat, vlan, duplex, speed,
                  typep, ports_input, ports_output)
            write_cvs(hostname, interface, descrip, stat, vlan, duplex,
                      speed, typep, ports_input, ports_output)

        except:
            continue

    jumpserver_connection.disconnect()


def convert(s):
    str1 = " "
    return (str1.join(s))


def write_cvs(hostname, interface, description, stat, vlan, duplex, speed,
              type_p, ports_input, ports_output):
    # try:
    date = datetime.date.today()
    with open(f"PuertosDisponibles_{hostname}_{date}.csv", "a",
              newline='') as csvfile:
        fieldnames = ['Interface', 'Description', 'Status', 'Vlan', 'Duplex',
                      'Speed', 'Type', 'Last input', 'Last output']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Interface': interface,
                         'Description': description,
                         'Status': stat,
                         'Vlan': vlan,
                         'Duplex': duplex,
                         'Speed': speed,
                         'Type': type_p,
                         'Last input': ports_input,
                         'Last output': ports_output})
    csvfile.close()


def main(args: dict):
    jumpserver_dictionary = Device.create_jumpserver_dictionary_from_params('10.119.3.119',
                                                                            args.get('username'),
                                                                            args.get('password'))
    jumpserver_connection = Device.connection(jumpserver_dictionary)
    connection_jump_server(jumpserver_connection, args)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)

if __name__ == "__main__":
    main()
