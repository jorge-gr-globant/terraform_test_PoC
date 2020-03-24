#!/usr/bin/python
import subprocess
import re
import os

consul_env = {"CONSUL_HTTP_TOKEN": os.getenv('CONSUL_HTTP_TOKEN')}


def main():
    consul_list_cmd = ["consul", "acl", "token", "list"]
    output = subprocess.check_output(consul_list_cmd, env=consul_env)
    for chunk in output.split("\n\n"):
        values = {}
        for line in chunk.split("\n"):
            if line.strip() and not re.match("Policies", line) and not line.startswith(" "):
                k, v = re.split(":\s+", line)
                values[k] = v
        if values['Description'] not in ('Master Token', 'Anonymous Token'):
            subprocess.call(['consul', 'acl', 'token', 'delete', '-id', values['AccessorID']])


if __name__ == '__main__':
    main()
