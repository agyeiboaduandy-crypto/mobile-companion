# OWURA

**AI Coding Agent for Mobile Terminal**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%2F%20Linux-yellow.svg)](https://termux.dev/)

---

## What is OWURA?

OWURA is a terminal-based AI coding assistant that runs on your phone via Termux. It learns from every interaction, remembers your projects, and gets smarter over time.

**Perfect for:**
- Developers without a laptop
- Coding on the go
- Quick prototyping
- Learning to code

---

## Install

Open Termux and run:

```bash
curl -sSL https://raw.githubusercontent.com/agyeiboaduandy-crypto/owura/main/install.sh | bash
```

Then start it:

```bash
source ~/.bashrc
owura
```

First run will ask for your API key. Get a free one at [Google AI Studio](https://aistudio.google.com/apikey).

---

## Usage

Once installed, just type `owura` in Termux.

### Chat with AI

```
owura> Write a Python function to sort a list
owura> How do I connect to a database?
owura> Debug this code: [paste code]
```

### Run Commands

```
/run ls                    # List files
/pwd                       # Show current directory
/run python3 app.py        # Run a command
/git status                # Git commands
```

### Memory System

```
/remember Use virtual environments always    # Store a fact
/recall python                                # Search memory
/memory                                       # View all memories
```

### System Management

```
/status    # Show disk and memory usage
/compact   # Clean caches and free space
/clean     # Quick cleanup
```

### Smart Skills

```
/review def foo(): pass    # Review code quality
/optimize for i in ...     # Optimize performance
/loophole rate limit       # Find workarounds
```

### Web Tools

```
/search python async       # Search the web
/github python scraper     # Search GitHub
/pypi requests             # Search Python packages
/weather London            # Get weather
```

### Creative Features

```
/story recursion           # Learn as stories
/metaphor database         # Understand with metaphors
/challenge easy            # Get coding challenges
/wisdom                    # Programming wisdom
```

### Get Help

```
/help      # Show all commands
/skills    # List coding skills
/mcp       # List connected services
/who       # Learn about OWURA
/mission   # See our mission
```

---

## Commands

| Command | What it does |
|---------|--------------|
| `/help` | Show all commands |
| `/run <cmd>` | Run a shell command |
| `/ls` | List files |
| `/cat <file>` | View a file |
| `/git <args>` | Run git |
| `/memory` | View memory stats |
| `/compact` | Clean caches |
| `/status` | System status |
| `/review` | Review code quality |
| `/optimize` | Optimize code |
| `/loophole` | Find workarounds |
| `/search` | Search the web |
| `/quit` | Exit OWURA |

---

## Features

### Learns From You
- Remembers what worked
- Stores your preferences
- Tracks your projects
- Remembers errors and solutions

### Built-in Skills
- Python, Node.js, Shell scripting
- Git operations
- File management
- API integration
- Database queries
- Docker
- Security best practices

### Web Tools
- Search the web
- GitHub/PyPI/npm search
- StackOverflow lookup
- Weather, news, Wikipedia

### Smart Skills
- Self-review code
- Self-optimize performance
- Find loopholes for impossible problems
- Reverse engineer code/systems

### Creative Features
- Storytelling for concepts
- Code poetry
- Coding challenges
- Programming wisdom

### Security
- Encrypted API keys
- Privacy-first design
- Auto-cleanup of caches

---

## Uninstall

```bash
rm -rf ~/.owura ~/.local/bin/owura
```

---

## License

Apache License 2.0

---

## Contributing

1. Fork the repo
2. Create a branch
3. Make your changes
4. Submit a pull request

---

**OWURA** - Code Anywhere. Anytime.
