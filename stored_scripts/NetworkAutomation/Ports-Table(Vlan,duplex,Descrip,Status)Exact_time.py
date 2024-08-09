#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2021. PadronDenisse Baxter
"""

import sys

from tools import Device


def get_info_ports(device_connection):
    try:
        device_connection.enable()
        hostname = device_connection.find_prompt()
        hostname = hostname[:-1]

        ports = device_connection.send_command("sh int status",
                                               delay_factor=10)
        interface_ports = ports.splitlines()

        # write_cvs(hostname, 'Interface', 'Description', 'Status', 'Vlan',
        #           'Duplex', 'Speed', 'Type', 'Last input', 'Last output')

        for interface in interface_ports:
            # Split to all the line
            interface_spit = interface.split()
            # Get the port name
            interface_name = interface_spit[0]
            # Get the index from the status of the port
            # i.e.1 "Te2/0/3   ** sALBRsac12 - ID connected    trunk        full    10G SFP-10GBase-SR "
            # i.e 2 Te2/0/11                     notconnect   1            full   1000 1000BaseSX SFP [5:6]
            # (i.e.1) index = 5
            if 'connected' in interface_spit:
                status = interface_spit.index('connected')
            if 'notconnect' in interface_spit:
                status = interface_spit.index('notconnect')
            if 'disabled' in interface_spit:
                status = interface_spit.index('disabled')
            if 'err' in interface_spit:
                status = interface_spit.index('err-disable')
            # Status intp[5]
            stat = interface_spit[status]
            # Vlan intp[6]
            vlan = interface_spit[status + 1]
            # Duplex intp[7]
            duplex = interface_spit[status + 2]
            # Speed intp[8]
            speed = interface_spit[status + 3]
            # Where port type begin
            leng_1 = status + 4
            # Port type, where leng_1 begins till len intp ends [9:9]
            type_p = interface_spit[leng_1:len(interface_spit)]
            # Convert "['1000BaseSX','SFP']" to string
            typep = convert(type_p)

            # Send cmd description for each port so we can get the full
            # description
            description = device_connection.send_command(
                f"sh int {interface_spit[0]} descrip", delay_factor=5)
            descri = description.split()
            # i.e. ['Interface','Status','Protocol','Description',
            # 'Te1/0','up','up',
            # 'dn=rAWMXzap01|rin=GigabitEthernet0/0/1|ro=LAN|ty=INFRA']
            descrip = descri[7:len(descri)]
            # Convert description to string
            descrip = convert(descrip)

            # Send cmd to get the last input and output value
            ports = device_connection.send_command(
                f"sh int {interface_spit[0]} | in Last input", delay_factor=5)
            # i.e. Last input never, output never, output hang never
            port = ports.split()
            # i.e. ['Last','input','never,','output','never,','output','hang','never']
            ports_input = port[2]
            ports_output = port[4]

            # Print all the information and save it to the csv
            data = {
                "hostname": hostname,
                "interface": interface,
                "description": descrip,
                "status": stat,
                "vlan": vlan,
                "duplex": duplex,
                "speed": speed,
                "type_port": typep,
                "ports_input": ports_input[:-1],
                "ports_output": ports_output[:-1],
            }
            device_connection.disconnect()
            # return data
            sys.stdout.write(str(data))
            # write_cvs(hostname, interface, descrip, stat, vlan, duplex,
            #           speed, typep, ports_input[:-1], ports_output[:-1])

    except Exception as err:
        print(err)


def convert_week(week):
    week = int(week)
    return week


# Fuction that converts "list" to string
def convert(s):
    str1 = " "
    return str1.join(s)


# def write_cvs(hostname, interface, description, stat, vlan, duplex, speed,
#               type_p, ports_input, ports_output):
#     # try:
#     date = datetime.date.today()
#     with open(f"PuertosDisponibles_{hostname}_{date}.csv", "a",
#               newline='') as csvfile:
#         fieldnames = ['Interface', 'Description', 'Status', 'Vlan', 'Duplex',
#                       'Speed', 'Type', 'Last input', 'Last output']
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
#                          'Last input': ports_input,
#                          'Last output': ports_output})
#     csvfile.close()
#     print(f"'''''''''''''''''''' Success  {interface} '''''''''''''''''''''")
#     except:
#        print ("There's a problem when writing")


def main(args: dict):
    device_dictionary = Device.create_device_dictionary(args)
    device_connection = Device.connection(device_dictionary)
    get_info_ports(device_connection)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
