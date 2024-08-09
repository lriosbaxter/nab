#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""
import datetime
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



def get_interfaces_cdp (device,ipaddr):
    print (f"########## Connecting to Device {ipaddr} ############")
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        
        hname_cm = net_connect.send_command("sh run | in hostname",delay_factor=5)
        hnamelist = hname_cm.split()
        hostname = hnamelist[1]
       
        print (f"########## Connecting to Hostname {hostname} ############")
        
        cdp_neigh_cmd = net_connect.send_command("sh cdp neigh")
        
        if "sDL" in cdp_neigh_cmd:
            cdp_neigh = cdp_neigh_cmd.splitlines()
            for loop, cdp in enumerate(cdp_neigh):
                if cdp.startswith("sDL"):
                    neighbor = cdp
                    interface = cdp_neigh[loop+1]
                    #print(neighbor, interface)
                    distro_int = interface.split()
                    distro_int = convert(distro_int[0:2])
                    print(f"Connected to: {neighbor}   in {distro_int}")
        
        net_connect.disconnect()
    
          
    except (AuthenticationException):
        label2 = "\n##### Authentication failure: " + device["ip"] + " #####\n"
        print(label2)
    except (NetMikoTimeoutException):
        label2 = "\n##### Time out to device: " + device["ip"] + " #####\n"
        print(label2)
    except (EOFError):
        label3 = (
            "\n##### End of file while attempting device: " + device["ip"] + " #####\n"
        )
        print(label3)
    except (SSHException):
        label4 = (
            "\n##### SSH issue. Check if SSHv2 is enabled: " + device["ip"] + " #####\n"
        )
        print(label4)
        device_dict(ipaddr,'padrond','Dennyplz25')
    
    """
    except:
        print('Something wrong happened')
        #write_cvs(hostname,interface,descrip,stat,vlan,duplex,speed,type_p,'Something wrong happened')
    """
    
def convert_week (week):
    week = int(week)
    print (f"In here is {week} weekkkkkkkkkkkkkkk")
    return week

def convert(s): 
    str1 = " " 
    return(str1.join(s)) 
   
def write_cvs(hostname,neighbor,interface):
    #try:
    #date = datetime.datetime.now()
    with open(f"Interfaces_SW_.csv", "a", newline='') as csvfile:
        fieldnames = ['Device','Neighbor','Interface']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print (f"**************** Getting info from:  {interface} ********************")
        writer.writerow({'Device': hostname, 
                         'Neighbor': neighbor,
                         'Interface': interface})
    csvfile.close()
    print (f"'''''''''''''''''''' Success  {interface} '''''''''''''''''''''")
    #except:
    #    print ("There's a problem when writing")
               
def device_dict(ipaddr,myusername,mypass):
    device = {
        "device_type": "cisco_ios",
        "ip": ipaddr,
        "username": myusername,
        "password": mypass,
        "secret": mypass,
    }
    get_interfaces_cdp(device,ipaddr)   

def main ():
    myusername = input("Enter your username: ")
    mypass = getpass.getpass()
    ipaddr = input("Enter the IP Address: ")
  
    device_dict(ipaddr,myusername,mypass)
      

if __name__ == "__main__":
    main()
