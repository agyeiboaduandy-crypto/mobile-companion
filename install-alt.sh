#!/bin/bash
# ============================================================
# OWURA - Alternative Installer (for when curl fails)
# ============================================================
set -e

REPO="agyeiboaduandy-crypto/owura"
INSTALL_DIR="$HOME/.owura"
BIN_DIR="$HOME/.local/bin"

echo "Installing OWURA (alternative method)..."

# Method 1: Try curl
echo "[1/4] Downloading OWURA..."
if command -v curl &> /dev/null; then
    curl -sL "https://github.com/$REPO/archive/main.tar.gz" -o /tmp/owura.tar.gz && \
    tar -xzf /tmp/owura.tar.gz -C "$HOME" --strip-components=1 && \
    rm -f /tmp/owura.tar.gz
    mv "$HOME/owura" "$INSTALL_DIR" 2>/dev/null || true
elif command -v wget &> /dev/null; then
    wget -q "https://github.com/$REPO/archive/main.tar.gz" -O /tmp/owura.tar.gz && \
    tar -xzf /tmp/owura.tar.gz -C "$HOME" --strip-components=1 && \
    rm -f /tmp/owura.tar.gz
    mv "$HOME/owura" "$INSTALL_DIR" 2>/dev/null || true
elif command -v git &> /dev/null; then
    git clone "https://github.com/$REPO.git" "$INSTALL_DIR"
else
    echo "ERROR: No download tool found. Install curl, wget, or git first."
    exit 1
fi

# Create directories
mkdir -p "$BIN_DIR"

# Create command
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

# Also try to put it in $PREFIX/bin (Termux standard)
mkdir -p "$PREFIX/bin" 2>/dev/null || true
cp "$BIN_DIR/owura" "$PREFIX/bin/owura" 2>/dev/null && chmod +x "$PREFIX/bin/owura" 2>/dev/null || true

# Update PATH
if ! grep -q "OWURA" "$HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$HOME/.bashrc"
    echo "# OWURA - AI Coding Agent" >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

# Install dependencies
echo "[2/4] Installing dependencies..."
cd "$INSTALL_DIR"
pip3 install -r requirements.txt 2>/dev/null || pip install -r requirements.txt 2>/dev/null || true

# Verify
echo "[3/4] Verifying..."
if [ -f "$INSTALL_DIR/owura/app.py" ]; then
    echo "  âœ“ Application files installed"
else
    echo "  âœ— Application files missing"
    exit 1
fi

# Make executable
chmod +x "$INSTALL_DIR/owura/app.py" 2>/dev/null || true

echo "[4/4] Done!"
echo ""
echo "OWURA installed successfully!"
echo ""
echo "To run:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "  owura"
echo ""
echo "Or:"
echo "  python3 $INSTALL_DIR/owura/app.py"
