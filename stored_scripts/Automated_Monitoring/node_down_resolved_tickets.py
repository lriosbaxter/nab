import sys

from tools.netmiko_tools import Device


def main(external_arguments: dict):
    device_dictionary = Device.create_device_dictionary(external_arguments)
    device_connection = Device.connection(device_dictionary)
    if device_dictionary.get('device_type') == 'cisco_ios':
        filtered_uptime = device_connection.send_command(f'sh ver | inc uptime')
        reload_reason = device_connection.send_command(f'sh ver | inc reason')
        reload_type = device_connection.send_command(f'sh ver | inc type')
    else:
        filtered_uptime = device_connection.send_command(f'sh ver | inc uptime')
        reload_reason = device_connection.send_command(f'sh ver | inc reason')
        reload_type = device_connection.send_command(f'sh ver | inc type')

    print(filtered_uptime)
    print(reload_type)
    print(reload_reason)


def select_rfo(uptime, reason):
    return "RFO"


def complete_ticket_filling(filling_dictionary):
    print(f"RFO {filling_dictionary.get('rfo')}", )


if __name__ == "__main__":
    external_arguments = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(external_arguments)
