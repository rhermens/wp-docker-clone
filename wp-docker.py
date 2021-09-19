#!/usr/bin/env python

import argparse
from package import generation

def main(args):
    generation.create_folder_structure(args.destination)
    generation.create_docker_compose(args.destination)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean wordpress docker")
    parser.add_argument("destination", help="Project destination")
    main(parser.parse_args())
