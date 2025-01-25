#!/bin/bash

source ./$(dirname "$0")/.env

# Backup Brewfile
brew bundle dump --file="$REPO_DIR/Brewfile" --force
cp "$DATA_DIR/Brewfile" "$REPO_DIR/Brewfile"

# Backup .zshrc
ZSHRC_FILE="$HOME/.zshrc"
cp "$ZSHRC_FILE" "$REPO_DIR/.zshrc"

# Backup Borgmatic
cp /etc/borgmatic/config.yaml "$REPO_DIR/config.yaml"

# Commit
cd "$REPO_DIR"

if [[ -n $(git status -s) ]]; then
    echo "Commiting the changes to Github"
    git add .
    git commit -m "Backup task: $(date +'%Y-%m-%d %H:%M:%S')"
    git push
else
    echo "No changes to commit."
fi