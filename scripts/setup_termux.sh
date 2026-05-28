#!/data/data/com.termux/files/usr/bin/bash

# Mobile Companion Termux Setup Script
# This script installs the necessary runtimes and tools for AI coding assistants.

echo "Starting Mobile Companion Setup..."

# Update packages
echo "[1/5] Updating packages..."
pkg update -y && pkg upgrade -y

# Install core dependencies
echo "[2/5] Installing core dependencies (Node.js, Python, Git, etc.)..."
pkg install -y nodejs python git curl wget zsh jq openssh

# Install AI Coding Assistants
echo "[3/5] Installing AI Coding Assistants..."

# Install opencode (if it supports the requested providers)
echo "Installing opencode..."
npm install -g opencode || echo "opencode installation failed."

# Install Ollama (if on Android/Termux, this usually requires a specific setup or remote host)
echo "Setting up Ollama configuration..."
# Note: Ollama usually runs as a server. We ensure curl is available to interact with it.
pkg install -y curl


# Setup Termux:API (Remind user to install the APK)
echo "[4/5] Checking Termux:API..."
pkg install -y termux-api || echo "Termux:API package failed to install."

# Finalizing configuration
echo "[5/5] Finalizing configuration..."
mkdir -p ~/.config/ai-companion

echo "--------------------------------------------------"
echo "Setup Complete!"
echo "Please ensure you have installed the Termux:API APK from F-Droid."
echo "You can now run 'claude' or 'opencode' to start."
echo "--------------------------------------------------"
