#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
source "$SCRIPT_DIR/.env"

echo "Backup Mac Repo: $REPO_DIR"

echo "Backup Brewfile"
brew bundle dump --file="$REPO_DIR/Brewfile" --force

echo "Backup .zshrc"
ZSHRC_FILE="$HOME/.zshrc"
cp "$ZSHRC_FILE" "$REPO_DIR/.zshrc"

echo "Backup Borgmatic Config"
cp /etc/borgmatic/config.yaml "$REPO_DIR/config.yaml"

echo "Commit"
cd "$REPO_DIR"

if [[ -n $(git status -s) ]]; then
    echo "Commiting the changes to Github"
    git add .
    git commit -m "Backup task: $(date +'%Y-%m-%d %H:%M:%S')"
    git push
else
    echo "No changes to commit."
fi
