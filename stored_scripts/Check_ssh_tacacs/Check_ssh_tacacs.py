#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.ssh_exception import (
    AuthenticationException,
    NetMikoTimeoutException,
    SSHException,
)
import getpass
import csv
import xlrd
import sys
from threading import Thread

def check_ssh_tacacs (device,ipaddr):
   
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        run = net_connect.send_command("sh run | in hostname")
        print (run)
        net_connect.disconnect()
        write_cvs(ipaddr,'yes','yes')
          
    except (AuthenticationException):
        label2 = f"\n##### Authentication failure: {ipaddr} #####\n"
        print(label2)
        write_cvs(ipaddr,'yes','no')
    except (NetMikoTimeoutException):
        label2 = f"\n##### Time out to device: {ipaddr} #####\n"
        print(label2)
        write_cvs(ipaddr,' ',' ')
    except (SSHException):
        label4 = (
            f"\n##### SSH issue. Check if SSHv2 is enabled: {ipaddr} #####\n"
        )
        print(label4)
        write_cvs(ipaddr,'no','no')
    except:
        label5 = (
            f"\n##### Something went wrong: {ipaddr} #####\n"
        )
        print(label5)
        write_cvs(ipaddr,' ',' ')
    

def write_cvs(ipaddr,ssh,tacacs):
    with open(f"Check_ssh_tacacs.csv", "a", newline='') as csvfile:
        fieldnames = ['IP','SSH','Tacacs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'IP': ipaddr, 
                         'SSH': ssh, 
                         'Tacacs': tacacs})
    csvfile.close()
    print (f"'''''''''''''''''''' Success  {ipaddr} '''''''''''''''''''''")
  
def device (ipaddr,myusername,mypass):
    device = {
        "device_type": "cisco_ios",
        "ip": ipaddr,
        "username": myusername,
        "password": mypass,
        "secret": mypass,
    }
    check_ssh_tacacs(device,ipaddr)
               
def main ():
    myusername = input("Enter your username: ")
    mypass = getpass.getpass()

    workbook = xlrd.open_workbook(r"Device list to Update-standardize configuration.xlsx")
    sheet = workbook.sheet_by_index(2)
    threads = []
    for index in range(1, sheet.nrows):
        ipaddr = sheet.row(index)[0].value
        device(ipaddr,myusername,mypass)
      
if __name__ == "__main__":
    main()
