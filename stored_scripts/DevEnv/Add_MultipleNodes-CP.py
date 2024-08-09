#! /usr/bin/env python
""" 
    Script for modiying nodes from SW
    Copyright(c) 2022. PadronDenisse HermosilloHector Baxter
"""

import sys
from tools import NPMDevice
import re
from concurrent.futures import ThreadPoolExecutor
import xlrd


def add_node(swis_connection, props_node, props_node_cp):
    node_prop = NPMDevice.create_dict_from_properties(props_node)
    node_cp_prop = NPMDevice.create_dict_from_properties(props_node_cp)

    results = NPMDevice.npm_create(swis_connection,
                                   'Orion.Nodes',
                                   **node_prop)

    node_id = re.search(r'(\d+)$', results).group(0)

    pollers_enabled = {
        'N.Status.ICMP.Native': True,
        'N.Status.SNMP.Native': False,
        'N.ResponseTime.ICMP.Native': True,
        'N.ResponseTime.SNMP.Native': False,
        'N.Details.SNMP.Generic': True,
        'N.Uptime.SNMP.Generic': True,
        'N.Cpu.SNMP.HrProcessorLoad': True,
        'N.Memory.SNMP.NetSnmpReal': True,
        'N.AssetInventory.Snmp.Generic': True,
        'N.Topology_Layer3.SNMP.ipNetToMedia': True,
        'N.Routing.SNMP.Ipv4CidrRoutingTable': True,
        'N.HardwareHealthMonitoring.SNMP.NPM.Cisco': True,
    }

    pollers = []
    for k in pollers_enabled:
        pollers.append(
            {
                'PollerType': k,
                'NetObject': 'N:' + node_id,
                'NetObjectType': 'N',
                'NetObjectID': node_id,
                'Enabled': pollers_enabled[k]
            }
        )

    for poller in pollers:
        response = NPMDevice.npm_create(swis_connection,
                                        'Orion.Pollers',
                                        **poller)
    results = NPMDevice.npm_send_query(swis_connection,
                                       "SELECT node_id, Uri "
                                       "FROM "
                                       "Orion.Nodes "
                                       "WHERE IPAddress = @IPAddress",
                                       IPAddress=node_prop['IPAddress'])
    # Use as needed
    uri = results['results'][0]['Uri']

    NPMDevice.npm_update(uri + '/CustomProperties', **node_cp_prop)
    obj_cp = NPMDevice.npm_read(uri + '/CustomProperties')


def main(foreign_arguments: dict):
    server_data_dictionary = NPMDevice.create_npm_dictionary(foreign_arguments)
    print(server_data_dictionary)
    swis_connection = NPMDevice.npm_connection(server_data_dictionary)
    print(swis_connection)
    executor = ThreadPoolExecutor(max_workers=4)

    # Read the excel file to get the IP of the devices
    workbook = xlrd.open_workbook("New_Devices.xlsx")
    sheet = workbook.sheet_by_index(1)
    for index in range(sheet.nrows):
        props_node = NPMDevice.create_props_node(sheet.row(index))
        props_node_cp = NPMDevice.create_props_node_cp(sheet.row(index))
        print(props_node_cp)
        # Call the "connection" function and send the arguments given
        executor.submit(add_node, swis_connection, props_node, props_node_cp)


if __name__ == '__main__':
    foreign_arguments = dict(
        [arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(foreign_arguments)
