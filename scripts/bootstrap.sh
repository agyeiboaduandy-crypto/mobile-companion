#!/data/data/com.termux/files/usr/bin/bash

# Mobile Companion - One-Click Bootstrap
# Run this single script to set up your entire AI coding station.
# Usage: bash bootstrap.sh

set -e

INSTALL_DIR="$HOME/mobile-companion"

echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘     Mobile Companion - AI Coding Station        â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "This will create a full AI coding environment."
echo "Target directory: $INSTALL_DIR"
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
mkdir -p "$HOME/.config/ai-companion"

echo "[2/7] Writing setup script..."
cat > "$INSTALL_DIR/scripts/setup_termux.sh" << 'SETUP'
#!/data/data/com.termux/files/usr/bin/bash
echo "Starting Mobile Companion Setup..."
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
mkdir -p ~/.config/ai-companion
echo "--------------------------------------------------"
echo "Setup Complete!"
echo "Ensure Termux:API APK is installed from F-Droid."
echo "--------------------------------------------------"
SETUP

echo "[3/7] Writing API key manager..."
cat > "$INSTALL_DIR/scripts/manage_keys.sh" << 'KEYS'
#!/data/data/com.termux/files/usr/bin/bash
ENV_FILE="$HOME/.mobile-companion.env"
set_key() {
    local key_name=$1
    local key_value=$2
    if [ -f "$ENV_FILE" ]; then
        sed -i "s/^$key_name=.*/$key_name=$key_value/" "$ENV_FILE"
    else
        echo "$key_name=$key_value" >> "$ENV_FILE"
    fi
    echo "Set $key_name successfully."
    bash ~/mobile-companion/scripts/fetch_models.sh
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
cat > "$INSTALL_DIR/scripts/fetch_models.sh" << 'FETCH'
#!/data/data/com.termux/files/usr/bin/bash
ENV_FILE="$HOME/.mobile-companion.env"
MODELS_FILE="$HOME/.mobile-companion-models"
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
echo "--- Available Models ---" > "$MODELS_FILE"
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
FETCH

echo "[5/7] Writing GitHub setup script..."
cat > "$INSTALL_DIR/scripts/setup_github.sh" << 'GH'
#!/data/data/com.termux/files/usr/bin/bash
echo "Setting up GitHub integration..."
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

echo "[6/7] Writing shell config and aliases..."
cat > "$INSTALL_DIR/scripts/shell_config.sh" << 'ALIAS'
if [ -f "$HOME/.mobile-companion.env" ]; then
    export $(grep -v '^#' "$HOME/.mobile-companion.env" | xargs)
fi
alias ai-open='opencode'
alias ai-ollama='curl -X POST http://localhost:11434/api/generate -d'
alias ai-models='cat ~/.mobile-companion-models'
alias ai-update-models='bash ~/mobile-companion/scripts/fetch_models.sh'
alias ai-setup='bash ~/mobile-companion/scripts/setup_termux.sh'
alias ai-keys='bash ~/mobile-companion/scripts/manage_keys.sh'
alias ai-github='bash ~/mobile-companion/scripts/setup_github.sh'
echo "Mobile Companion AI aliases loaded."
ALIAS

echo "[7/7] Writing config files..."
cat > "$INSTALL_DIR/.env.example" << 'ENV'
GOOGLE_AI_STUDIO_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
NVIDIA_API_KEY=your_nvidia_api_key_here
OLLAMA_HOST=http://localhost:11434
ENV

cat > "$INSTALL_DIR/config/mcp_config.json" << 'MCP'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data/data/com.termux/files/home/mobile-companion"]
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

cat > "$INSTALL_DIR/docs/google-ai-studio.md" << 'G'
# Google AI Studio Setup
```bash
ai-keys set GOOGLE_AI_STUDIO_KEY your_key_here
```
G

cat > "$INSTALL_DIR/docs/groq.md" << 'GR'
# Groq Setup
```bash
ai-keys set GROQ_API_KEY your_key_here
```
GR

cat > "$INSTALL_DIR/docs/nvidia.md" << 'NV'
# NVIDIA Setup
```bash
ai-keys set NVIDIA_API_KEY your_key_here
```
NV

cat > "$INSTALL_DIR/docs/ollama.md" << 'OL'
# Ollama Setup
```bash
ai-keys set OLLAMA_HOST http://your-ollama-ip:11434
```
OL

# Make scripts executable
chmod +x "$INSTALL_DIR/scripts/"*.sh

# Source aliases
echo ""
echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘           BOOTSTRAP COMPLETE!                   â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "Next steps:"
echo "  1. Install dependencies:  ai-setup"
echo "  2. Set your API keys:     ai-keys set GOOGLE_AI_STUDIO_KEY sk-..."
echo "  3. Fetch available models: ai-models"
echo "  4. Setup GitHub:          ai-github"
echo "  5. Start coding:          ai-open"
echo ""
echo "Add this to your .zshrc or .bashrc:"
echo "  source ~/mobile-companion/scripts/shell_config.sh"
echo ""
