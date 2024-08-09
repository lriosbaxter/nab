#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2021. PadronDenisse Baxter
"""
import datetime
from netmiko import ConnectHandler
from netmiko import redispatch
from netmiko.ssh_exception import (
    AuthenticationException,
    NetMikoTimeoutException,
    SSHException,
)
import getpass
import csv
import xlrd
import sys
import re
import time
       
def bootlines_config (device):
    print ("########## Connecting to Device " + device["ip"] + " ############")
    #Try to do a connection, if there's an error the except fuctions will help us to identify the kind of error we get
    try:
        #Connect to the device into enable mode
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        
        #Find the prompt to get the hostname of the device
        hostname = net_connect.find_prompt()
        #Remove the # from the prompt
        hostname = hostname[:-1]
        
        #Create an empty list
        cmd_lines = []
        
        print (f"########## Connecting to Hostname {hostname} ############")
        
        #Send sh run | in boot command to get the bootlines
        bootlines = net_connect.send_command("sh run | in boot")
        bootlines = bootlines.splitlines()
        
        #Loop on bootlines to get the boot system lines
        for boot in bootlines:
            if boot.startswith("boot sys"):
                #Add the negated boot system line
                cmd_lines.append(f"no {boot}")
            else:
                continue
        
        #If cmd_lines is empty do noting
        if cmd_lines == []:
            print ("There's noting to do")
            saved = 'no'
        else:
            #Send the configuration
            send_config = net_connect.send_config_set(cmd_lines)
            print(send_config)
            print(cmd_lines)
            
            #Save configuration
            net_connect.send_command("wr")
            saved = 'yes'
            
        #Send variables to write_cvs() in order to create a report
        write_cvs(hostname,ipaddr,cmd_lines,saved)
        
        
        #Dissconnect from the device
        net_connect.disconnect()
        print (f"--------- Disconnecting from Hostname {hostname} ---------")        

    #Credentials provides are not valid
    except (AuthenticationException):
        label2 = "\n##### Authentication failure: " + device["ip"] + " #####\n"
        print(label2)

    #There's a timeout, it device can be behind a firewall
    except (NetMikoTimeoutException):
        label2 = "\n##### Time out to device: " + device["ip"] + " #####\n"
        print(label2)

    #There was an error when tying to reach the file
    except (EOFError):
        label3 = (
            "\n##### End of file while attempting device: " + device["ip"] + " #####\n"
        )
        print(label3)

    #SSH is not enabled
    except (SSHException):
        label4 = (
            "\n##### SSH issue. Check if SSHv2 is enabled: " + device["ip"] + " #####\n"
        )
        print(label4)
    
    #There was another error not listed
    except:
        print ("There's an error in where")


def write_cvs(hostname,ipaddr,cmd_lines,saved):
    #If the file exist will opened, if not will be created
    with open(f"Bootlines_devices.csv", "a", newline='') as csvfile:
        fieldnames = ['Hostname','IP_Address','Config_sent','Saved']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print (f"**************** Getting info from:  {hostname} ********************")
        #Will write the information by row
        writer.writerow({'Hostname': hostname, 
                         'IP_Address': ipaddr,
                         'Config_sent': cmd_lines, 
                         'Saved': saved})
    #Close file
    csvfile.close()
    print (f"'''''''''''''''''''' Success  {hostname} '''''''''''''''''''''")

 
def device_dict(ipaddr,myusername,mypass):
    #This dictionary is needed in order to use Netmiko connecion
    device = {
        "device_type": "cisco_ios",
        "ip": ipaddr,
        "username": myusername,
        "password": mypass,
        "secret": mypass,
        
    }
    #Send dictionary to bootlines_config()
    bootlines_config(device)   


def main ():
    #Main function. Terminal will ask for TACACS+ username and password in order to connect to the devices
    myusername = input("Enter your username: ")
    mypass = getpass.getpass()
    
    #Write the hearders to the csv file
    write_cvs('Hostname','IP_Address','Config_sent','Saved')
    
    #Read the inventory file where is store the list of devices that will be impacted by the script
    workbook = xlrd.open_workbook(r"Devices.xlsx")
    sheet = workbook.sheet_by_index(0)
    for index in range(1, sheet.nrows):
        ipaddr = sheet.row(index)[1].value
        #Send the variables needed to device_dict()
        device_dict(ipaddr,myusername,mypass)

if __name__ == "__main__":
    main()