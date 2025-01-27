#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
source "$SCRIPT_DIR/.env"
export BORG_PASSPHRASE=$BORG_PASSPHRASE

/usr/local/bin/borgmatic break-lock
/usr/local/bin/borgmatic -v 2
