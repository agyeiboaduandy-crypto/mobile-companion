#!/data/data/com.termux/files/usr/bin/bash

# GitHub Setup for Mobile Companion
# This script helps set up Git and SSH for pushing to GitHub.

echo "Setting up GitHub integration..."

# Configure Git
read -p "Enter your GitHub username: " git_user
read -p "Enter your GitHub email: " git_email

git config --global user.name "$git_user"
git config --global user.email "$git_email"

# SSH Key Setup
if [ ! -f "$HOME/.ssh/id_ed25519" ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -C "$git_email" -N "" -f "$HOME/.ssh/id_ed25519"
    echo "SSH key generated."
else
    echo "SSH key already exists."
fi

echo "--------------------------------------------------"
echo "Your public SSH key is below. Copy and add it to GitHub (Settings -> SSH and GPG keys):"
echo "--------------------------------------------------"
cat "$HOME/.ssh/id_ed25519.pub"
echo "--------------------------------------------------"
read -p "Press Enter once you have added the key to GitHub..."

# Test connection
ssh -T git@github.com
