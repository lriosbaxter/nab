#! /usr/bin/env python
""" 
    Script for modiying nodes from SW
    Copyright(c) 2022. PadronDenisse HermosilloHector Baxter
"""

import sys
from tools import NPMDevice


def main(foreign_arguments: dict):
    # setup swis params
    server_data_dictionary = NPMDevice.create_npm_dictionary(foreign_arguments)
    print(server_data_dictionary)
    swis_connection = NPMDevice.npm_connection(server_data_dictionary)
    print(swis_connection)
    swis_query = "SELECT Uri FROM Orion.Nodes WHERE IPAddress = @ip_addr"
    ipadd = ''

    # filter_by_ip_address = Device.npm_send_query(swis_connection, swis_query,
    #                                              ip_address)

    # Use as needed
    # uri = filter_by_ip_address['results'][0]['Uri']

    # obj = filter_by_ip_address.read(uri)
    # pprint.pprint(obj)


if __name__ == '__main__':
    foreign_arguments = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(foreign_arguments)
