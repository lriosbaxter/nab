
from tools.netmiko_tools import Device
import sys


def main(
        args: dict) -> None:
    device_dictionary = Device.create_device_dictionary(args)
    device_connection = Device.connection(device_dictionary)


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
