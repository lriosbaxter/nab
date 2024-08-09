#! /usr/bin/env python
""" 
    Script for modiying nodes from SW
    Copyright(c) 2022. PadronDenisse HermosilloHector Baxter
"""

import re
import sys
from tools import NPMDevice
from concurrent.futures import ThreadPoolExecutor
import xlrd


def add_node_snmp(
        swis_connection, props_node,
        props_node_cp):

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
        'N.VRFRouting.SNMP.MPLSVPNStandard': True,
        'N.AssetInventory.Snmp.Generic': True,
        'N.Topology_Layer3.SNMP.ipNetToMedia': True,
        'N.Routing.SNMP.Ipv4CidrRoutingTable': True,
        'N.HardwareHealthMonitoring.SNMP.NPM.Cisco': True,
        'N.VRFRouting.SNMP.CiscoVrfMib': True,
        'N.RoutingNeighbor.SNMP.OSPF': True,
        'N.RoutingNeighbor.SNMP.BGP': True,
        'N.EnergyWise.SNMP.Cisco': True,
        'N.MulticastRouting.SNMP.MulticastRoutingTable': True,
        'N.Topology_Vlans.SNMP.VtpVlan': True,
        'N.Topology_CDP.SNMP.cdpCacheTable': True,
        'N.Topology_PortsMap.SNMP.Dot1dBase': True,
        'N.Topology_Layer3_IpRouting.SNMP.ipCidrRouter': True,
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
    results = NPMDevice.npm_send_query(
        swis_connection,
        "SELECT node_id, Uri FROM Orion.Nodes WHERE IPAddress = @IPAddress",
        IPAddress=node_prop['IPAddress'])

    uri = results['results'][0]['Uri']

    NPMDevice.npm_update(swis_connection,
                         uri + '/CustomProperties',
                         **node_cp_prop)

    obj_cp = NPMDevice.npm_read(swis_connection,
                                uri + '/CustomProperties')

    node_id = results['results'][0]['node_id']
    node = f"N:{node_id}"

    hw_health = NPMDevice.npm_invoke(swis_connection,
                                     'Orion.HardwareHealth.HardwareInfo',
                                     'EnableHardwareHealth',
                                     node, 9)
    return node_id


def discover_interfaces(swis_connection, node_id):
    results = NPMDevice.npm_invoke(swis_connection,
                                   'Orion.NPM.Interfaces',
                                   'DiscoverInterfacesOnNode',
                                   node_id)

    interfaces = []
    for x in results['DiscoveredInterfaces']:

        if x['ifOperStatus'] == 1:

            inter_caption = x['Caption'].split()
            if 'Loopback' in x['Caption']:
                continue
            elif '.' in inter_caption[0]:
                if 'ca=' in x['Caption']:
                    interfaces.append(x)
                else:
                    continue
            elif 'ro=' in x['Caption']:
                interfaces.append(x)
            elif 'zscaler' in x['Caption'].lower():
                interfaces.append(x)
            elif 'tunnel_to' in x['Caption'].lower():
                interfaces.append(x)
            else:
                continue
        else:
            continue
    add_interfaces = NPMDevice.npm_invoke(swis_connection,
                                          'Orion.NPM.Interfaces',
                                          'AddInterfacesOnNode',
                                          node_id,
                                          interfaces,
                                          'AddDefaultPollers')
    print(add_interfaces)
    return add_interfaces


def main(foreign_arguments):
    server_data_dictionary = NPMDevice.create_npm_dictionary(foreign_arguments)
    swis_connection = NPMDevice.npm_connection(server_data_dictionary)
    executor = ThreadPoolExecutor(max_workers=4)
    workbook = xlrd.open_workbook("New_Devices.xlsx")
    sheet = workbook.sheet_by_index(1)
    for index in range(sheet.nrows):
        props_node = NPMDevice.create_props_node(sheet.row(index))
        props_node_cp = NPMDevice.create_props_node_cp(sheet.row(index))
        print(props_node_cp)
        node_id = executor.submit(add_node_snmp, swis_connection, props_node,
                                  props_node_cp)
        discover_interfaces(swis_connection, node_id)


if __name__ == '__main__':
    foreign_arguments = dict(
        [arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(foreign_arguments)
