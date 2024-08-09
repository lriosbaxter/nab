import re
import sys

from tools.netmiko_tools import Device


def main(external_arguments: dict):
    device_dictionary = Device.create_device_dictionary(external_arguments)
    device_connection = Device.connection(device_dictionary)
    print(device_connection)
    complete_ticket_filling(device_connection)


def complete_ticket_filling(device_connection):
    print(device_connection.send_command("sh env all"))

    # print(f"RFO", device_dictionary)


if __name__ == "__main__":
    external_arguments = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(external_arguments)
