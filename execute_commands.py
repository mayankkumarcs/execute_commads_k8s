import argparse
import json
import os
import re
import subprocess
import sys

kubeconfig_path = ''

pwd = os.path.join(os.path.dirname(os.path.realpath(__file__)))
output_dir = os.path.join(pwd, 'client_version_1_20_0_server_version_1_18_19')

# Initialize the Parser
parser = argparse.ArgumentParser(
    description='Test Kubectl class methods sanity')

# Adding Arguments
parser.add_argument('-f', '--kube-config', metavar='`Update` kubeconfig file',
                    dest='kubeconfig_path', action='store', required=True)

def stringify(value):
    if isinstance(value, bytes):
        stringified_value = value.decode()
    else:
        stringified_value = str(value)
    return stringified_value

def value_path():
    with open(os.path.join(pwd, 'commands_without_parameter'), 'r') as f:
        output = f.read()
    return output.splitlines()

def write_output(output, file_name):
    f = open(os.path.join(output_dir, file_name), 'w')
    output = f.writelines(output)
    f.close()

def execute(cmd_string, sudo=False, env=None,
            current_working_directory=None):
    command = subprocess.run(cmd_string, capture_output=True)
    cmd_output = command.stdout.decode("utf-8")
    cmd_error = sys.stderr.buffer.write(command.stderr)
    return stringify(cmd_output), stringify(cmd_error)

def main():
    arg = parser.parse_args()
    kubeconfig_path = arg.kubeconfig_path
    kubeconfig_path = kubeconfig_path or os.path.expanduser('~/.kube/config')
    command_list = value_path()
    for command in command_list:
        final_command = ['kubectl', '--kubeconfig', kubeconfig_path, '--request-timeout','120s']
        final_command.extend(command.split())
        command_output, err = execute(final_command)
        write_output(command_output, command)

if __name__ == '__main__':
    main()
