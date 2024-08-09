#! /usr/bin/env python
""" 
    Script to get the devices with BGP configured
    Copyright (c) 2023. PadronDenisse
"""

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
       
def connection_jump_server(ip_jumpserver,myusername,mypass,ipaddr):
    device = {
        "device_type": "terminal_server",
        "ip": ip_jumpserver,
        "username": myusername,
        "password": mypass,
        "port": 22
    }

    net_connect = ConnectHandler(**device)
        
    print(f"Jump server prompt:{net_connect.find_prompt()}")
           
    print(ipaddr)
    #ipaddr = 
    ping = net_connect.write_channel(f"ssh-keygen -R {ipaddr}\n")
    ping = net_connect.write_channel(f"ssh -l padrond {ipaddr}\n")
    time.sleep(10)
    connection = net_connect.read_channel()
       
    print (connection)
    if 'password' in connection:
        net_connect.write_channel("Dennyplz25.\n")
        
    elif '(yes/no)' in connection:
        net_connect.write_channel("yes\n")
        time.sleep(8)
        net_connect.write_channel("Dennyplz25.\n")
        print(f"Device prompt: {net_connect.find_prompt()}")
        
    elif 'Connection refused' in connection:
        net_connect.disconnect()
  

    try:
        redispatch(net_connect, device_type = 'cisco_ios')
        print(f"Device prompt: {net_connect.find_prompt()}")
 
        hostname = net_connect.find_prompt()
        hostname = hostname[:-1]
        
        print (hostname)
        bgp_summary = net_connect.send_command("sh bgp summary")
        if '% BGP not active' in bgp_summary:
            write_cvs(hostname,device['ip'],'No')
        elif 'State/PfxRcd' in bgp_summary:
            write_cvs(hostname,device['ip'],'Yes')
        else:
            write_cvs(hostname,device['ip'],bgp_summary)
        #net_connect.write_channel("exit\n")
            
        print (f"'''''''''''''''''''' Success  {hostname} '''''''''''''''''''''")
        net_connect.disconnect()
    
          
    except (AuthenticationException):
        label2 = "\n##### Authentication failure: " + device["ip"] + " #####\n"
        print(label2)
        write_cvs('',device['ip'],'AuthenticationException')
       
    except (NetMikoTimeoutException):
        label2 = "\n##### Time out to device: " + device["ip"] + " #####\n"
        write_cvs('',device['ip'],'NetmikoIssue')
    except (EOFError):
        label3 = (
            "\n##### End of file while attempting device: " + device["ip"] + " #####\n"
        )
        print(label3)
        write_cvs('',device['ip'],'EOFError')
        
    except (SSHException):
        label4 = (
            "\n##### SSH issue. Check if SSHv2 is enabled: " + device["ip"] + " #####\n"
        )
        print(label4)
        write_cvs('',device['ip'],'SSH Exceptions')
    

def write_cvs(hostname,ipaddr,bgp_conf):
    today = str(date.today())
    with open(f"BGP_Uptime_{today}.csv", "a", newline='') as csvfile:
        fieldnames = ['Hostname','IP_Address','BGP_Configured']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print (f"**************** Getting info from:  {hostname} ********************")
        writer.writerow({'Hostname': hostname, 
                         'IP_Address': ipaddr, 
                         'BGP_Configured': bgp_conf})
    csvfile.close()
    print (f"'''''''''''''''''''' Success  {hostname} '''''''''''''''''''''")

        
def main ():
    #myusername = input("Enter your TACACS username: ")
    #password = getpass.getpass()
    ip_jumpserver = input("Enter the IP Address Jumpserver: ")
    #ip_jumpserver = '10.119.3.119'
    myusername= 'padrond'
    mypass = 'Overcooked.80k'
    
    write_cvs('Hostname','IP_Address','BGP_Configured')
    executor = ThreadPoolExecutor(max_workers=20)
    
    workbook = xlrd.open_workbook("Devices.xlsx")
    sheet = workbook.sheet_by_index(1)
    for index in range(1, sheet.nrows):
        ipaddr = sheet.row(index)[1].value
        
        executor.submit(connection_jump_server,ip_jumpserver,myusername,mypass,ipaddr)
    
    

if __name__ == "__main__":
    main()