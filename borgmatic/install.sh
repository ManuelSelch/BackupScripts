#!/bin/bash

# installation
sudo apt update
sudo apt install borgbackup

sudo apt install python3-pip
sudo pip3 install borgmatic

# maria-dump for database backups
sudo apt install mariadb-client

pip3 install -r ./$(dirname "$0")/requirements.txt