#!/bin/bash

source ./$(dirname "$0")/.env
export BORG_PASSPHRASE=$BORG_PASSPHRASE

borgmatic break-lock
borgmatic -v 2