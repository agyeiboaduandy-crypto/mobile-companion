# OWURA

**AI Coding Agent for Mobile Terminal — Just describe, it builds.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%2F%20Linux-yellow.svg)](https://termux.dev/)

Build real, production-grade products from your phone. OWURA is a terminal-based AI coding assistant designed for **vibe coders** — people who describe what they want and watch it get built. No laptop required.

---

## Table of Contents

- [What is OWURA?](#what-is-owura)
- [Installation](#installation)
  - [Termux (Android) — One-Liner](#termux-android--one-liner)
  - [Linux / macOS](#linux--macos)
  - [Manual Install (Most Reliable)](#manual-install-most-reliable)
  - [Direct Python (Always Works)](#direct-python-always-works)
- [Quick Start](#quick-start)
- [Building Projects](#building-projects)
  - [Just Describe It](#just-describe-it)
  - [Available Templates](#available-templates)
- [Commands](#commands)
- [Providers](#providers)
- [What You Get When You Build](#what-you-get-when-you-build)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)
- [License](#license)

---

## What is OWURA?

OWURA is not a toy. It's a **production-grade project generator** that lives in your terminal:

- **Describe what you want**: `/build a Twitter clone with Next.js and PostgreSQL`
- **It scaffolds the entire project**: Docker, CI/CD, database, auth, tests, monitoring — everything
- **You just run it**: `docker-compose up -d`
- **No config, no setup, no hassle**

Built for Termux on Android. Works on any Linux system.

---

## Installation

### Termux (Android) — One-Liner

```bash
pkg update && pkg upgrade -y
pkg install python git curl -y
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash
source ~/.bashrc
owura
```

### Linux / macOS

```bash
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash
source ~/.bashrc
owura
```

### Manual Install (Most Reliable)

```bash
# 1. Install Python if you don't have it (Termux)
pkg install python git

# 2. Clone OWURA
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura

# 3. Install dependencies
pip3 install rich cryptography

# 4. Create the launcher script
mkdir -p ~/.local/bin
cat > ~/.local/bin/owura << 'EOF'
#!/bin/bash
exec python3 "$HOME/.owura/owura/app.py" "$@"
EOF
chmod +x ~/.local/bin/owura

# 5. Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 6. Run it
owura
```

### Direct Python (Always Works)

```bash
# 1. Prerequisites
pkg install python git
git clone https://github.com/agyeiboaduandy-crypto/owura.git ~/.owura
cd ~/.owura
pip3 install rich cryptography

# 2. Run directly (no PATH config needed)
python3 ~/.owura/owura/app.py
```

---

## Quick Start

```bash
owura
```

First run walks you through:
1. **Pick a provider** (Gemini is free — no credit card needed)
2. **Enter your API key** (get one free at https://aistudio.google.com/apikey)
3. **Select a model** from the ones fetched automatically from your provider
4. **Start building** 🚀

---

## Building Projects

### Just Describe It

This is the main feature. Tell OWURA what you want in plain English:

```bash
/build a Twitter clone with Next.js and PostgreSQL
/build a REST API with FastAPI and Redis caching
/build a real-time chat app with WebSockets
/build a cryptocurrency dashboard with Go
/build a microservice for user authentication
```

OWURA automatically:
1. **Detects the best tech stack** from your description
2. **Scaffolds a complete project** with production-grade structure
3. **Includes everything you need**: Docker, CI/CD, database, tests, monitoring

### Available Templates

```bash
/create fastapi my-api          # FastAPI + PostgreSQL (async)
/create flask-api my-api        # Flask + SQLAlchemy
/create express my-api          # Express.js + TypeScript + Prisma
/create nextjs my-app           # Next.js + TypeScript
/create django my-app           # Django + SQLite
/create react my-app            # React + Vite
/create go-api my-api           # Go HTTP server
/create python-cli my-tool      # Python CLI tool
/create rust-cli my-tool        # Rust CLI (cargo)
```

### What Every Production Template Includes

Every project scaffolded by `/build` or `/create` comes with:

| Feature | What you get |
|---------|-------------|
| **Docker** | Multi-stage build, production-optimized |
| **Docker Compose** | App + PostgreSQL + Redis + Nginx, all wired up |
| **Database** | Async SQLAlchemy (Python) or Prisma (Node), with migrations |
| **API Architecture** | Versioned routes, schemas, services layer |
| **Testing** | Pytest or Vitest with fixtures and CI integration |
| **CI/CD** | GitHub Actions — lint, test, build, deploy |
| **Monitoring** | Prometheus + Grafana ready (production compose) |
| **Logging** | Structured JSON logging, request tracing |
| **Rate Limiting** | SlowAPI (Python) or express-rate-limit (Node) |
| **Security** | CORS, Helmet, input validation |
| **Health Checks** | `/api/health` endpoint for orchestration |
| **NGINX** | Reverse proxy with load balancing config |
| **Environments** | `.env.example` with all documented variables |

---

## Commands

### Building

| Command | Description |
|---------|-------------|
| `/build <description>` | Just describe what you want — OWURA scaffolds it |
| `/create <template> <name>` | Create from a specific template |
| `/analyze [path]` | Analyze a project and suggest improvements |
| `/generate tests <file>` | Generate test stubs for a file |
| `/deploy <platform>` | Generate deploy config (docker/heroku/railway/vercel) |

### AI & Provider

| Command | Description |
|---------|-------------|
| `/provider [name]` | Set provider — interactive, fetches models from API |
| `/key [key]` | Set or view your API key |
| `/model [name]` | Set model manually |

### Code & Files

| Command | Description |
|---------|-------------|
| `/run <command>` | Execute any shell command |
| `/ls [path]` | List directory contents |
| `/cat <file>` | View file with syntax highlighting |
| `/cd <path>` | Change directory |
| `/git <args>` | Run git commands |
| `/pwd` | Show current directory |

### Smart Skills

| Command | Description |
|---------|-------------|
| `/review <code/file>` | Code quality review with scoring |
| `/optimize <code/file>` | Performance optimization suggestions |
| `/reverse <target>` | Reverse engineer code/APIs/binary |
| `/loophole <problem>` | Find creative workarounds |
| `/fix <problem>` | Make impossible things work |

### Web & Search

| Command | Description |
|---------|-------------|
| `/search <query>` | Search the web |
| `/github <query>` | Search GitHub repos |
| `/pypi <package>` | Search Python Package Index |
| `/npm <package>` | Search npm registry |
| `/so <query>` | Search StackOverflow |
| `/wiki <topic>` | Wikipedia lookup |
| `/weather <city>` | Get weather forecast |
| `/news [topic]` | Latest news |
| `/fetch <url>` | Fetch and display a URL |
| `/docs <query> [lang]` | Search documentation |

### Memory & Learning

| Command | Description |
|---------|-------------|
| `/memory` | Show memory statistics |
| `/remember <fact>` | Store a fact permanently |
| `/recall <query>` | Search your memories |
| `/project <name>` | Record a project |
| `/learn <what> -> <outcome>` | Record a learning |

### System

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/config` | Show current configuration |
| `/status` | System status and usage |
| `/privacy` | Privacy and security status |
| `/compact` | Full system cleanup |
| `/clean` | Quick cache cleanup |
| `/who` | Learn about OWURA |
| `/mission` | See our mission |
| `/version` | Show version |
| `/quit` | Exit |

### Creative

| Command | Description |
|---------|-------------|
| `/story <concept>` | Learn complex ideas as stories |
| `/metaphor <concept>` | Understand with metaphors |
| `/challenge [easy]` | Get coding challenges |
| `/wisdom` | Programming wisdom |
| `/poem` | Code poetry |
| `/ascii <text>` | ASCII art generator |

---

## Providers

OWURA supports 15+ AI providers. Models are fetched **live from the API** when you add your key — no hardcoded lists.

| Provider | CLI Name | Free Tier | How to get key |
|----------|----------|-----------|---------------|
| **Google Gemini** | `gemini` | ✅ Yes | https://aistudio.google.com/apikey |
| **OpenAI** | `openai` | ❌ Paid | https://platform.openai.com/api-keys |
| **Groq** | `groq` | ✅ Yes | https://console.groq.com/keys |
| **NVIDIA NIM** | `nvidia` | ✅ Yes | https://build.nvidia.com/ |
| **Together AI** | `together` | ✅ Yes | https://api.together.xyz/signup |
| **OpenRouter** | `openrouter` | ✅ Yes | https://openrouter.ai/keys |
| **DeepSeek** | `deepseek` | ✅ Yes | https://platform.deepseek.com/ |
| **Mistral AI** | `mistral` | ✅ Yes | https://console.mistral.ai/ |
| **Perplexity** | `perplexity` | ❌ Paid | https://www.perplexity.ai/settings/api |
| **Fireworks AI** | `fireworks` | ✅ Yes | https://fireworks.ai/ |
| **Cohere** | `cohere` | ✅ Yes | https://dashboard.cohere.com/ |
| **xAI (Grok)** | `xai` | ❌ Paid | https://x.ai/api |
| **GitHub Models** | `github` | ✅ Yes | https://github.com/settings/tokens |
| **Anthropic** | `anthropic` | ❌ Paid | https://console.anthropic.com/ |
| **Custom** | `custom <url>` | Depends | Any OpenAI-compatible API |

### Adding a Custom Provider

Any OpenAI-compatible API works:
```bash
/provider custom https://api.together.xyz/v1
/provider custom https://openrouter.ai/api/v1
/provider custom https://api.deepseek.com/v1
```

The 14 built-in providers above are just shortcuts — you can use any OpenAI-compatible endpoint as a custom provider.

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

### "pip install failed — externally managed"
```bash
pip3 install rich cryptography --break-system-packages
```

### "Module not found: cryptography"
```bash
pip3 install cryptography
```

### Termux permissions
```bash
termux-setup-storage
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

**OWURA** — Code Anywhere. Anytime. Just describe, it builds.
