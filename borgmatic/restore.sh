#!/bin/bash

source ./$(dirname "$0")/.env
export BORG_PASSPHRASE=$BORG_PASSPHRASE

cd /
borgmatic break-lock
borgmatic extract --archive latest -v 2     