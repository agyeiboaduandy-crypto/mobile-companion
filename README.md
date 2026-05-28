# OWURA

**Your AI Coding Agent for Mobile**

A lightweight, permanent coding companion that turns your phone into a powerful AI development station. Code anywhere, anytime.

## What is OWURA?

OWURA is a mobile-first AI coding agent that connects to multiple AI providers and gives you the power of opencode right on your phone. When your laptop is down, OWURA keeps you coding.

## Features

- **Multi-Provider AI**: Connect to Google AI Studio, Groq, NVIDIA, or Ollama
- **Auto Model Detection**: Automatically fetches available models when you add an API key
- **Terminal Integration**: Direct Termux integration for full Linux environment
- **GitHub Push**: Push your code directly from your phone
- **MCP Support**: Model Context Protocol for enhanced AI capabilities
- **Permanent Setup**: One-time setup, code forever

## Quick Start

```bash
# In Termux
pkg install -y git
git clone https://github.com/agyeiboaduandy-crypto/owura.git
cd owura
bash scripts/bootstrap.sh
```

## Commands

| Command | Description |
|---------|-------------|
| `owura-setup` | Install all runtimes and dependencies |
| `owura-keys set KEY value` | Set an API key |
| `owura-keys list` | Show all configured keys |
| `owura-models` | List available models from all providers |
| `owura-update-models` | Refresh the model list |
| `owura-open` | Launch opencode |
| `owura-github` | Configure GitHub SSH access |
| `owura` | Launch OWURA app |

## Supported Providers

| Provider | Key Name |
|----------|----------|
| Google AI Studio | `GOOGLE_AI_STUDIO_KEY` |
| Groq | `GROQ_API_KEY` |
| NVIDIA | `NVIDIA_API_KEY` |
| Ollama | `OLLAMA_HOST` |

## APK

Build the OWURA APK directly in Termux:

```bash
cd owura/apk
bash build.sh
```

## Architecture

```
owura/
â”œâ”€â”€ scripts/           # Core scripts
â”‚   â”œâ”€â”€ bootstrap.sh   # One-click installer
â”‚   â”œâ”€â”€ owura.sh       # Main launcher
â”‚   â”œâ”€â”€ setup.sh       # Runtime installer
â”‚   â”œâ”€â”€ keys.sh        # API key manager
â”‚   â”œâ”€â”€ models.sh      # Model fetcher
â”‚   â””â”€â”€ github.sh      # GitHub setup
â”œâ”€â”€ config/            # Configuration
â”‚   â””â”€â”€ mcp.json       # MCP server config
â”œâ”€â”€ apk/               # Android app
â”‚   â”œâ”€â”€ src/           # Kotlin sources
â”‚   â”œâ”€â”€ res/           # Resources
â”‚   â””â”€â”€ build.sh       # APK builder
â””â”€â”€ docs/              # Documentation
```

## Why OWURA?

Because coding shouldn't stop when your laptop breaks. OWURA is your permanent mobile coding partner - lightweight, powerful, and always with you.

---

**OWURA** - Code Anywhere. Anytime.
