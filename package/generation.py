import os

def create_folder_structure(destination: str):
    path = os.path.expanduser(destination)

    if os.path.isdir(path):
        raise Exception("Project folder already exists")

    os.mkdir(path)
    os.mkdir(f"{path}/wp")
    os.mkdir(f"{path}/dump")

    return path

def create_docker_compose(path: str, db_user: str = "wp", db_pwd: str = "wp", db_name: str = "wp"):
    with open(os.path.join(os.path.dirname(__file__), './../boiler/docker-compose.yml')) as boilerplate:
        content = boilerplate.read()

    content = content.replace("$$DB_USER$$", db_user)
    content = content.replace("$$DB_PWD$$", db_pwd)
    content = content.replace("$$DB_NAME$$", db_name)

    with open(f"{os.path.expanduser(path)}/docker-compose.yml", "x") as composeFile:
        composeFile.write(content)

