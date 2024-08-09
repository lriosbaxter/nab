import sys

from netmiko import ConnectHandler


def main(test_dictionary):
    connection = ConnectHandler(**test_dictionary)
    print(connection)
    run_conf = connection.send_command('sh run')
    print(run_conf)
    return run_conf


if __name__ == '__main__':
    args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])
    main(args)
