#!/bin/bash

# Update Homebrew
echo "Update Brew Formuales"
brew update

# Upgrade installed formulae
echo "Update apps installed via Homebrew"
brew upgrade

# Upgrade apps installed via mac app store
echo "Update apps installed via Mac App"
mas upgrade # Learn more here -> https://github.com/mas-cli/mas