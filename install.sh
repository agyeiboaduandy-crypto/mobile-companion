#!/bin/bash
# ============================================================
# OWURA - One-Click Installer
# AI Coding Agent for Mobile Terminal
# ============================================================
set -e

REPO="agyeiboaduandy-crypto/owura"
INSTALL_DIR="$HOME/.owura"
BIN_DIR="$HOME/.local/bin"
PYTHON_MIN="3.8"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "  ___   _   _  _   _  ___   ___ "
    echo " / _ \ | | | || | | | / _ \ / _ \\"
    echo "| | | || | | || | | || | | | (_) |"
    echo "| |_| || |_| || |_| || |_| | \__, |"
    echo " \___/  \__, | \___/  \___/    /_/"
    echo "         __/ |                    "
    echo "        |___/                     "
    echo -e "${NC}"
    echo -e "${GREEN}AI Coding Agent - Code Anywhere. Anytime.${NC}"
    echo ""
}

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON=python3
    elif command -v python &> /dev/null; then
        PYTHON=python
    else
        echo -e "${YELLOW}Python 3 not found. Installing...${NC}"
        install_python
        PYTHON=python3
    fi
    
    # Check version
    VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo -e "${GREEN}Python ${VERSION} found${NC}"
}

install_python() {
    if command -v pkg &> /dev/null; then
        # Termux
        pkg update -y
        pkg install -y python
    elif command -v apt &> /dev/null; then
        # Debian/Ubuntu
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif command -v brew &> /dev/null; then
        # macOS
        brew install python
    elif command -v pacman &> /dev/null; then
        # Arch
        sudo pacman -S python python-pip
    elif command -v dnf &> /dev/null; then
        # Fedora
        sudo dnf install python3 python3-pip
    else
        echo -e "${RED}Cannot install Python automatically.${NC}"
        echo "Please install Python 3.8+ manually:"
        echo "  https://www.python.org/downloads/"
        exit 1
    fi
}

install_owura() {
    echo -e "${CYAN}Installing OWURA...${NC}"
    
    # Create directories
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    
    # Download OWURA
    echo -e "${YELLOW}Downloading files...${NC}"
    if command -v git &> /dev/null; then
        git clone "https://github.com/$REPO.git" "$INSTALL_DIR" 2>/dev/null || {
            echo "Git clone failed, using curl..."
            download_with_curl
        }
    else
        download_with_curl
    fi
    
    # Install dependencies
    echo -e "${YELLOW}Installing dependencies...${NC}"
    cd "$INSTALL_DIR"
    $PYTHON -m pip install -r requirements.txt --quiet --user 2>/dev/null || \
    $PYTHON -m pip install -r requirements.txt --quiet 2>/dev/null || {
        echo -e "${YELLOW}pip install had issues, trying with --break-system-packages...${NC}"
        $PYTHON -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null || true
    }
    
    # Create command
    create_command
    
    echo -e "${GREEN}Installation complete!${NC}"
}

download_with_curl() {
    curl -sL "https://github.com/$REPO/archive/main.tar.gz" | tar xz -C "$INSTALL_DIR" --strip-components=1
}

create_command() {
    cat > "$BIN_DIR/owura" << 'COMMAND'
#!/bin/bash
# OWURA launcher
PYTHON=""
for cmd in python3 python; do
    if command -v $cmd &> /dev/null; then
        PYTHON=$cmd
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Error: Python not found"
    exit 1
fi

exec $PYTHON "$HOME/.owura/owura/app.py" "$@"
COMMAND
    chmod +x "$BIN_DIR/owura"
    
    # Add to PATH if needed
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo "" >> "$HOME/.bashrc"
        echo "# OWURA - AI Coding Agent" >> "$HOME/.bashrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        
        echo "" >> "$HOME/.zshrc" 2>/dev/null || true
        echo "# OWURA - AI Coding Agent" >> "$HOME/.zshrc" 2>/dev/null || true
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
        
        export PATH="$BIN_DIR:$PATH"
    fi
    
    # Try to create symlink
    ln -sf "$BIN_DIR/owura" /usr/local/bin/owura 2>/dev/null || true
}

print_success() {
    echo ""
    echo -e "${GREEN}â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—${NC}"
    echo -e "${GREEN}â•‘  OWURA Installed Successfully!           â•‘${NC}"
    echo -e "${GREEN}â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•${NC}"
    echo ""
    echo -e "${CYAN}To start OWURA:${NC}"
    echo "  source ~/.bashrc  # or restart terminal"
    echo "  owura"
    echo ""
    echo -e "${CYAN}First run will ask for your API key.${NC}"
    echo -e "${CYAN}Get a free Gemini key at: https://aistudio.google.com/apikey${NC}"
    echo ""
}

# Main
print_banner
check_python
install_owura
print_success
