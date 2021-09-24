import pysftp
import subprocess
from package.config import Config

def sftp_clone(dest: str, config: Config):
    sftp = pysftp.Connection(config.host, config.user, password = config.pwd)

    with sftp.cd(config.directory):
        sftp.get_r('.', dest)

    sftp.close()

def mysql_dump(dest: str, config: Config):
    try:
        subprocess.run(f"mysqldump -h {config.db_host} -u {config.db_user} -p{config.db_pwd} {config.db_name} > {dest}/dump/{config.db_name}.sql", shell=True)
    except Exception as e:
        print("Could not dump database.")
        print(f"Dump your database into: {dest}/dump")
