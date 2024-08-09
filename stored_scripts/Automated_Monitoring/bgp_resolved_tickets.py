import re
import sys

from tools.netmiko_tools import Device


def main(
        args: dict) -> None:
    device_dictionary = Device.create_device_dictionary(args)
    device_connection = Device.connection(device_dictionary)
    if device_dictionary.get('device_type') == 'cisco_ios':
        filtered_bgp = filter_bgp(device_connection, f'sh bgp sum')
    else:
        filtered_bgp = filter_bgp(device_connection, f'sh ip bgp sum')
    interface_information = filter_interfaces(device_connection)
    complete_bgp_information = dict(ip=device_dictionary.get('ip'),
                                    bgp_config=filtered_bgp,
                                    unestablished_ip=args.get(
                                        'unestablished_ip'),
                                    carrier=interface_information.get(
                                        'carrier'))
    complete_ticket_filling(complete_bgp_information)
    exit()


def filter_bgp(
        device_ssh_connection, sh_bgp: str) -> list:
    bgp_sum_conf = device_ssh_connection.send_command(sh_bgp)
    if 'ip' in sh_bgp:
        return re.findall(r"BGP\scommunity[\w\W]*", bgp_sum_conf)
    else:
        return re.findall(r"BGP\sactivity[\w\W]*", bgp_sum_conf)


def filter_interfaces(
        device_ssh_connection) -> dict:
    int_desc_conf = device_ssh_connection.send_command('sh int desc')
    get_carrier = re.findall(r"ca=.[a-zA-Z]*", int_desc_conf)
    if len(get_carrier) < 1:
        get_carrier.append(' ')
        get_carrier = get_carrier[0].split(' ')[1]
    else:
        get_carrier = get_carrier[0].split('ca=')[1]
    ip_int_brief = device_ssh_connection.send_command('sh ip int brief')
    show_version = device_ssh_connection.send_command('sh ver | inc uptime')
    device_ssh_connection.disconnect()
    return {
        'device_uptime': show_version,
        'carrier': get_carrier,
        'int_brief': ip_int_brief
    }


def complete_ticket_filling(
        device_dict: dict) -> None:
    print(f"Device IP: {device_dict.get('ip')}\n\n"
          f"RFO: CR {device_dict.get('carrier')}\n\n"
          f"{device_dict.get('bgp_config')[0]}\n\n"
          f"UNE IP:{device_dict.get('unestablished_ip')}\n")


if __name__ == "__main__":
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
