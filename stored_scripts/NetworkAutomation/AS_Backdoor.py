#! /usr/bin/env python
""" 
    Script for getting info of devices
    Copyright(c) 2020. PadronDenisse Baxter
"""

from concurrent.futures import ThreadPoolExecutor
import csv
import xlrd
import sys

from tools import Device


def get_info_as(device_connection, ipaddr, city, country, site_id):
    hname_cm = device_connection.send_command("sh run | in hostname")
    hnamelist = hname_cm.split()
    hostname = hnamelist[1]
    print(hostname)
    backdoor = device_connection.send_command("sh run | i router bgp|backdoor")
    as_number = backdoor.split()
    backdoor = convert(as_number)
    print(backdoor)
    as_value = as_number[2]
    print(as_value)

    # Send the values to write_cvs
    write_cvs(hostname, ipaddr, city, country, site_id, backdoor, as_value)
    # End connection
    device_connection.disconnect()


def convert(s):
    str1 = " "
    return str1.join(s)


def write_cvs(hostname, ipaddr, city, country, site_id, backdoor, as_value):
    with open(f"AS_Global.csv", "a", newline='') as csvfile:
        fieldnames = ['Caption', 'IP_Adress', 'City', 'Country', 'SiteID',
                      'AS', 'Backdoor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Caption': hostname,
                         'IP_Adress': ipaddr,
                         'City': city,
                         'Country': country,
                         'SiteID': site_id,
                         'AS': as_value,
                         'Backdoor': backdoor})
    # Close file
    csvfile.close()
    print(f"'''''''''''''''''''' Success  {ipaddr} '''''''''''''''''''''")


def main(args: dict):
    device_dictionary = Device.create_device_dictionary(args)
    device_connection = Device.connection(device_dictionary)

    # Columns we need in the final file
    write_cvs('Caption', 'IP_Adress', 'City', 'Country', 'SiteID', 'AS',
              'Backdoor')

    # File we use
    executor = ThreadPoolExecutor(max_workers=10)

    workbook = xlrd.open_workbook(r"Devices.xlsx")
    sheet = workbook.sheet_by_index(1)

    for index in range(1, sheet.nrows):
        caption = sheet.row(index)[0].value
        ipaddr = sheet.row(index)[1].value
        city = sheet.row(index)[2].value
        country = sheet.row(index)[3].value
        siteID = sheet.row(index)[6].value

        executor.submit(get_info_as, device_connection, ipaddr, city, country,
                        siteID)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
