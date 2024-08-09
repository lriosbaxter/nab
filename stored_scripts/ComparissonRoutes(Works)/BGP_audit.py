#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""
from datetime import datetime
from threading import Thread
from netmiko import Netmiko
from netmiko.ssh_exception import (
    SSHException,
    AuthenticationException,
    NetMikoTimeoutException,
)
import os
import xlrd
import getpass
import pandas as pd
import csv

startTime = datetime.now()

threads = []

#This is the file we use for the script
workbook = xlrd.open_workbook(r"Bax_Routers.xlsx")
sheet = workbook.sheet_by_index(0)

#Username and password for accessing
myusername = input("Enter your username: ")
mypass = getpass.getpass()
    
def getinfo(hostname,ipaddr,myusername,mypass,num,router):
    try:
        switch = {
            "host": ipaddr,
            "username": myusername,
            "password": mypass,
            "device_type": "cisco_ios",
            "secret": mypass,
        }
        
        print(
            "'''''''''''Connecting to %s" %hostname + " %s" %router + " device '''''''''''''' \n"
        )
        net_connect = Netmiko(**switch)
        net_connect.enable()
        net_connect.send_command("terminal len 0")
        #To get the name of the device, in case the file doesnt have it
        host = net_connect.send_command("sh run | in hostname")
        host_r = host.split()
        hostname_r = host_r[1]
        print(
        "----------Getting info from %s" % hostname + " %s" %router + "-------------------\n"
        )
        try:
            
            neigh = net_connect.send_command("sh ip bgp summa | in %i" %num)
            # Split the string so we can get an specific number/char
            neigh = neigh.split()
            bgp_neigh = neigh[0]
            adver = net_connect.send_command("sh ip bgp neig %s" %bgp_neigh + " advertised-routes | in Total")
            # Split the string so we can get an specific number/char
            total = adver.split()
            total_pack = total [4]
        except:
            total_pack = "Other ASN"
            net_connect.disconnect()
        print(
            "***********Disconnecting from %s" % hostname + " %s" %router + "*****************\n"
        )

        net_connect.disconnect()
        return total_pack,hostname_r

    except (AuthenticationException):
        label2=ipaddr + "     Fail    Auth_error\n"
        print (label2)
        total_pack = label2
        hostname_r = "ERROR"
        return total_pack,hostname_r
            
    except (NetMikoTimeoutException):
        label3=ipaddr + "     Fail    Timeout\n"
        print (label3)
        total_pack = label3
        hostname_r = "ERROR"
        return total_pack,hostname_r
            
    except (EOFError):
        label4=ipaddr + "     Fail    EOFError\n"
        print (label4)
        total_pack = label4
        hostname_r = "ERROR"
        return total_pack,hostname_r
            
    except (SSHException):
        label5=ipaddr + ";" + "     Fail    SSH_error\n"
        print (label5)
        total_pack = label5
        hostname_r = "ERROR"
        return total_pack,hostname_r
            
#Open txt    
foutput = open("Output.txt", "w")
#Write the name of the columns
foutput.write("Site; Hostname R1; IP Adress R1; Routes; Hostname R2; IP Adress R2; Routes; Match")

#This simplify the writing on our script
def write (hostname,hostr_1,r1,prefix_r1,hostr_2,r2,prefix_r2,match):
    foutput.write(hostname + " ;")
    foutput.write(hostr_1 + " ;")
    foutput.write(r1 + " ;")
    foutput.write( prefix_r1 + " ;")
    foutput.write(hostr_2 + " ;")
    foutput.write( r2 + " ;" )
    foutput.write(prefix_r2 + " ;")
    foutput.write(match + ";\n" ) 
    
def main (myusername,mypass,hostname,r1,r2):
    #First router
    prefix_r1,hostr_1 = getinfo(hostname,r1,myusername,mypass,65000,"primary")
    #Sencond router
    prefix_r2,hostr_2 = getinfo(hostname,r2,myusername,mypass,64617,"secondary")
    
    #If the number of routes are equal it writes YES on match
    if prefix_r1 == prefix_r2:
        write(hostname,hostr_1,r1,prefix_r1,hostr_2,r2,prefix_r2,"YES")
    
    #Else it enter into another condition
    else:
        #Neither of the routes don't have leyend "Other ASN" enter into another condition
        if prefix_r1 != "Other ASN" and prefix_r2 != "Other ASN":
            #If any of the hostnames is ERROR, match is going to be ERROR
            #And the hostname will have the type of error
            if hostr_1 == "ERROR" or hostr_2 == "ERROR":
                write(hostname,hostr_1,r1,prefix_r1,hostr_2,r2,prefix_r2,"ERROR")
            #If not, it will write NO because the routes doesn´t match
            else:
                write(hostname,hostr_1,r1,prefix_r1,hostr_2,r2,prefix_r2,"NO")
        #The devicce can have Another ASN
        else:
             write(hostname,hostr_1,r1,prefix_r1,hostr_2,r2,prefix_r2,"***")
        

#Determine the values of the file
for index in range(1, sheet.nrows):
    hostname = sheet.row(index)[0].value
    r1 = sheet.row(index)[1].value
    r2 = sheet.row(index)[2].value
    hostname = str(hostname)
    
    t = Thread(target=main, args=(myusername, mypass, hostname, r1, r2))
    t.start()
    threads.append(t)

# wait for all threads to completed
for t in threads:
    t.join()

#we close the txt
foutput.close()

# Convert txt into csv
in_filename = ('Output.txt')
out_filename = ('Output.csv')
df = pd.read_csv(in_filename, sep=";")
df.to_csv(out_filename, index=False)

print("\nTotal execution time:")
print(datetime.now() - startTime)
print("\n########## Success ############")
