#! /usr/bin/env python
""" 
    Script for modiying nodes from SW
    Copyright(c) 2022. PadronDenisse HermosilloHector Baxter
"""

import sys
from tools import NPMDevice


def main(foreign_arguments: dict):
    server_data_dictionary = NPMDevice.create_npm_dictionary(foreign_arguments)
    print(server_data_dictionary)
    swis_connection = NPMDevice.npm_connection(server_data_dictionary)
    ipadd = ''
    invoke_entity = 'Orion.HardwareHealth.HardwareInfo'
    invoke_verb = 'EnableHardwareHealth'
    arg_1 = 'N:372'
    arg_2 = 9
    print(swis_connection)
    result = NPMDevice.npm_invoke(swis_connection, invoke_entity, invoke_verb, arg_1, arg_2)
    # uri = results['results'][0]['Uri']

    # obj = swis.read(results)
    # pprint.pprint (obj)


if __name__ == '__main__':
    foreign_arguments = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(foreign_arguments)
