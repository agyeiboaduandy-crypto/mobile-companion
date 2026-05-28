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
    echo "    â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
    echo "    â•‘       â–ˆâ–ˆ      â–ˆâ–ˆ â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ     â•‘"
    echo "    â•‘       â–ˆâ–ˆ      â–ˆâ–ˆ â–ˆâ–ˆ      â–ˆâ–ˆ          â•‘"
    echo "    â•‘       â–ˆâ–ˆ      â–ˆâ–ˆ â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆâ–ˆâ–ˆ       â•‘"
    echo "    â•‘       â–ˆâ–ˆ      â–ˆâ–ˆ      â–ˆâ–ˆ â–ˆâ–ˆ          â•‘"
    echo "    â•‘       â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ â–ˆâ–ˆ â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ     â•‘"
    echo "    â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
    echo -e "${NC}"
    echo -e "${GREEN}  AI Coding Agent - Code Anywhere. Anytime.${NC}"
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
    
    VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "unknown")
    echo -e "${GREEN}Python ${VERSION} found${NC}"
}

install_python() {
    if command -v pkg &> /dev/null; then
        pkg update -y
        pkg install -y python
    elif command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif command -v brew &> /dev/null; then
        brew install python
    else
        echo -e "${RED}Cannot install Python automatically.${NC}"
        echo "Please install Python 3.8+ manually"
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
        rm -rf "$INSTALL_DIR" 2>/dev/null || true
        git clone "https://github.com/$REPO.git" "$INSTALL_DIR" 2>/dev/null || download_with_curl
    else
        download_with_curl
    fi
    
    # Install dependencies
    echo -e "${YELLOW}Installing dependencies...${NC}"
    cd "$INSTALL_DIR"
    
    # Try multiple pip install methods
    $PYTHON -m pip install -r requirements.txt --quiet --user 2>/dev/null && echo "pip install succeeded" || \
    $PYTHON -m pip install -r requirements.txt --quiet 2>/dev/null && echo "pip install succeeded" || \
    $PYTHON -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null && echo "pip install succeeded" || \
    echo -e "${YELLOW}Warning: pip install had issues, OWURA may still work${NC}"
    
    # Create the command
    create_command
    
    echo -e "${GREEN}Installation complete!${NC}"
}

download_with_curl() {
    rm -rf "$INSTALL_DIR" 2>/dev/null || true
    mkdir -p "$INSTALL_DIR"
    curl -sL "https://github.com/$REPO/archive/main.tar.gz" | tar xz -C "$HOME" --strip-components=1
    # Move to correct location if needed
    if [ ! -f "$INSTALL_DIR/owura/app.py" ]; then
        mv "$HOME/owura" "$INSTALL_DIR" 2>/dev/null || true
    fi
}

create_command() {
    # Method 1: Create in $PREFIX/bin (Termux standard)
    if [ -d "$PREFIX/bin" ]; then
        cat > "$PREFIX/bin/owura" << 'COMMAND'
#!/bin/bash
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
        chmod +x "$PREFIX/bin/owura"
        echo -e "${GREEN}Command installed to $PREFIX/bin/owura${NC}"
    fi
    
    # Method 2: Create in ~/.local/bin (backup)
    cat > "$BIN_DIR/owura" << 'COMMAND'
#!/bin/bash
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
    echo -e "${GREEN}Command installed to $BIN_DIR/owura${NC}"
    
    # Method 3: Create in /usr/local/bin (backup)
    mkdir -p /usr/local/bin 2>/dev/null || true
    ln -sf "$BIN_DIR/owura" /usr/local/bin/owura 2>/dev/null || true
    
    # Update PATH in bashrc
    update_path
    
    # Export for current session
    export PATH="$BIN_DIR:$PREFIX/bin:$PATH"
    
    # Verify installation
    verify_installation
}

update_path() {
    # Remove old entries first
    sed -i '/# OWURA - AI Coding Agent/d' "$HOME/.bashrc" 2>/dev/null || true
    sed -i '/export PATH.*owura/d' "$HOME/.bashrc" 2>/dev/null || true
    
    # Add fresh entry
    echo "" >> "$HOME/.bashrc"
    echo "# OWURA - AI Coding Agent" >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    
    # Also update .profile for login shells
    if [ -f "$HOME/.profile" ]; then
        sed -i '/# OWURA - AI Coding Agent/d' "$HOME/.profile" 2>/dev/null || true
        echo "" >> "$HOME/.profile"
        echo "# OWURA - AI Coding Agent" >> "$HOME/.profile"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
    fi
    
    echo -e "${GREEN}PATH updated in ~/.bashrc${NC}"
}

verify_installation() {
    echo ""
    echo -e "${CYAN}Verifying installation...${NC}"
    
    # Check if command exists
    if command -v owura &> /dev/null; then
        echo -e "${GREEN}âœ“ 'owura' command found in PATH${NC}"
    else
        echo -e "${YELLOW}! 'owura' not in PATH yet, will work after: source ~/.bashrc${NC}"
    fi
    
    # Check if app.py exists
    if [ -f "$INSTALL_DIR/owura/app.py" ]; then
        echo -e "${GREEN}âœ“ Application files installed${NC}"
    else
        echo -e "${RED}âœ— Application files missing${NC}"
    fi
    
    # Check if requirements are installed
    if $PYTHON -c "import rich" 2>/dev/null; then
        echo -e "${GREEN}âœ“ Dependencies installed${NC}"
    else
        echo -e "${YELLOW}! Some dependencies may be missing${NC}"
    fi
}

print_success() {
    echo ""
    echo -e "${GREEN}â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—${NC}"
    echo -e "${GREEN}â•‘     OWURA Installed Successfully!            â•‘${NC}"
    echo -e "${GREEN}â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•${NC}"
    echo ""
    echo -e "${CYAN}To start OWURA:${NC}"
    echo ""
    echo "  Option 1 (recommended):"
    echo "    source ~/.bashrc"
    echo "    owura"
    echo ""
    echo "  Option 2 (if above doesn't work):"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "    owura"
    echo ""
    echo "  Option 3 (always works):"
    echo "    python3 ~/.owura/owura/app.py"
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
