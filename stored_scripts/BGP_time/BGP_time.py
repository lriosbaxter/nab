#! /usr/bin/env python
""" 
    Dictionary of the comands for getting info
    Copyright (c) 2019. PadronDenisse
"""

from jinja2 import Template
import xlrd
import csv
from netmiko import ConnectHandler
from netmiko.ssh_exception import (
    AuthenticationException,
    NetMikoTimeoutException,
    SSHException,
)
import getpass
from datetime import date
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def get_info(device):
    print (f"########## Connecting to Device {device['ip']} ############")
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        
        hostname = net_connect.find_prompt()
        hostname = hostname[:-1]
        
        print (hostname)
        bgp_summary = net_connect.send_command("sh bgp summary")
        bgp_summary = bgp_summary.splitlines()
        print (bgp_summary)
        
        for bgp in bgp_summary:
            if bgp[:1].isdigit() and '.' in bgp:
                bgp_values = bgp.split()
                ip_neigh = bgp_values[0]
                uptime = bgp_values[8]
                status = bgp_values[9:]
                print (ip_neigh, uptime)
                write_cvs(hostname,device['ip'],ip_neigh,uptime,status)
            else:
                continue
        
        print (f"'''''''''''''''''''' Success  {hostname} '''''''''''''''''''''")
        net_connect.disconnect()
    
          
    except (AuthenticationException):
        label2 = "\n##### Authentication failure: " + device["ip"] + " #####\n"
        print(label2)
        write_cvs('',device['ip'],'AuthenticationException','','')
       
    except (NetMikoTimeoutException):
        label2 = "\n##### Time out to device: " + device["ip"] + " #####\n"
        write_cvs('',device['ip'],'NetmikoIssue','','')
    except (EOFError):
        label3 = (
            "\n##### End of file while attempting device: " + device["ip"] + " #####\n"
        )
        print(label3)
        write_cvs('',device['ip'],'EOFError','','')
        
    except (SSHException):
        label4 = (
            "\n##### SSH issue. Check if SSHv2 is enabled: " + device["ip"] + " #####\n"
        )
        print(label4)
        write_cvs('',device['ip'],'SSH Exceptions','','')

def write_cvs(hostname,ipaddr,interface,description,status):
    today = str(date.today())
    with open(f"BGP_Uptime_{today}.csv", "a", newline='') as csvfile:
        fieldnames = ['Hostname','IP_Address','Interface','Description','Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print (f"**************** Getting info from:  {hostname} ********************")
        writer.writerow({'Hostname': hostname, 
                         'IP_Address': ipaddr, 
                         'Interface': interface, 
                         'Description': description,
                         'Status': status})
    csvfile.close()
    print (f"'''''''''''''''''''' Success  {hostname} '''''''''''''''''''''")

def device_dict(ipaddr,myusername,mypass):
    device = {
        "device_type": "cisco_ios",
        "ip": ipaddr,
        "username": myusername,
        "password": mypass,
        "secret": mypass,
    }
    get_info(device)   


def main ():
    myusername = input("Enter your username: ")
    mypass = getpass.getpass()
  
    
    write_cvs('Hostname','IP_Address','IP_Neighbor','Uptime','Status')
    executor = ThreadPoolExecutor(max_workers=20)
    
    workbook = xlrd.open_workbook("Devices.xlsx")
    sheet = workbook.sheet_by_index(0)
    for index in range(1, sheet.nrows):
        ipaddr = sheet.row(index)[1].value
        interface = sheet.row(index)[2].value
        
        executor.submit(device_dict,ipaddr,myusername,mypass)
      

if __name__ == "__main__":
    main()