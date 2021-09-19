#!/usr/bin/env python

import os
import re
import subprocess
import pysftp
import re
import argparse
from getpass import getpass
from package import generation

def sftp_clone(dest: str, config: dict):
    sftp = pysftp.Connection(config["host"], config["user"], password = config["pwd"])

    with sftp.cd(config["directory"]):
        sftp.get_r('.', dest)

    sftp.close()

def parse_wp_config(source_path: str):
    parsedConfig = {}
    with open(f"{source_path}/wp-config.php", "r") as config:
        for definition in re.findall("define\((.*?)\);", config.read()):
            split = re.findall("[\'\"`](.*?)[\'\"`]", definition)[:2]
            parsedConfig[split[0]] = split[1] if len(split) > 1 else None

    return parsedConfig

def main(args):
    dest = generation.create_folder_structure(args.destination)

    sftp_config = {
        "host": input("SFTP Host: "),
        "user": input("SFTP User: "),
        "pwd": getpass("SFTP Password: "),
        "directory": input("SFTP Remote directory: ")
    }
    sftp_clone(f"{dest}/wp", sftp_config)

    wp_config = parse_wp_config(f"{dest}/wp")
    if wp_config['DB_HOST'] == 'localhost' or wp_config['DB_HOST'] == '127.0.0.1':
        db_host = sftp_config["host"]
    else:
        db_host = wp_config['DB_HOST']
    os.remove(f"{dest}/wp/wp-config.php")

    try:
        subprocess.run(f"mysqldump -h {db_host} -u {wp_config['DB_USER']} -p{wp_config['DB_PASSWORD']} {wp_config['DB_NAME']} > {dest}/dump/{wp_config['DB_NAME']}.sql", shell=True)
    except Exception as e:
        print("Could not dump database.")
        print(f"Dump your database into: {dest}/dump")

    generation.create_docker_compose(dest, wp_config["DB_USER"], wp_config["DB_PASSWORD"], wp_config["DB_NAME"])

    print("Happy hacking!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean wordpress docker")
    parser.add_argument("destination", help="Project destination")
    main(parser.parse_args())
