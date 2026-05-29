# OWURA

**Terminal AI Coding Agent**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%2F%20Linux-yellow.svg)](https://termux.dev/)

OWURA is an AI coding agent that runs in your terminal. It helps you build software — from scripts to full production systems — by generating code, scaffolding projects, managing files, and running commands. Built for Termux on Android, also runs on Linux and macOS.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
  - [Termux (Android)](#termux-android)
  - [Linux / macOS](#linux--macos)
  - [Manual Install](#manual-install)
  - [Direct Python](#direct-python)
- [Specifications](#specifications)
  - [Technical Overview](#technical-overview)
  - [Scaffolding Features](#scaffolding-features)
  - [Providers](#providers)
- [Usage](#usage)
  - [Building Projects](#building-projects)
  - [Commands](#commands)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)
- [License](#license)

---

## Quick Start

```bash
owura
```

First run walks you through:
1. Pick an AI provider (Gemini is free, no credit card)
2. Enter your API key
3. Select a model from all available (fetched live from your provider)
4. Start building

Each launch checks for new OWURA versions — notifications appear automatically.

---

## Installation

### Termux (Android)

**One-liner:**

```bash
pkg update && pkg upgrade -y
pkg install python git curl -y
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash
source ~/.bashrc
owura
```

**Step by step if the one-liner doesn't work:**

```bash
# 1. Update packages
pkg update && pkg upgrade -y

# 2. Install Python and git
pkg install python git curl -y

# 3. Clone the repo
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura

# 4. Install Python dependencies
pip3 install rich cryptography

# 5. Create the launcher
mkdir -p ~/.local/bin
cat > ~/.local/bin/owura << 'EOF'
#!/bin/bash
exec python3 "$HOME/.owura/owura/app.py" "$@"
EOF
chmod +x ~/.local/bin/owura

# 6. Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 7. Run
owura
```

**Note for Termux:** If you get storage permission errors, run `termux-setup-storage` first.

---

### Linux / macOS

```bash
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash
source ~/.bashrc
owura
```

---

### Manual Install

Works everywhere including Termux:

```bash
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura
pip3 install rich cryptography
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

---

### Direct Python

No PATH setup needed:

```bash
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura
cd ~/.owura
pip3 install rich cryptography
python3 ~/.owura/owura/app.py
```

---

## Specifications

### Technical Overview

| Aspect | Details |
|--------|---------|
| **Language** | Python 3.8+ |
| **Interface** | Interactive TUI (terminal) via Rich |
| **AI Providers** | 15 built-in + any OpenAI-compatible endpoint |
| **Model Discovery** | Fetches available models live from provider API |
| **API Keys** | Encrypted at rest via Fernet (cryptography) |
| **Memory** | Persistent JSON store with facts, learnings, patterns |
| **Privacy** | Prompt sanitization strips emails, phones, keys, passwords |
| **Skills** | 12+ built-in skills with auto-detection |
| **Project Scaffolding** | 9 templates with Docker, CI/CD, DB, tests |
| **Web Tools** | Search, GitHub, PyPI, npm, StackOverflow, Wikipedia, weather |
| **Caching** | Local response cache with auto-cleanup (7-day TTL) |
| **Compaction** | Auto-cleanup of pip/npm/temp caches |
| **Context Compaction** | Auto-summarizes conversation every 20 messages, keeps latest 10 |
| **Self-Upgrade** | `/upgrade` — detects new versions and upgrades itself via git pull |
| **Platforms** | Termux (Android), Linux, macOS |

### Scaffolding Features

Every scaffolded project includes:

| Layer | What you get |
|-------|-------------|
| **Container** | Multi-stage Dockerfile, Docker Compose (app + PostgreSQL + Redis + Nginx) |
| **Database** | Async SQLAlchemy (Python) / Prisma (Node) with migrations |
| **API Layer** | Versioned routes, request schemas, service layer |
| **Authentication** | JWT-ready middleware, password hashing |
| **Security** | CORS, Helmet, rate limiting, input validation |
| **Logging** | Structured JSON logging with request tracing |
| **Monitoring** | Prometheus + Grafana (production compose) |
| **Testing** | Pytest / Vitest with fixtures |
| **CI/CD** | GitHub Actions — lint, test, build, deploy |
| **Health** | /api/health endpoint with Docker healthcheck |
| **Config** | .env.example with every variable documented |
| **Scaling** | Production compose with replica support |

### Providers

15 AI providers supported. Models are fetched live when you add your key.

| Provider | CLI name | Free tier | Key |
|----------|----------|-----------|-----|
| Google Gemini | `gemini` | ✅ | https://aistudio.google.com/apikey |
| Groq | `groq` | ✅ | https://console.groq.com/keys |
| NVIDIA NIM | `nvidia` | ✅ | https://build.nvidia.com/ |
| Together AI | `together` | ✅ | https://api.together.xyz/signup |
| OpenRouter | `openrouter` | ✅ | https://openrouter.ai/keys |
| DeepSeek | `deepseek` | ✅ | https://platform.deepseek.com/ |
| Mistral AI | `mistral` | ✅ | https://console.mistral.ai/ |
| Fireworks AI | `fireworks` | ✅ | https://fireworks.ai/ |
| Cohere | `cohere` | ✅ | https://dashboard.cohere.com/ |
| GitHub Models | `github` | ✅ | https://github.com/settings/tokens |
| OpenAI | `openai` | ❌ | https://platform.openai.com/api-keys |
| Perplexity | `perplexity` | ❌ | https://www.perplexity.ai/settings/api |
| xAI (Grok) | `xai` | ❌ | https://x.ai/api |
| Anthropic | `anthropic` | ❌ | https://console.anthropic.com/ |
| Custom | `custom <url>` | varies | Any OpenAI-compatible API |

Any OpenAI-compatible endpoint works as a custom provider:
```bash
/provider custom https://api.together.xyz/v1
/provider custom https://openrouter.ai/api/v1
```

---

## Usage

### Building Projects

Describe what you want:

```bash
/build a Twitter clone with Next.js and PostgreSQL
/build a REST API with FastAPI and Redis
/build a real-time chat app with WebSockets
/build a cryptocurrency dashboard with Go
/build a microservice for user authentication
```

OWURA detects the tech stack and scaffolds a complete production project. You can also pick a specific template:

```bash
/create fastapi my-api          # FastAPI + PostgreSQL async
/create flask-api my-api        # Flask + SQLAlchemy
/create express my-api          # Express.js + TypeScript + Prisma
/create nextjs my-app           # Next.js + TypeScript
/create django my-app           # Django + SQLite
/create react my-app            # React + Vite
/create go-api my-api           # Go HTTP server
/create python-cli my-tool      # Python CLI
/create rust-cli my-tool        # Rust CLI (cargo)
```

---

### Commands

**Building**
| Command | Description |
|---------|-------------|
| `/build <description>` | Scaffold a project from a description |
| `/create <template> <name>` | Create from a specific template |
| `/analyze [path]` | Analyze a project and suggest improvements |
| `/generate tests <file>` | Generate test stubs |
| `/deploy <platform>` | Generate deploy config |

**AI & Provider**
| Command | Description |
|---------|-------------|
| `/provider [name]` | Set AI provider (interactive, fetches all models) |
| `/key [key]` | Set or view API key |
| `/model [name]` | Set model manually |
| `/upgrade` | Check for updates and upgrade OWURA itself |

**Code & Files**
| Command | Description |
|---------|-------------|
| `/run <cmd>` | Execute shell command |
| `/ls [path]` | List directory |
| `/cat <file>` | View file with syntax highlighting |
| `/cd <path>` | Change directory |
| `/git <args>` | Run git commands |
| `/pwd` | Show current directory |

**Smart Skills**
| Command | Description |
|---------|-------------|
| `/review <code/file>` | Code quality review with score |
| `/optimize <code/file>` | Performance optimization tips |
| `/reverse <target>` | Reverse engineer code/APIs/binary |
| `/loophole <problem>` | Find workarounds |
| `/fix <problem>` | Solve impossible problems |

**Web & Search**
| Command | Description |
|---------|-------------|
| `/search <query>` | Web search |
| `/github <query>` | Search GitHub |
| `/pypi <package>` | Search PyPI |
| `/npm <package>` | Search npm |
| `/so <query>` | Search StackOverflow |
| `/wiki <topic>` | Wikipedia lookup |
| `/weather <city>` | Weather forecast |
| `/news [topic]` | Latest news |
| `/docs <query> [lang]` | Documentation search |

**Memory & Learning**
| Command | Description |
|---------|-------------|
| `/memory` | Memory statistics |
| `/remember <fact>` | Store a fact |
| `/recall <query>` | Search memories |
| `/project <name>` | Record a project |
| `/learn <what> -> <outcome>` | Record a learning |

**System**
| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/config` | Show configuration |
| `/status` | System status |
| `/privacy` | Privacy status |
| `/compact` | Full cleanup |
| `/clean` | Quick cache cleanup |
| `/upgrade` | Check for and apply updates |
| `/who` | About OWURA |
| `/version` | Show version |
| `/quit` | Exit |

**Skills & MCPs**
| Command | Description |
|---------|-------------|
| `/skills` | List all skills (built-in + custom) |
| `/mcp` | List all MCPs (built-in + custom) |
| `/skill-add <key>` | Add a custom skill with interactive prompts |
| `/skill-remove <key>` | Remove a custom skill |
| `/mcp-add <key>` | Add a custom MCP with interactive prompts |
| `/mcp-remove <key>` | Remove a custom MCP |

**Creative**
| Command | Description |
|---------|-------------|
| `/story <concept>` | Learn through stories |
| `/metaphor <concept>` | Understand via metaphors |
| `/challenge [easy]` | Coding challenges |
| `/wisdom` | Programming wisdom |
| `/poem` | Code poetry |

---

## Troubleshooting

### "owura: command not found"
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### "Python not found" (Termux)
```bash
pkg install python
```

### "pip install failed"
```bash
pip3 install rich cryptography --break-system-packages
```

### "cryptography" module error
```bash
pip3 install cryptography
```

### Storage permission (Termux)
```bash
termux-setup-storage
```

---

## Uninstall

```bash
rm -rf ~/.owura ~/.local/bin/owura
sed -i '/OWURA/d' ~/.bashrc
```

---

## License

Apache License 2.0
