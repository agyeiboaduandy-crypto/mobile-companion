#!/bin/bash
# ============================================================
# OWURA - Uninstaller
# ============================================================

echo ""
echo "OWURA Uninstaller"
echo "=================="
echo ""

read -p "Are you sure you want to uninstall OWURA? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "Cancelled."
    exit 0
fi

echo "Removing OWURA..."

# Remove installation directory
rm -rf "$HOME/.owura"

# Remove command
rm -f "$HOME/.local/bin/owura"
rm -f /usr/local/bin/owura

# Remove from PATH in bashrc
if [ -f "$HOME/.bashrc" ]; then
    sed -i '/# OWURA - AI Coding Agent/d' "$HOME/.bashrc"
    sed -i '/export PATH="\$HOME\/.local\/bin:\$PATH"/d' "$HOME/.bashrc"
fi

# Remove from zshrc
if [ -f "$HOME/.zshrc" ]; then
    sed -i '/# OWURA - AI Coding Agent/d' "$HOME/.zshrc"
    sed -i '/export PATH="\$HOME\/.local\/bin:\$PATH"/d' "$HOME/.zshrc"
fi

echo ""
echo "OWURA has been uninstalled."
echo "Your API keys and memory have been preserved in ~/.owura/"
echo "To remove completely: rm -rf ~/.owura"
echo ""
