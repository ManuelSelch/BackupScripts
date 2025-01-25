#!/bin/bash

source ./$(dirname "$0")/.env

# Function to check if Homebrew is installed
install_homebrew() {
    if ! command -v brew &> /dev/null
    then
        echo "Homebrew not found, installing now..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed."
    fi
}

# Function to download Brewfile and run brew bundle
pull() {
    echo "Pull Updates..."
    git pull
}

copy_brewfile() {
    echo "Running brew bundle to install software..."
    brew bundle --file="$MAC_REPO_DIR/Brewfile"
}

# Function to copy .zshrc to the home directory
copy_zshrc() {
    echo "Backing up existing .zshrc to .zshrc.backup..."
    cp ~/.zshrc ~/.zshrc.backup

    echo "Copying new .zshrc to the home directory..."
    cp "$MAC_REPO_DIR/.zshrc" ~/
    echo ".zshrc copied successfully."
}

coopy_borgmatic() {
    sudo mkdir -p "/etc/borgmatic" && sudo cp "$MAC_REPO_DIR/config.yaml" "/etc/borgmatic/config.yaml"
    sudo chown -R $USER:  /etc/borgmatic
}

# Main Script Execution
cd "$MAC_REPO_DIR"
install_homebrew
pull

copy_brewfile
copy_zshrc
coopy_borgmatic

echo "Restore complete"
