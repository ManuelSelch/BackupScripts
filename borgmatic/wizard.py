import yaml
import os
from dotenv import load_dotenv
from paramiko import SSHClient, AutoAddPolicy, Ed25519Key
from scp import SCPClient

load_dotenv()
config_file = os.getenv('BORG_CONFIG_FILE', 'config.yaml')
scp: SCPClient = None

default_config = {
    'source_directories': [],
    'repositories': [
        {
            'path': '/path/to/repository',
            'label': 'remote'
        }
    ],

    'mariadb_databases': [],

    'before_backup': [],
    'after_backup': [],

    'keep_daily': 7,
    'keep_weekly': 4,
    'keep_monthly': 6,

    'archive_name_format': 'backup-{now}',
    'relocated_repo_access_is_ok': True,
    'files_cache': 'ctime,size',
    'read_special': True,
    'one_file_system': True,
    'compression': 'lz4'
}


def load_config():
    if not os.path.exists(config_file):
        print("Config not found, creating a new one with basic structure.")
        return default_config
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def load_local_config(config):
    global scp
    with open(config_file, 'r') as f:
        localConfig = yaml.safe_load(f)
        config.update(localConfig)
    scp = None
    print("Loaded local config")

def load_remote_config(config):
    global scp
    ssh = SSHClient()
    
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.load_system_host_keys()
    key_path = os.path.expanduser("~/.ssh/id_ed25519")
    private_key = Ed25519Key.from_private_key_file(key_path)

    host = input("host: ")
    ssh.connect(host, username="manuel", pkey=private_key)

    scp = SCPClient(ssh.get_transport())
    scp.get(remote_path="/etc/borgmatic/config.yaml", local_path="config.yaml")
    with open("config.yaml", 'r') as f:
        remoteConfig = yaml.safe_load(f)
        config.update(remoteConfig)

    print("Loaded remote config")
    pass

def save_config(config):
    if scp is None:
        save_local_config(config)
    else:
        save_remote_config(config)
   

def save_local_config(config):
    os.makedirs("/etc/borgmatic", exist_ok=True)
    with open(config_file, 'w+') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print("Saved local")

def save_remote_config(config):
    global scp
    with open("config.yaml", 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    scp.put("config.yaml", "/etc/borgmatic/config.yaml")
    print("Saved remote")

def add_dir(config):
    dir = input("dir: ")
    if dir:
        config['source_directories'].append(dir)
        print(f"Directory {dir} added successfully.")
    else:
        print("Invalid input. No volume added.")

def add_docker_volume(config):
    volume = input("Docker volume name (e.g., /var/lib/docker/volumes/<VOLUME>): ")
    if volume:
        volume_path = "/var/lib/docker/volumes/" + volume
        config['source_directories'].append(volume_path)
        print(f"Volume {volume_path} added successfully.")
    else:
        print("Invalid input. No volume added.")

def add_docker_database(config):
    container = input("container: ")
    user = input("user: ")
    password = input("password: ")
    database = input("database: ")
    
    dump_file = container + "_" + database + ".sql"
    
    cmd_dump = "docker exec "+container+" mysqldump -u "+user+" -p"+password+" "+database+" > "+dump_file
    cmd_cleanup = "rm " + dump_file


    if 'before_backup' not in config.keys():
        config['before_backup'] = []
    if 'after_backup' not in config.keys():
        config['after_backup'] = []

    config['before_backup'].append(cmd_dump)
    config['source_directories'].append(dump_file)
    config['after_backup'].append(cmd_cleanup)


def add_database(config):
    if 'mariadb_databases' not in config.keys():
        config['mariadb_databases'] = []

    database = input("database: ")
    user = input("user: ")
    password = input("password: ")

    config['mariadb_databases'].append({
        'name': database,
        'hostname': '127.0.0.1',
        'port': 3306,
        'username': user,
        'password': password
    })

def edit_repository(config):
    repo = input("Repository: ")
    if repo:
        config['repositories'][0]['path'] = repo
    else:
        print("Invalid input. No repository added.")

def view_config(config):
   print(yaml.dump(config, default_flow_style=False, sort_keys=False))

def show_help(config):
    for command_name in COMMANDS:
        print(f"- {command_name}")


COMMANDS = {
    'add docker volume': add_docker_volume,
    'add docker database': add_docker_database,
    'add dir': add_dir,
    'add database': add_database,
    
    'repo': edit_repository,
    
    'local': load_local_config,
    'remote': load_remote_config,

    'view': view_config,
    'save': save_config,

    'help': show_help,
    'exit': None, 
}

def main():
    config = load_config()

    while True:
        choice = input("\n> ").strip().lower()
        if choice in COMMANDS:
            if COMMANDS[choice]:
                COMMANDS[choice](config)
            else:
                print("Exiting the wizard.")
                return
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
