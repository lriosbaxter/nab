from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect

from netmiko.exceptions import (
    AuthenticationException,
    NetMikoTimeoutException,
    SSHException,
)


class Device:
    @classmethod
    def create_device_dictionary(cls,
                                 request_data: dict) -> dict:
        return {
            "device_type": request_data.get('device_type'),
            "ip": request_data.get('ip_address'),
            "username": request_data.get('username'),
            "password": request_data.get('password'),
            "secret": request_data.get('password'),
        }

    @classmethod
    def create_device_dictionary_from_params(cls,
                                             device_os: str, ip_address: str,
                                             username: str, password: str) -> dict:
        return {
            "device_type": device_os,
            "ip": ip_address,
            "username": username,
            "password": password,
            "secret": password,
        }
    @classmethod
    def create_jumpserver_dictionary_from_params(cls,
                                                 ip_address: str, username: str,
                                                 password: str) -> dict:
        return {
            "device_type": "terminal_server",
            "ip": ip_address,
            "username": username,
            "password": password,
            "secret": password,
            "port": 22
        }

    @classmethod
    def connection(cls,
                   device: dict):
        try:
            net_connect = ConnectHandler(**device)
            return net_connect

        except AuthenticationException:
            failure = {
                "type": "authentication",
                "ip_address": device["ip"],
            }
            return failure
        except NetMikoTimeoutException:
            failure = {
                "type": "time_out",
                "ip_address": device["ip"],
            }
            return failure
        except EOFError:
            failure = {
                "type": "end_of_file",
                "ip_address": device["ip"],
            }
            return failure
        except SSHException:
            failure = {
                "type": "ssh_issue",
                "ip_address": device["ip"],
            }
            return failure

    @classmethod
    def detect_device_os(cls,
                         device: dict) -> dict:
        os_detect = SSHDetect(**device)
        best_os_match = os_detect.autodetect()
        device['device_type'] = best_os_match
        return device
