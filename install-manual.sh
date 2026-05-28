#!/bin/bash
# ============================================================
# OWURA - Manual Installer (copy-paste method)
# Use this if curl/wget don't work
# ============================================================

echo "=== OWURA Manual Install ==="
echo ""
echo "Follow these steps:"
echo ""

# Step 1: Create directories
echo "Step 1: Creating directories..."
mkdir -p "$HOME/.owura"
mkdir -p "$HOME/.local/bin"

# Step 2: Clone or download
echo ""
echo "Step 2: Getting OWURA files..."
echo ""
echo "Option A (if git is installed):"
echo "  git clone https://github.com/agyeiboaduandy-crypto/owura.git $HOME/.owura"
echo ""
echo "Option B (if curl works):"
echo "  curl -sL https://github.com/agyeiboaduandy-crypto/owura/archive/main.tar.gz | tar -xz -C $HOME"
echo "  mv $HOME/owura-main $HOME/.owura"
echo ""
echo "Option C (manual download):"
echo "  1. Go to https://github.com/agyeiboaduandy-crypto/owura"
echo "  2. Click Code -> Download ZIP"
echo "  3. Extract to $HOME/.owura"
echo ""

# Step 3: Create command
echo "Step 3: Creating owura command..."
cat > "$HOME/.local/bin/owura" << 'COMMAND'
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
chmod +x "$HOME/.local/bin/owura"
echo "  Created: $HOME/.local/bin/owura"

# Step 4: Update PATH
echo ""
echo "Step 4: Updating PATH..."
if ! grep -q "OWURA" "$HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$HOME/.bashrc"
    echo "# OWURA - AI Coding Agent" >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo "  Added to ~/.bashrc"
else
    echo "  Already in ~/.bashrc"
fi

# Step 5: Install dependencies
echo ""
echo "Step 5: Installing dependencies..."
cd "$HOME/.owura"
pip3 install rich cryptography 2>/dev/null || pip install rich cryptography 2>/dev/null || echo "  (install rich and cryptography manually)"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Run OWURA with:"
echo "  source ~/.bashrc"
echo "  owura"
echo ""
echo "Or:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "  owura"
