# OWURA

**AI Coding Agent for Mobile Terminal**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%2F%20Linux-yellow.svg)](https://termux.dev/)

---

## What is OWURA?

OWURA is a terminal-based AI coding assistant that runs on your phone via Termux. It learns from every interaction, remembers your projects, and gets smarter over time.

---

## Installation

### Method 1: curl (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash
source ~/.bashrc
owura
```

### Method 2: Alternative Install (if curl fails)

```bash
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install-alt.sh | bash
source ~/.bashrc
owura
```

### Method 3: Manual Install (Most Reliable)

```bash
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura
mkdir -p ~/.local/bin
cat > ~/.local/bin/owura << 'EOF'
#!/bin/bash
exec python3 "$HOME/.owura/owura/app.py" "$@"
EOF
chmod +x ~/.local/bin/owura
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
owura
```

### Method 4: Direct Python (Always Works)

```bash
pkg install python git
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura
cd ~/.owura
pip3 install rich cryptography
python3 ~/.owura/owura/app.py
```

---

## Quick Start

After installation:

```bash
owura
```

First run will ask for your API key. Get a free one at [Google AI Studio](https://aistudio.google.com/apikey).

---

## Commands

### Basic
| Command | What it does |
|---------|--------------|
| `/help` | Show all commands |
| `/run <cmd>` | Run a shell command |
| `/ls` | List files |
| `/cat <file>` | View a file |
| `/git <args>` | Run git |
| `/quit` | Exit OWURA |

### AI & Memory
| Command | What it does |
|---------|--------------|
| `/provider <name>` | Set AI provider |
| `/key <api_key>` | Set API key |
| `/memory` | View memory stats |
| `/remember <fact>` | Store a fact |
| `/recall <query>` | Search memory |

### Smart Skills
| Command | What it does |
|---------|--------------|
| `/review` | Review code quality |
| `/optimize` | Optimize performance |
| `/loophole` | Find workarounds |
| `/reverse` | Reverse engineer code |

### Web Tools
| Command | What it does |
|---------|--------------|
| `/search <query>` | Search the web |
| `/github <query>` | Search GitHub |
| `/pypi <package>` | Search Python packages |
| `/npm <package>` | Search npm packages |
| `/so <query>` | Search StackOverflow |
| `/wiki <topic>` | Wikipedia lookup |
| `/weather <city>` | Get weather |
| `/news [topic]` | Get latest news |

### Creative
| Command | What it does |
|---------|--------------|
| `/story <concept>` | Learn as stories |
| `/metaphor <concept>` | Understand with metaphors |
| `/challenge [easy]` | Get coding challenges |
| `/wisdom` | Programming wisdom |
| `/poem` | Code poetry |

### System
| Command | What it does |
|---------|--------------|
| `/status` | Show system status |
| `/compact` | Clean caches |
| `/clean` | Quick cleanup |
| `/privacy` | Privacy status |
| `/who` | Learn about OWURA |
| `/mission` | See our mission |

---

## Providers

| Provider | Free Tier | Command |
|----------|-----------|---------|
| Gemini | Yes | `/provider gemini` |
| OpenAI | No | `/provider openai` |
| Groq | Yes | `/provider groq` |
| NVIDIA | Yes | `/provider nvidia` |
| Custom | - | `/provider custom <url>` |

---

## Features

- **Persistent Memory** - Learns from every interaction
- **12+ Skills** - Python, Git, Docker, APIs, etc.
- **Web Search** - Search, GitHub, PyPI, npm, StackOverflow
- **Smart Skills** - Self-review, optimize, find loopholes
- **Creative Mode** - Stories, metaphors, challenges
- **Security** - Encrypted keys, privacy-first
- **Auto-cleanup** - Manages cache automatically

---

## Troubleshooting

### "owura: command not found"
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### "Permission denied"
```bash
chmod +x ~/.local/bin/owura
```

### "Python not found"
```bash
pkg install python
```

### "pip install failed"
```bash
pip3 install rich cryptography --break-system-packages
```

---

## Uninstall

```bash
rm -rf ~/.owura ~/.local/bin/owura
```

---

## License

Apache License 2.0

---

**OWURA** - Code Anywhere. Anytime.
