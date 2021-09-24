import re
import os
from getpass import getpass

class Config():
    remote: bool
    db: bool

    protocol: int = None
    host: str
    user: str
    pwd: str
    directory: str

    db_from_wp: bool = None
    db_host: str
    db_user: str
    db_pwd: str
    db_name: str

    def __init__(self, remote = False, db = False):
        self.remote = remote
        self.db = db

    def ask_input(self):
        if (self.remote):
            while(self.protocol == None):
                protocol = int(input("Enter a number (1: SFTP): "))

                if (protocol == 1):
                    self.protocol = protocol

            self.host = input("Host: ")
            self.user = input("User: ")
            self.pwd = getpass("Password: ")
            self.directory = input("Remote directory: ")

        if (self.db):
            if (self.remote == False):
                self.db_from_wp = False
            while(self.db_from_wp == None):
                db_from_wp = input("Take database configuration from wp-config? [y/n]: ")

                if (db_from_wp == 'y' or db_from_wp == 'n'):
                    self.db_from_wp = True if db_from_wp == 'y' else False

            if (self.db_from_wp == False):
                self.db_host = input("MySQL Host: ")
                self.db_user = input("MySQL User: ")
                self.db_pwd = getpass("MySQL Password: ")
                self.db_name = input("MySQL Database name: ")

    def db_from_wp_config(self, path: str):
        wp_config = self.parse_wp_config(path)

        if wp_config['DB_HOST'] == 'localhost' or wp_config['DB_HOST'] == '127.0.0.1':
            self.db_host = self.host
        else:
            self.db_host = wp_config['DB_HOST']

        self.db_user = wp_config['DB_USER']
        self.db_pwd = wp_config['DB_PASSWORD']
        self.db_name = wp_config['DB_NAME']

    def parse_wp_config(self, wp_config: str):
        parsedConfig = {}
        with open(wp_config, "r") as config:
            for definition in re.findall("define\((.*?)\);", config.read()):
                split = re.findall("[\'\"`](.*?)[\'\"`]", definition)[:2]
                parsedConfig[split[0]] = split[1] if len(split) > 1 else None

        return parsedConfig
