#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""

import csv
import sys
from tools import Device


def get_info_ports(device_connection):
    device_connection.enable()

    hname_cm = device_connection.send_command("sh run | in hostname")
    hnamelist = hname_cm.split()
    hostname = hnamelist[1]
    ports = device_connection.send_command("sh int status")
    int_ports = ports.splitlines()
    write_cvs(hostname, 'Interface', 'Description', 'Status', 'Vlan', 'Duplex', 'Speed', 'Type', 'Time', 'Used')

    i = 0
    for int in int_ports:
        try:
            intp = int.split()
            interface = intp[0]
            # Posicion connected/notconnected

            if 'connected' in int:
                status = intp.index('connected')
                stat = 'Direct'

            elif 'notconnect' in int:
                status = intp.index('notconnect')
                stat = 'Indirect'

            elif 'err-disabled' in int:
                status = intp.index('err-disabled')
                stat = 'Err-disabled'

            elif 'disabled' in int:
                status = intp.index('disabled')
                stat = 'Disabled'

            elif 'sfpAbsent' in int:
                status = intp.index('sfpAbsent')
                stat = 'Disabled'

            elif 'xcvrInval' in int:
                status = intp.index('xcvrInval')
                stat = 'Disabled'

            vlan = intp[status + 1]
            duplex = intp[status + 2]
            speed = intp[status + 3]
            leng_1 = status + 4
            type_p = intp[leng_1:len(intp)]
            type_p = convert(type_p)


            try:
                description = device_connection.send_command(f'sh int {intp[0]} | in Descrip')
                descri = description.split()
                descrip = descri[1:len(descri)]
                descrip = convert(descrip)
            except:
                descrip = ' '

            if stat == 'connected':
                write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, 'time', 'yes')
                continue
            else:
                ports = device_connection.send_command(f"sh int {intp[0]} | in Last input")
                port = ports.split()
                if ports:
                    # If never used
                    if 'never' in port[2] and 'never' in port[4]:
                        time = 'never'
                        write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, time, 'no')
                        continue

                    # Hours since used
                    if ':' in ports:
                        time = ':'
                        write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, time, 'yes')
                        continue
                    # Days since used
                    if 'h' in port[2] or 'h' in port[4]:
                        time = 'h'
                        write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, time, 'yes')
                        continue
                    # Weeks since used
                    if 'w' in ports:
                        if 'w' in port[2]:
                            week = port[2]
                            index = week.find('w')
                            w = convert_week(week[0:index])
                            if w > 5:
                                if 'w' in port[4]:
                                    week = port[4]
                                    index = week.find('w')
                                    w = convert_week(week[0:index])
                                    if w > 5:
                                        if 'y' in port[2] or 'y' in port[4]:
                                            time = 'y'
                                            write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed,
                                                      type_p, time, 'no')
                                            continue
                                        else:
                                            time = port[4]
                                            write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed,
                                                      type_p, time, 'no')
                                            continue
                                    # If minor
                                    else:
                                        time = port[4]
                                        write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p,
                                                  time, 'yes')
                                        continue
                                # If w in second port
                                else:
                                    time = port[2]
                                    write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, 'no')
                                    continue
                            # If minor of 5
                            else:
                                time = port[2]
                                write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, 'yes')
                                continue
                        # If w in first port
                        else:
                            if 'w' in port[4]:
                                week = port[4]
                                index = week.find('w')
                                w = convert_week(week[0:index])
                                if w > 2:
                                    if 'y' in port[2] or 'y' in port[4]:
                                        time = 'y'
                                        write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p,
                                                  time, 'no')
                                        continue
                                    else:
                                        time = port[4]
                                        write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p,
                                                  time, 'no')
                                        continue
                                else:
                                    time = port[4]
                                    write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, time,
                                              'yes')
                                    continue
                            else:
                                time = port[4]
                                write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, time,
                                          'yes')
                                continue
                # If ports
                else:
                    write_cvs(hostname, interface, descrip, stat, vlan, duplex, speed, type_p, time, 'yes')
                    continue

        except:
            continue

        device_connection.disconnect()


def convert_week(week):
    week = int(week)
    print(f"In here is {week} weekkkkkkkkkkkkkkk")
    return week


def convert(s):
    str1 = " "
    return (str1.join(s))


def write_cvs(hostname, interface, description, stat, vlan, duplex, speed, type_p, time, used):
    with open(f"PuertosDisponibles_{hostname}.csv", "a", newline='') as csvfile:
        fieldnames = ['Interface', 'Description', 'Status', 'Vlan', 'Duplex', 'Speed', 'Type', 'Last used', 'Time',
                      'Used']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print(f"**************** Getting info from:  {interface} ********************")
        writer.writerow({'Interface': interface,
                         'Description': description,
                         'Status': stat,
                         'Vlan': vlan,
                         'Duplex': duplex,
                         'Speed': speed,
                         'Type': type_p,
                         'Time': time,
                         'Used': used})
    csvfile.close()


def main(args: dict):
    device_dictionary = Device.create_device_dictionary(args)
    device_connection = Device.connection(device_dictionary)
    get_info_ports(device_connection)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
