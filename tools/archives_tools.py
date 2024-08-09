import re
import subprocess


class ArchiveTools:
    @classmethod
    def archive_search(cls, folder_name, archive_name, device_data):
        device_type = device_data.get('device_type')
        ip = device_data.get('ip')
        username = device_data.get('username')
        password = device_data.get('password')
        secret = device_data.get('secret')
        if "unestablished_ip_address" in device_data.keys():
            unestablished_ip = device_data.get('unestablished_ip_address')
            process = subprocess.Popen(
                f"python stored_scripts/{folder_name}/{archive_name}"
                f" device_type={device_type} ip_address={ip}"
                f" username={username} password={password} secret={secret}"
                f" unestablished_ip={unestablished_ip}", shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(
                f"python stored_scripts/{folder_name}/{archive_name}"
                f" device_type={device_type} ip_address={ip}"
                f" username={username} password={password} secret={secret}",
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode('utf-8'))
        return stdout.decode('utf-8')
