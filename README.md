# Mobile Companion

A companion app that transforms your Android device into a powerful AI coding station by leveraging Termux.

## Overview

The Mobile Companion allows you to run advanced AI coding assistants directly on your phone. It consists of a Termux-based runtime environment and a lightweight Android wrapper (APK) for easier management and access.

## Architecture

### 1. Termux Backend
Termux provides the Linux environment necessary to run CLI-based AI tools.
- **Runtimes**: Node.js, Python, Git, OpenSSH, jq.
- **Supported Providers**: 
  - Google AI Studio (Gemini)
  - Groq
  - NVIDIA
  - Ollama (Cloud/Local)
- **Integrations**:
  - **MCP (Model Context Protocol)**: Uses `config/mcp_config.json` to enable tools like filesystem and GitHub access.
  - **GitHub**: Full Git integration for pushing code directly from Termux.
  - **Skills**: Custom extensions for AI agents.
  - **Auto Model Fetching**: Automatically detects available models from your API keys.
- **API Integration**: Termux:API for hardware and system access.

### 2. Companion APK
The Android app acts as a control center and an integrated terminal with a built-in onboarding flow (see `docs/apk_flow.md`):
- **Integrated Terminal**: Uses a bridge to execute commands in Termux without leaving the app.
- **Onboarding Wizard**: Step-by-step guide to set up Termux, API keys, and GitHub.
- **Key Management**: Centralized storage for AI API keys.
- **Model Selector**: Auto-populated list of available models from connected providers.

### 3. Project Structure
```
mobile-companion/
â”œâ”€â”€ README.md
â”œâ”€â”€ .env.example
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ bootstrap.sh          # One-click installer
â”‚   â”œâ”€â”€ setup_termux.sh       # Runtime installer
â”‚   â”œâ”€â”€ manage_keys.sh        # API key manager
â”‚   â”œâ”€â”€ fetch_models.sh       # Model list fetcher
â”‚   â”œâ”€â”€ setup_github.sh       # GitHub SSH setup
â”‚   â””â”€â”€ shell_config.sh       # Shell aliases
â”œâ”€â”€ config/
â”‚   â””â”€â”€ mcp_config.json       # MCP server config
â””â”€â”€ docs/
    â”œâ”€â”€ apk_flow.md           # APK onboarding steps
    â”œâ”€â”€ google-ai-studio.md
    â”œâ”€â”€ groq.md
    â”œâ”€â”€ nvidia.md
    â””â”€â”€ ollama.md
```

## Quick Start (Termux)

Run this single command in Termux to set up everything:

```bash
curl -sL https://raw.githubusercontent.com/agyeiboaduandy-crypto/mobile-companion/main/scripts/bootstrap.sh | bash
```

Or manually:

```bash
pkg update && pkg upgrade -y
pkg install -y git
git clone https://github.com/agyeiboaduandy-crypto/mobile-companion.git
cd mobile-companion
bash scripts/bootstrap.sh
```

## Commands

| Command | Description |
|---------|-------------|
| `ai-setup` | Install all runtimes and dependencies |
| `ai-keys set KEY value` | Set an API key |
| `ai-keys list` | Show all configured keys |
| `ai-models` | List available models from all providers |
| `ai-update-models` | Refresh the model list |
| `ai-open` | Launch opencode |
| `ai-github` | Configure GitHub SSH access |

## Supported Providers

| Provider | Key Name | Endpoint |
|----------|----------|----------|
| Google AI Studio | `GOOGLE_AI_STUDIO_KEY` | generativelanguage.googleapis.com |
| Groq | `GROQ_API_KEY` | api.groq.com |
| NVIDIA | `NVIDIA_API_KEY` | api.nvidia.com |
| Ollama | `OLLAMA_HOST` | localhost:11434 |

## Prerequisites
- Android device.
- [Termux](https://termux.dev/en/) installed from F-Droid.
- [Termux:API](https://github.com/termux/termux-api) installed from F-Droid.
