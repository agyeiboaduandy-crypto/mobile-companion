#!/data/data/com.termux/files/usr/bin/bash

# OWURA - Bootstrap Installer
# One-click setup for your AI coding station

set -e

INSTALL_DIR="$HOME/owura"

echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘         OWURA - AI Coding Agent                 â•‘"
echo "â•‘         Code Anywhere. Anytime.                 â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "This will create your AI coding environment."
echo "Target: $INSTALL_DIR"
echo ""

read -p "Continue? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "[1/7] Creating directory structure..."
mkdir -p "$INSTALL_DIR/scripts"
mkdir -p "$INSTALL_DIR/config"
mkdir -p "$INSTALL_DIR/docs"
mkdir -p "$HOME/.config/owura"

echo "[2/7] Writing core scripts..."
cat > "$INSTALL_DIR/scripts/setup.sh" << 'SETUP'
#!/data/data/com.termux/files/usr/bin/bash
echo "Starting OWURA Setup..."
echo "[1/5] Updating packages..."
pkg update -y && pkg upgrade -y
echo "[2/5] Installing core dependencies..."
pkg install -y nodejs python git curl wget zsh jq openssh
echo "[3/5] Installing AI Coding Assistants..."
npm install -g opencode || echo "opencode installation failed."
pkg install -y curl
echo "[4/5] Checking Termux:API..."
pkg install -y termux-api || echo "Termux:API package failed."
echo "[5/5] Finalizing..."
mkdir -p ~/.config/owura
echo "--------------------------------------------------"
echo "OWURA Setup Complete!"
echo "Ensure Termux:API APK is installed from F-Droid."
echo "--------------------------------------------------"
SETUP

echo "[3/7] Writing key manager..."
cat > "$INSTALL_DIR/scripts/keys.sh" << 'KEYS'
#!/data/data/com.termux/files/usr/bin/bash
ENV_FILE="$HOME/.owura.env"
set_key() {
    local key_name=$1
    local key_value=$2
    if [ -f "$ENV_FILE" ]; then
        sed -i "s/^$key_name=.*/$key_name=$key_value/" "$ENV_FILE"
    else
        echo "$key_name=$key_value" >> "$ENV_FILE"
    fi
    echo "Set $key_name successfully."
    bash ~/owura/scripts/models.sh
}
show_keys() {
    if [ -f "$ENV_FILE" ]; then
        cat "$ENV_FILE"
    else
        echo "No keys set yet."
    fi
}
case "$1" in
    set) set_key "$2" "$3" ;;
    list) show_keys ;;
    *) echo "Usage: $0 {set key_name value | list}" ;;
esac
KEYS

