# ðŸŒŒ OWURA: The AI Coding Agent for Mobile

**Code Anywhere. Anytime. Permanently.**

OWURA is not just an appâ€”it's a professional-grade development ecosystem that transforms your Android device into a powerful AI-driven coding station. By leveraging a unique bridge between a native Android interface and the Termux Linux environment, OWURA provides a seamless, high-performance experience for developers who refuse to be tied to a laptop.

![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Android%20%2F%20Termux-green.svg)
![Agent](https://img.shields.io/badge/Agent-OWURA_v1.0-neon)

---

## ðŸš€ The Vision

Most "mobile IDEs" are just text editors with a few plugins. **OWURA is different.** It is a lightweight version of a full AI coding agent (like opencode) optimized specifically for the constraints and strengths of mobile devices.

OWURA creates a "Cyber-Cockpit" on your phone, connecting you to the world's most powerful LLMs and giving you a real Linux shell to execute, test, and deploy your code.

## âœ¨ Key Features

### ðŸ§  Intelligent Model Routing
OWURA doesn't lock you into one AI. It automatically detects and routes your requests to the best available provider based on your API keys:
- **Google AI Studio (Gemini 1.5 Pro)**: For deep reasoning and massive context.
- **Groq (Llama 3)**: For near-instantaneous code generation.
- **NVIDIA NIM**: For high-performance specialized models.
- **Ollama**: For local, private AI execution on your own hardware.

### ðŸ› ï¸ The Professional Toolchain
- **Full Linux Backend**: Powered by Termux, giving you access to `git`, `node`, `python`, `rust`, `go`, and more.
- **MCP (Model Context Protocol)**: Integrated filesystem and GitHub servers that allow the AI to actually *read and write* your files and *manage your repos*.
- **GitHub Synchronization**: Push your professional work to the cloud directly from your pocket.
- **Native Android Bridge**: A custom APK that manages your environment and launches your agent with a single tap.

### ðŸŽ­ Agent Modes
OWURA adapts to your current workflow:
- `[ARCHITECT]`: Focuses on system design, file structure, and planning.
- `[CODER]`: Optimized for raw implementation, refactoring, and speed.
- `[SENTRY]`: Dedicated to debugging, security audits, and error hunting.

---

## ðŸ“¦ Installation

### 1. Prerequisites
- **Android Device**
- **Termux** (Install from [F-Droid](https://f-droid.org/en/packages/com.termux/))
- **Termux:API** (Install from [F-Droid](https://f-droid.org/en/packages/com.termux.api/))

### 2. One-Click Setup
Run this command in Termux to deploy the entire OWURA ecosystem:

```bash
curl -sL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/scripts/bootstrap.sh | bash
```

### 3. Configure Your Brain
Set your API keys using the built-in manager:
```bash
owura-keys set GOOGLE_AI_STUDIO_KEY your_key_here
owura-keys set GROQ_API_KEY your_key_here
```

### 4. Launch the Agent
```bash
owura
```

---

## ðŸ“± The Companion APK

The OWURA APK is the control center for your agent. It handles:
- **Onboarding**: Guides you through the Termux installation.
- **Key Management**: Securely stores your API tokens.
- **Model Scanner**: Lists all models available from your providers.
- **Quick-Launch**: Bypasses the terminal setup and jumps straight into coding.

**To build the APK on your laptop:**
```bash
cd owura-android
./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

---

## ðŸ“œ License

Distributed under the **Apache License 2.0**. See `LICENSE` for more information.

---

**OWURA** â€” *Because the world doesn't stop coding just because your laptop is closed.*
