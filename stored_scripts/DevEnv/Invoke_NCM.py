#! /usr/bin/env python
""" 
    Script for modiying nodes from SW
    Copyright(c) 2022. PadronDenisse HermosilloHector Baxter
"""

import sys
from tools import NPMDevice
import xlrd


def get_node(swis_connection, ip_address):
    results = NPMDevice.npm_send_query(swis_connection,
                                       "SELECT node_id, Uri "
                                       "FROM Orion.Nodes "
                                       "WHERE IPAddress = @IPAddress",
                                       IPAddress=ip_address)
    node_id = results['results'][0]['NodeID']
    print(node_id)
    invoke_cirrus_nodes = NPMDevice.npm_invoke(swis_connection,
                                               'Cirrus.Nodes',
                                               'AddNodeToNCM',
                                               node_id)
    print(invoke_cirrus_nodes)


def main(foreign_arguments):
    server_data_dictionary = NPMDevice.create_npm_dictionary(foreign_arguments)
    print(server_data_dictionary)
    swis_connection = NPMDevice.npm_connection(server_data_dictionary)
    print(swis_connection)
    workbook = xlrd.open_workbook("New_Devices.xlsx")
    sheet = workbook.sheet_by_index(1)
    for index in range(sheet.nrows):
        ip_address = sheet.row(index)[1].value
        get_node(swis_connection, ip_address)


if __name__ == '__main__':
    foreign_arguments = dict(
        [arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(foreign_arguments)