echo "[4/7] Writing model fetcher..."
cat > "$INSTALL_DIR/scripts/models.sh" << 'MODELS'
#!/data/data/com.termux/files/usr/bin/bash
ENV_FILE="$HOME/.owura.env"
MODELS_FILE="$HOME/.owura-models"
fetch_google() {
    local key=$(grep "GOOGLE_AI_STUDIO_KEY=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)
    if [ -n "$key" ]; then
        echo "Fetching Google AI Studio models..."
        curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$key" | jq -r '.models[].name' | sed 's/^models\//' > "$MODELS_FILE.google"
    fi
}
fetch_groq() {
    local key=$(grep "GROQ_API_KEY=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)
    if [ -n "$key" ]; then
        echo "Fetching Groq models..."
        curl -s -H "Authorization: Bearer $key" "https://api.groq.com/openai/v1/models" | jq -r '.data[].id' > "$MODELS_FILE.groq"
    fi
}
fetch_nvidia() {
    local key=$(grep "NVIDIA_API_KEY=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)
    if [ -n "$key" ]; then
        echo "Fetching NVIDIA models..."
        curl -s -H "Authorization: Bearer $key" "https://api.nvidia.com/v1/models" | jq -r '.data[].id' > "$MODELS_FILE.nvidia"
    fi
}
fetch_ollama() {
    local host=$(grep "OLLAMA_HOST=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)
    if [ -n "$host" ]; then
        echo "Fetching Ollama models..."
        curl -s "$host/api/tags" | jq -r '.models[].name' > "$MODELS_FILE.ollama"
    fi
}
fetch_google
fetch_groq
fetch_nvidia
fetch_ollama
echo "--- OWURA Available Models ---" > "$MODELS_FILE"
echo "[Google AI Studio]" >> "$MODELS_FILE"
cat "$MODELS_FILE.google" 2>/dev/null >> "$MODELS_FILE"
echo "" >> "$MODELS_FILE"
echo "[Groq]" >> "$MODELS_FILE"
cat "$MODELS_FILE.groq" 2>/dev/null >> "$MODELS_FILE"
echo "" >> "$MODELS_FILE"
echo "[NVIDIA]" >> "$MODELS_FILE"
cat "$MODELS_FILE.nvidia" 2>/dev/null >> "$MODELS_FILE"
echo "" >> "$MODELS_FILE"
echo "[Ollama]" >> "$MODELS_FILE"
cat "$MODELS_FILE.ollama" 2>/dev/null >> "$MODELS_FILE"
rm -f "$MODELS_FILE".*
echo "Models updated in $MODELS_FILE"
cat "$MODELS_FILE"
MODELS

echo "[5/7] Writing GitHub setup..."
cat > "$INSTALL_DIR/scripts/github.sh" << 'GH'
#!/data/data/com.termux/files/usr/bin/bash
echo "Setting up GitHub for OWURA..."
read -p "Enter your GitHub username: " git_user
read -p "Enter your GitHub email: " git_email
git config --global user.name "$git_user"
git config --global user.email "$git_email"
if [ ! -f "$HOME/.ssh/id_ed25519" ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -C "$git_email" -N "" -f "$HOME/.ssh/id_ed25519"
fi
echo "--------------------------------------------------"
echo "Your public SSH key (copy and add to GitHub):"
echo "--------------------------------------------------"
cat "$HOME/.ssh/id_ed25519.pub"
echo "--------------------------------------------------"
read -p "Press Enter once you have added the key to GitHub..."
ssh -T git@github.com
GH

echo "[6/7] Writing shell config..."
cat > "$INSTALL_DIR/scripts/config.sh" << 'CONFIG'
if [ -f "$HOME/.owura.env" ]; then
    export $(grep -v '^#' "$HOME/.owura.env" | xargs)
fi
alias owura='bash ~/owura/scripts/owura-agent.sh'
alias owura-setup='bash ~/owura/scripts/setup.sh'
alias owura-keys='bash ~/owura/scripts/keys.sh'
alias owura-models='cat ~/.owura-models'
alias owura-update-models='bash ~/owura/scripts/models.sh'
alias owura-github='bash ~/owura/scripts/github.sh'
alias owura-open='bash ~/owura/scripts/owura-agent.sh'
echo "OWURA aliases loaded. Type 'owura' to start."
CONFIG


cat > "$INSTALL_DIR/scripts/owura.sh" << 'OWURA'
#!/data/data/com.termux/files/usr/bin/bash
echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘         OWURA - AI Coding Agent                 â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "  1. Setup     - Install dependencies"
echo "  2. Keys      - Manage API keys"
echo "  3. Models    - View available models"
echo "  4. Open      - Launch opencode"
echo "  5. GitHub    - Configure git"
echo "  6. Update    - Refresh models"
echo "  0. Exit"
echo ""
read -p "Select option: " choice
case $choice in
    1) bash ~/owura/scripts/setup.sh ;;
    2) bash ~/owura/scripts/keys.sh ;;
    3) cat ~/.owura-models ;;
    4) opencode ;;
    5) bash ~/owura/scripts/github.sh ;;
    6) bash ~/owura/scripts/models.sh ;;
    0) exit ;;
    *) echo "Invalid option" ;;
esac
OWURA

echo "[7/7] Writing config files..."
cat > "$INSTALL_DIR/.env.example" << 'ENV'
GOOGLE_AI_STUDIO_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
NVIDIA_API_KEY=your_nvidia_api_key_here
OLLAMA_HOST=http://localhost:11434
ENV

cat > "$INSTALL_DIR/config/mcp.json" << 'MCP'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data/data/com.termux/files/home/owura"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  },
  "skills": []
}
MCP

chmod +x "$INSTALL_DIR/scripts/"*.sh

echo ""
echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘           OWURA IS READY!                       â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "Next steps:"
echo "  1. Install deps:   owura-setup"
echo "  2. Set API keys:   owura-keys set GOOGLE_AI_STUDIO_KEY sk-..."
echo "  3. Fetch models:   owura-update-models"
echo "  4. Start coding:   owura"
echo ""
echo "Add this to your .zshrc or .bashrc:"
echo "  source ~/owura/scripts/config.sh"
echo ""
