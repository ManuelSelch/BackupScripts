import yaml
import os
from dotenv import load_dotenv

load_dotenv()
config_file = os.getenv('BORG_CONFIG_FILE', 'config.yaml')

default_config = {
    'source_directories': [],
    'repositories': [
        {
            'path': '/path/to/repository',
            'label': 'remote'
        }
    ],

    'before_backup': [],
    'after_backup': [],

    'keep_daily': 7,
    'keep_weekly': 4,
    'keep_monthly': 6,
    'read_special': True
}


def load_config():
    if not os.path.exists(config_file):
        print("Config not found, creating a new one with basic structure.")
        return default_config
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def save_config(config):
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f"Config updated at {config_file}")

def add_dir(config):
    dir = input("dir: ")
    if dir:
        config['source_directories'].append(dir)
        print(f"Directory {dir} added successfully.")
    else:
        print("Invalid input. No volume added.")

def add_volume(config):
    volume = input("Docker volume name (e.g., /var/lib/docker/volumes/<VOLUME>): ")
    if volume:
        volume_path = "/var/lib/docker/volumes/" + volume
        config['source_directories'].append(volume_path)
        print(f"Volume {volume_path} added successfully.")
    else:
        print("Invalid input. No volume added.")

def add_database(config):
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
    'add volume': add_volume,
    'add dir': add_dir,
    'add database': add_database,
    'edit repo': edit_repository,
    
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
