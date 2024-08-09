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
from concurrent.futures import ThreadPoolExecutor


def get_info_BW (device,ipaddr):
    print (f"########## Connecting to Device {ipaddr} ############")
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        print (f"*********** Getting info from {ipaddr} **************")
        #Get hostname
        hname_cm = net_connect.send_command("sh run | in hostname")
        hnamelist = hname_cm.split()
        hostname = hnamelist[1]
        #Get interfaces
        interface = net_connect.send_command("sh int descrip")
        interf = interface.splitlines()
        #Get interface description
        for i in interf:
            inter = i.split()
            if inter[1] == 'admin' or inter[0] == 'Interface':
                continue
            else:
                try:
                    descrip = inter[3:len(inter)]
                    descrip = convert(descrip)
                            
                except:
                    descrip = ' '
                          
                write_cvs(hostname,ipaddr,inter[0],descrip)
        
        print (f"'''''''''''''''''''' Success  {ipaddr} '''''''''''''''''''''")
        #End connection with device  
        net_connect.disconnect()
	
    except (AuthenticationException):
        #Auth failure
        label1 = "\n##### Authentication failure: " + device["ip"] + " #####\n"
        print(label1)
        write_cvs('',ipaddr,'Authentication failure','Cant connect')
    except (NetMikoTimeoutException):
        #Timeout error
        label2 = "\n##### Time out to device: " + device["ip"] + " #####\n"
        print(label2)
        write_cvs('',ipaddr,'Time out','Cant connect')
    except (EOFError):
        #File Error
        label3 = "\n##### End of file while attempting device: " + device["ip"] + " #####\n"
        print(label3)
        write_cvs('',ipaddr,'End of file','Cant connect')
    except (SSHException):
        #SSH error
        label4 = "\n##### SSH issue. Check if SSHv2 is enabled: " + device["ip"] + " #####\n"
        print(label4)
        write_cvs('',ipaddr,'SSH issue','Cant connect')
    except:
        #Error
        label5 = "\n##### Something happened: " + device["ip"] + " #####\n"
        print(label5)
        write_cvs('',ipaddr,'Something went wrong','Error')
    
def convert(s): 
    str1 = " " 
    return(str1.join(s)) 
   
def write_cvs(hostname,ipaddr,interface,description):
    #Write info in the final file
    with open(f"Devices_description.csv", "a", newline='') as csvfile:
        fieldnames = ['Hostname','IP_Adress','Interface','Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Hostname':hostname,
                         'IP_Adress':ipaddr,
                         'Interface':interface,
                         'Description':description})
    #Close file
    csvfile.close()
    
               
def device_dict(ipaddr,myusername,mypass):
    #dictionario of the device
    device = {
        "device_type": "cisco_ios",
        "ip": ipaddr,
        "username": myusername,
        "password": mypass,
        "secret": mypass,
    }
    #Send the values to get_info_AS 
    get_info_BW(device,ipaddr)   

def main ():
    myusername = input("Enter your username: ")
    mypass = getpass.getpass()
    #Columns we need in the final file
    write_cvs('Hostname','IP_Adress','Interface','Description')
    
    #File we use
    workbook = xlrd.open_workbook(r"Devices.xlsx")
    sheet = workbook.sheet_by_index(0)
    executor = ThreadPoolExecutor(max_workers=15)
    
    #We loop through the rows of the file
    for index in range(1, sheet.nrows):
        #Set every column of the file
        ipaddr = sheet.row(index)[1].value
        executor.submit(device_dict,ipaddr,myusername,mypass)

if __name__ == "__main__":
    main()
