#! /usr/bin/env python
""" 
    Script for modiying nodes from SW
    Copyright(c) 2022. PadronDenisse HermosilloHector Baxter
"""

import sys
from tools import NPMDevice


def discover_interfaces(swis_connection, node_id):
    print("Discover and add interfaces:")
    invoke_npm_interfaces = NPMDevice.npm_invoke(swis_connection,
                                                 'Orion.NPM.Interfaces',
                                                 'DiscoverInterfacesOnNode',
                                                 node_id)
    print(invoke_npm_interfaces)
    interfaces = []
    """
    We will loop under the interfaces the device has and select the only ones 
    with "dn=" in the description, this means we'll select the standard ones.
    """
    for x in invoke_npm_interfaces['DiscoveredInterfaces']:
        if x['ifOperStatus'] == 1:
            if 'dn=' in x['Caption']:
                interfaces.append(x)
            else:
                continue
        else:
            continue
    print(interfaces)

    invoke_add_interfaces = NPMDevice.npm_invoke(swis_connection,
                                                 'Orion.NPM.Interfaces',
                                                 'AddInterfacesOnNode',
                                                 node_id,
                                                 interfaces,
                                                 'AddDefaultPollers')

    print(invoke_add_interfaces)


def main(foreign_arguments: dict):
    server_data_dictionary = NPMDevice.create_npm_dictionary(foreign_arguments)
    print(server_data_dictionary)
    swis_connection = NPMDevice.npm_connection(server_data_dictionary)
    print(swis_connection)
    swis_query = "SELECT Uri FROM Orion.Nodes WHERE IPAddress = @ip_addr"
    filter_by_ip_address = NPMDevice.npm_send_query(swis_connection,
                                                    swis_query,
                                                    ip_address='10.55.255.180')
    node_id = filter_by_ip_address['results'][0]['NodeID']
    print(node_id)
    discover_interfaces(swis_connection, node_id)


if __name__ == '__main__':
    foreign_arguments = dict(
        [arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(foreign_arguments)
