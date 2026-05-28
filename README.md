# ðŸŒŒ OWURA

**AI Coding Agent for Mobile Terminal**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%2F%20Linux-yellow.svg)](https://termux.dev/)

---

## What is OWURA?

OWURA is a **living, learning AI coding assistant** that runs in your terminal. It's designed for developers who want to code anywhere, anytime - especially on mobile devices using Termux.

Unlike basic AI chatbots, OWURA:
- **Learns from every interaction** - remembers what worked and what didn't
- **Stores project context** - knows about your past projects and preferences
- **Has built-in skills** - 12+ coding skills ready to use
- **Connects to MCP servers** - Context7, GitHub, PyPI, npm, and more
- **Works offline** - your data stays on your device

---

## Quick Install

```bash
# One-click install
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash

# Or manually
git clone https://github.com/agyeiboaduandy-crypto/owura.git
cd owura
chmod +x install.sh
./install.sh
```

Then run:
```bash
owura
```

---

## Features

### ðŸ§  Persistent Memory
OWURA remembers everything:
- Facts and preferences
- Project details
- Code patterns that work
- Errors and their solutions

### ðŸ› ï¸ Built-in Skills
| Skill | Description |
|-------|-------------|
| `web-search` | Search documentation and examples |
| `file-operations` | Create, read, update files |
| `git-operations` | Version control |
| `python-dev` | Python development |
| `nodejs-dev` | Node.js development |
| `shell-scripting` | Bash scripting |
| `api-integration` | Connect to APIs |
| `database` | SQL and NoSQL |
| `docker` | Container management |
| `security` | Secure coding |
| `testing` | Test and debug |
| `deployment` | Deploy apps |

### ðŸ”Œ MCP Servers
- **Context7** - Up-to-date documentation
- **GitHub** - Repos, issues, code search
- **PyPI** - Python packages
- **npm** - Node.js packages
- **StackOverflow** - Find solutions
- **DevDocs** - Developer documentation

### ðŸ“ Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/config` | View configuration |
| `/provider <name>` | Set AI provider |
| `/key <api_key>` | Set API key |
| `/run <cmd>` | Execute command |
| `/memory` | View memory stats |
| `/remember <fact>` | Store a fact |
| `/recall <query>` | Search memory |
| `/project <name>` | Record project |
| `/skills` | List skills |
| `/mcp` | List MCP servers |
| `/suggest` | Get suggestions |
| `/template <type>` | Get template |
| `/quit` | Exit |

---

## Configuration

### Providers
- **Gemini** (free tier available) - Get key at [AI Studio](https://aistudio.google.com/apikey)
- **OpenAI** - Get key at [OpenAI](https://platform.openai.com/api-keys)
- **Groq** - Get key at [Groq](https://console.groq.com/keys)

### First Run
```bash
owura
# Follow the prompts to set your provider and API key
```

### Change Provider
```
/provider gemini
/key your-api-key-here
```

---

## Memory System

OWURA learns automatically:
- **Code patterns** - remembers successful commands
- **Errors & solutions** - learns from debugging
- **User preferences** - adapts to your style
- **Project context** - tracks your projects

### Manual Memory
```
/remember Python 3.12 has new type hints
/recall python
/project myapp --record a new project
/learn pip install breaks on arm64 -> use --platform flag
```

---

## Project Structure

```
owura/
â”œâ”€â”€ owura/
â”‚   â”œâ”€â”€ __init__.py      # Package init
â”‚   â”œâ”€â”€ __main__.py      # Entry point
â”‚   â”œâ”€â”€ app.py           # Main application
â”‚   â”œâ”€â”€ skills.py        # Built-in skills
â”‚   â””â”€â”€ memory.py        # Memory system
â”œâ”€â”€ install.sh           # Installer
â”œâ”€â”€ uninstall.sh         # Uninstaller
â”œâ”€â”€ requirements.txt     # Dependencies
â”œâ”€â”€ setup.py            # Package setup
â””â”€â”€ README.md           # This file
```

---

## Usage Examples

### Chat with AI
```
owura> Write a Python function to sort a list
owura> How do I connect to PostgreSQL?
owura> Debug this code: [paste code]
```

### Execute Commands
```
/ls
/pwd
/run python3 script.py
/git status
```

### Memory
```
/recall python
/memory
/remember Use virtual environments always
```

### Skills
```
/skills
/web-search how to use async await in Python
```

---

## Uninstall

```bash
./uninstall.sh
# or
rm -rf ~/.owura ~/.local/bin/owura
```

---

## License

Apache License 2.0 - See [LICENSE](LICENSE)

---

## Contributing

1. Fork the repo
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

**OWURA** - *Code Anywhere. Anytime. Permanently.*
