#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
source "$SCRIPT_DIR/.env"
export BORG_PASSPHRASE=$BORG_PASSPHRASE

borgmatic break-lock
borgmatic -v 2