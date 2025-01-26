#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
source "$SCRIPT_DIR/.env"
export BORG_PASSPHRASE=$BORG_PASSPHRASE

cd /
borgmatic break-lock
borgmatic extract --archive latest -v 2     