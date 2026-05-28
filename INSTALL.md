# OWURA Installation Guide

## Method 1: One-Click Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash
source ~/.bashrc
owura
```

## Method 2: Alternative Install (if curl fails)

```bash
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install-alt.sh | bash
source ~/.bashrc
owura
```

## Method 3: Manual Install (if nothing works)

```bash
# Clone the repo
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura

# Create the command
mkdir -p ~/.local/bin
cat > ~/.local/bin/owura << 'EOF'
#!/bin/bash
exec python3 "$HOME/.owura/owura/app.py" "$@"
EOF
chmod +x ~/.local/bin/owura

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install dependencies
cd ~/.owura
pip3 install rich cryptography

# Run
owura
```

## Method 4: Direct Python (Always Works)

```bash
# Install Python first
pkg install python

# Download OWURA
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura

# Install dependencies
cd ~/.owura
pip3 install rich cryptography

# Run directly
python3 ~/.owura/owura/app.py
```

## Troubleshooting

### "owura: command not found"
```bash
export PATH="$HOME/.local/bin:$PATH"
owura
```

### "Permission denied"
```bash
chmod +x ~/.local/bin/owura
chmod +x ~/.owura/owura/app.py
```

### "Python not found"
```bash
pkg install python
```

### "pip install failed"
```bash
pip3 install rich cryptography --break-system-packages
```

## First Run

1. Run `owura`
2. Choose provider (gemini recommended - it's free)
3. Enter your API key
4. Start coding!
