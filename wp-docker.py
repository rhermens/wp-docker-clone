#!/usr/bin/env python

import argparse
import os
from package import generation, remote
from package.config import Config

def main(args):
    if (args.remote or args.db):
        config = Config(args.remote, args.db)
        config.ask_input()

    generation.create_folder_structure(args.destination)

    if (args.remote):
        if (config.protocol == 1):
            remote.sftp_clone(f"{args.destination}/wp", config)
        if (config.db_from_wp == True):
            config.db_from_wp_config(f"{args.destination}/wp/wp-config.php")
        os.remove(f"{args.destination}/wp/wp-config.php")

    if (args.db):
        remote.mysql_dump(args.destination, config)

    generation.create_docker_compose(args.destination)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create WordPress docker env")
    parser.add_argument("destination", help="Project destination")
    parser.add_argument("--remote", action="store_true", help="Clone remote (S)FTP WordPress")
    parser.add_argument("--db", action="store_true", help="Dump MySQL db")
    main(parser.parse_args())
