#!/usr/bin/env python3
"""
OWURA - AI Coding Agent for Mobile Terminal
A living, learning assistant that gets smarter with every session.
"""

import os
import sys
import json
import subprocess
import readline
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from rich.theme import Theme
    from rich.text import Text
    from rich.table import Table
    from rich.columns import Columns
    from rich.layout import Layout
    from rich.live import Live
    from rich.align import Align
except ImportError:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from rich.theme import Theme
    from rich.text import Text
    from rich.table import Table
    from rich.columns import Columns
    from rich.layout import Layout
    from rich.live import Live
    from rich.align import Align

from owura.skills import SKILLS, MCP_SERVERS, get_skill_help, get_mcp_help, get_skill_context
from owura.memory import get_memory
from owura.compactor import get_compactor
from owura.security import get_security
from owura.pro import get_pro_tools

# ============================================================
# CONFIGURATION
# ============================================================
CONFIG_DIR = Path.home() / ".owura"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

THEME = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "accent": "bold magenta",
    "muted": "dim",
    "owura": "bold cyan",
})

console = Console(theme=THEME)

# ============================================================
# CONFIG MANAGER
# ============================================================
class Config:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.security = get_security()
        self.data = self.load()
    
    def load(self):
        if self.config_file.exists():
            with open(self.config_file) as f:
                data = json.load(f)
                # Migrate API key to encrypted storage
                if "api_key" in data and data["api_key"]:
                    provider = data.get("provider", "custom")
                    self.security.encrypt_key(provider, data["api_key"])
                    data["api_key"] = ""
                    self.save_data(data)
                return data
        return {
            "provider": "gemini",
            "api_key": "",
            "model": "gemini-2.0-flash",
            "base_url": "",
            "theme": "dark",
            "auto_save": True,
            "max_history": 100,
            "memory_enabled": True,
            "auto_learn": True,
            "privacy_mode": True,
        }
    
    def save(self):
        self.save_data(self.data)
    
    def save_data(self, data):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        # Never save API key to plaintext config
        save_data = {k: v for k, v in data.items() if k != "api_key"}
        with open(self.config_file, "w") as f:
            json.dump(save_data, f, indent=2)
    
    def get(self, key, default=None):
        if key == "api_key":
            # Get from encrypted storage
            provider = self.data.get("provider", "custom")
            return self.security.decrypt_key(provider) or ""
        return self.data.get(key, default)
    
    def set(self, key, value):
        if key == "api_key":
            # Store in encrypted storage
            provider = self.data.get("provider", "custom")
            self.security.encrypt_key(provider, value)
        else:
            self.data[key] = value
            self.save()

# ============================================================
# AI PROVIDER (Enhanced with Memory)
# ============================================================
class AIProvider:
    def __init__(self, config):
        self.config = config
        self.memory = get_memory()
        self.security = get_security()
    
    def chat(self, message, context=None):
        provider = self.config.get("provider")
        api_key = self.config.get("api_key")
        base_url = self.config.get("base_url", "")
        
        if not api_key:
            console.print("[error]No API key configured. Use '/key' to set one.[/error]")
            return None
        
        # Check cache first
        cached = self.security.get_cached_response(message)
        if cached:
            return cached
        
        # Sanitize prompt (strip personal info)
        if self.config.get("privacy_mode", True):
            sanitized, redacted = self.security.sanitize_prompt(message)
            if redacted:
                self.security.log_prompt(provider, message, redacted)
                message = sanitized
        
        # Get skills context
        skill_context = get_skill_context(message)
        
        # Get memory context
        memory_context = ""
        if self.config.get("memory_enabled"):
            memory_context = self.memory.get_full_context()
            
            memory_search = self.memory.search(message)
            if memory_search:
                memory_context += f"\n\n## Relevant from Memory\n{memory_search}"
        
        # Build enhanced system prompt
        system_prompt = self._build_system_prompt(skill_context, memory_context)
        
        # Add privacy notice to system prompt
        system_prompt += "\n\n## Privacy\nDo not store or repeat any personal information (emails, phones, keys, passwords). Keep all user data private."
        
        # Call provider
        if provider == "gemini":
            response = self._gemini_chat(message, api_key, system_prompt)
        elif provider == "custom" or base_url:
            response = self._custom_openai_chat(message, api_key, system_prompt, base_url)
        elif provider == "openai":
            response = self._openai_chat(message, api_key, system_prompt)
        elif provider == "groq":
            response = self._groq_chat(message, api_key, system_prompt)
        elif provider == "nvidia":
            response = self._nvidia_chat(message, api_key, system_prompt)
        else:
            return f"Unknown provider: {provider}"
        
        # Cache response
        if response and not response.startswith("Error"):
            import hashlib
            prompt_hash = hashlib.sha256(message.encode()).hexdigest()[:16]
            self.security.cache_response(prompt_hash, response, provider)
        
        return response
    
    def _build_system_prompt(self, skill_context, memory_context):
        prompt = """You are OWURA, a living AI coding assistant that learns and grows.
You are optimized for mobile terminal use on Android via Termux.

## Core Capabilities
- Write, debug, and explain code in any language
- Execute shell commands and manage files
- Connect to APIs and databases
- Deploy and manage applications
- Learn from every interaction

## Personality
- Be concise but thorough
- Show code with syntax highlighting hints
- Explain what commands do before running
- Suggest improvements and alternatives
- Remember user preferences and patterns

## Response Format
- Use markdown for formatting
- Use code blocks with language tags
- Be direct and actionable
- When unsure, ask for clarification

"""
        if skill_context:
            prompt += skill_context
        if memory_context:
            prompt += f"\n\n## Memory & Context\n{memory_context}"
        
        return prompt
    
    def _gemini_chat(self, message, api_key, system_prompt):
        import urllib.request
        
        model = self.config.get("model", "gemini-2.0-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": message}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096,
            }
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                response_text = result["candidates"][0]["content"]["parts"][0]["text"]
                
                if self.config.get("auto_learn"):
                    self._auto_learn(message, response_text)
                
                return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _openai_chat(self, message, api_key, system_prompt):
        import urllib.request
        
        model = self.config.get("model", "gpt-4")
        url = "https://api.openai.com/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 4096,
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                response_text = result["choices"][0]["message"]["content"]
                
                if self.config.get("auto_learn"):
                    self._auto_learn(message, response_text)
                
                return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _groq_chat(self, message, api_key, system_prompt):
        import urllib.request
        
        model = self.config.get("model", "llama3-70b-8192")
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 4096,
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                response_text = result["choices"][0]["message"]["content"]
                
                if self.config.get("auto_learn"):
                    self._auto_learn(message, response_text)
                
                return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _nvidia_chat(self, message, api_key, system_prompt):
        import urllib.request
        
        model = self.config.get("model", "meta/llama-3.1-70b-instruct")
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 4096,
            "temperature": 0.7,
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                response_text = result["choices"][0]["message"]["content"]
                
                if self.config.get("auto_learn"):
                    self._auto_learn(message, response_text)
                
                return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _custom_openai_chat(self, message, api_key, system_prompt, base_url):
        """Universal OpenAI-compatible API chat. Works with ANY provider."""
        import urllib.request
        
        model = self.config.get("model", "default")
        
        # Ensure base_url ends with /chat/completions
        if not base_url.endswith("/chat/completions"):
            base_url = base_url.rstrip("/") + "/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 4096,
            "temperature": 0.7,
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(base_url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                response_text = result["choices"][0]["message"]["content"]
                
                if self.config.get("auto_learn"):
                    self._auto_learn(message, response_text)
                
                return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _openai_chat(self, message, api_key, system_prompt):
        import urllib.request
        
        model = self.config.get("model", "gpt-4")
        url = "https://api.openai.com/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 4096,
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                response_text = result["choices"][0]["message"]["content"]
                
                if self.config.get("auto_learn"):
                    self._auto_learn(message, response_text)
                
                return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _groq_chat(self, message, api_key, system_prompt):
        import urllib.request
        
        model = self.config.get("model", "llama3-70b-8192")
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 4096,
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                response_text = result["choices"][0]["message"]["content"]
                
                if self.config.get("auto_learn"):
                    self._auto_learn(message, response_text)
                
                return response_text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _auto_learn(self, user_input, response):
        """Automatically learn from conversations."""
        try:
            # Detect code patterns
            if "```" in response:
                # Extract languages used
                import re
                languages = re.findall(r'```(\w+)', response)
                for lang in languages:
                    self.memory.add_pattern("languages", lang, f"Used in conversation")
            
            # Detect project mentions
            project_keywords = ["project", "app", "build", "create", "make"]
            if any(kw in user_input.lower() for kw in project_keywords):
                self.memory.add_fact(f"User wanted to: {user_input[:100]}", "projects")
            
            # Detect errors and solutions
            if "error" in user_input.lower() or "fix" in user_input.lower():
                self.memory.add_learning(
                    f"Problem: {user_input[:80]}",
                    f"Solution approach: {response[:80]}",
                    user_input[:50],
                    "debugging"
                )
            
            # Detect preferences
            if "prefer" in user_input.lower() or "like" in user_input.lower():
                self.memory.add_fact(f"User preference: {user_input[:100]}", "preferences")
            
            self.memory.save_all()
        except:
            pass  # Don't let memory errors break the chat

# ============================================================
# COMMAND PROCESSOR (Enhanced)
# ============================================================
class CommandProcessor:
    def __init__(self, config, ai):
        self.config = config
        self.ai = ai
        self.memory = get_memory()
        self.compactor = get_compactor()
        self.history = []
    
    def process(self, user_input):
        """Process user input and return response."""
        # Check for commands
        if user_input.startswith("/"):
            return self.handle_command(user_input)
        
        # Send to AI
        response = self.ai.chat(user_input)
        return response
    
    def handle_command(self, cmd):
        """Handle slash commands."""
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        commands = {
            "/help": self.cmd_help,
            "/config": self.cmd_config,
            "/provider": self.cmd_provider,
            "/model": self.cmd_model,
            "/key": self.cmd_key,
            "/clear": self.cmd_clear,
            "/history": self.cmd_history,
            "/run": self.cmd_run,
            "/exec": self.cmd_run,
            "/file": self.cmd_file,
            "/ls": self.cmd_ls,
            "/pwd": self.cmd_pwd,
            "/cd": self.cmd_cd,
            "/cat": self.cmd_cat,
            "/git": self.cmd_git,
            "/skills": self.cmd_skills,
            "/mcp": self.cmd_mcp,
            "/memory": self.cmd_memory,
            "/remember": self.cmd_remember,
            "/recall": self.cmd_recall,
            "/project": self.cmd_project,
            "/learn": self.cmd_learn,
            "/suggest": self.cmd_suggest,
            "/template": self.cmd_template,
            "/compact": self.cmd_compact,
            "/status": self.cmd_status,
            "/clean": self.cmd_clean,
            "/privacy": self.cmd_privacy,
            "/create": self.cmd_create,
            "/analyze": self.cmd_analyze,
            "/generate": self.cmd_generate,
            "/deploy": self.cmd_deploy,
            "/test": self.cmd_test,
            "/version": self.cmd_version,
            "/quit": self.cmd_quit,
            "/exit": self.cmd_quit,
            "/q": self.cmd_quit,
        }
        
        if command in commands:
            return commands[command](args)
        else:
            return f"Unknown command: {command}. Type /help for available commands."
    
    def cmd_help(self, args):
        help_text = """
## OWURA Commands

### Basic
| Command | Description |
|---------|-------------|
| `/help` | Show this help |
| `/config` | Open configuration |
| `/clear` | Clear screen |
| `/version` | Show version |
| `/quit` | Exit OWURA |

### AI & Providers
| Command | Description |
|---------|-------------|
| `/provider <name>` | Set AI provider (gemini/openai/groq) |
| `/model <name>` | Set AI model |
| `/key <api_key>` | Set API key |

### Files & Code
| Command | Description |
|---------|-------------|
| `/run <cmd>` | Execute shell command |
| `/ls [path]` | List directory |
| `/pwd` | Show current directory |
| `/cd <path>` | Change directory |
| `/cat <file>` | Show file contents |
| `/git <args>` | Run git command |

### Memory & Learning
| Command | Description |
|---------|-------------|
| `/memory` | Show memory stats |
| `/remember <fact>` | Store a fact |
| `/recall <query>` | Search memory |
| `/project <name>` | Record a project |
| `/learn <what> -> <outcome>` | Record a learning |

### Skills & MCPs
| Command | Description |
|---------|-------------|
| `/skills` | List available skills |
| `/mcp` | List MCP servers |
| `/suggest` | Get smart suggestions |
| `/template <type>` | Get project template |

### System Management
| Command | Description |
|---------|-------------|
| `/status` | Show system status |
| `/compact` | Run full compaction |
| `/clean` | Quick cache cleanup |

### History
| Command | Description |
|---------|-------------|
| `/history` | Show command history |
"""
        return help_text
    
    def cmd_config(self, args):
        table = Table(title="Current Configuration", show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in self.config.data.items():
            if key == "api_key":
                display = value[:8] + "..." if value else "(not set)"
            else:
                display = str(value)
            table.add_row(key, display)
        
        # Add memory stats
        table.add_row("---", "---")
        table.add_row("facts_stored", str(len(self.memory.memory.get("facts", []))))
        table.add_row("learnings_stored", str(len(self.memory.learnings)))
        table.add_row("patterns_stored", str(sum(len(v) for v in self.memory.patterns.values())))
        
        console.print(table)
        return None
    
    def cmd_provider(self, args):
        if not args:
            return """Available providers:

  gemini   - Google AI Studio (free tier)
  openai   - OpenAI
  groq     - Groq (fast inference)
  nvidia   - NVIDIA NIM
  custom   - Any OpenAI-compatible API

Usage:
  /provider gemini
  /provider custom https://api.example.com/v1
  /provider custom https://api.together.xyz/v1

Supported OpenAI-compatible APIs:
  - OpenRouter (https://openrouter.ai/api/v1)
  - Together AI (https://api.together.xyz/v1)
  - Fireworks (https://api.fireworks.ai/inference/v1)
  - DeepInfra (https://api.deepinfra.com/v1/openai)
  - Groq (https://api.groq.com/openai/v1)
  - NVIDIA NIM (https://integrate.api.nvidia.com/v1)
  - Any local LLM (http://localhost:11434/v1)"""
        
        parts = args.split(maxsplit=1)
        provider = parts[0].lower()
        base_url = parts[1] if len(parts) > 1 else ""
        
        valid = ["gemini", "openai", "groq", "nvidia", "custom"]
        if provider not in valid:
            return f"Invalid provider. Choose from: {', '.join(valid)}"
        
        if provider == "custom" and not base_url:
            return "Usage: /provider custom <base_url>\nExample: /provider custom https://api.together.xyz/v1"
        
        self.config.set("provider", provider)
        if base_url:
            self.config.set("base_url", base_url)
        
        defaults = {
            "gemini": "gemini-2.0-flash",
            "openai": "gpt-4",
            "groq": "llama3-70b-8192",
            "nvidia": "meta/llama-3.1-70b-instruct",
            "custom": "default",
        }
        self.config.set("model", defaults.get(provider, "default"))
        
        self.memory.set_preference("provider", provider)
        
        if provider == "custom":
            return f"Custom provider set!\nBase URL: {base_url}\nModel: default\n\nUse /model <name> to set the model."
        return f"Provider set to {provider}. Model: {self.config.get('model')}"
    
    def cmd_model(self, args):
        if not args:
            return f"Current model: {self.config.get('model')}"
        
        self.config.set("model", args)
        return f"Model set to {args}"
    
    def cmd_key(self, args):
        if not args:
            key = self.config.get("api_key")
            if key:
                return f"API key: {key[:8]}...{key[-4:]}"
            return "No API key set"
        
        self.config.set("api_key", args)
        return "API key saved!"
    
    def cmd_clear(self, args):
        console.clear()
        return None
    
    def cmd_history(self, args):
        if not self.history:
            return "No history yet."
        
        table = Table(title="History", show_header=True, header_style="bold cyan")
        table.add_column("#", style="muted")
        table.add_column("Input", style="cyan")
        table.add_column("Time", style="muted")
        
        for i, entry in enumerate(self.history[-20:], 1):
            table.add_row(str(i), entry["input"][:50], entry["time"])
        
        console.print(table)
        return None
    
    def cmd_run(self, args):
        if not args:
            return "Usage: /run <command>"
        
        # Auto-compact before heavy operations
        self.compactor.auto_compact(threshold_percent=85)
        
        try:
            result = subprocess.run(
                args, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[error]{result.stderr}[/error]"
            
            # Learn from execution
            if result.returncode == 0:
                self.memory.add_pattern("commands", args, "Successful execution")
            else:
                self.memory.add_learning(
                    f"Command failed: {args}",
                    f"Exit code: {result.returncode}",
                    args, "commands"
                )
            
            return output or "Command executed (no output)"
        except subprocess.TimeoutExpired:
            return "Command timed out (30s limit)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def cmd_ls(self, args):
        path = args if args else "."
        try:
            items = list(Path(path).iterdir())
            items.sort(key=lambda x: (not x.is_dir(), x.name))
            
            table = Table(show_header=False, show_lines=False, show_edge=False)
            table.add_column("Name")
            
            for item in items[:30]:
                name = item.name
                if item.is_dir():
                    table.add_row(f"[bold blue]{name}/[/bold blue]")
                elif name.endswith(('.py', '.js', '.ts', '.sh', '.go', '.rs')):
                    table.add_row(f"[bold green]{name}[/bold green]")
                elif name.endswith(('.md', '.txt', '.json', '.yaml')):
                    table.add_row(f"[bold yellow]{name}[/bold yellow]")
                else:
                    table.add_row(name)
            
            console.print(table)
            return None
        except Exception as e:
            return f"Error: {str(e)}"
    
    def cmd_pwd(self, args):
        return str(Path.cwd())
    
    def cmd_cd(self, args):
        if not args:
            return str(Path.cwd())
        try:
            os.chdir(args)
            return f"Now in: {Path.cwd()}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def cmd_cat(self, args):
        if not args:
            return "Usage: /cat <file>"
        try:
            with open(args) as f:
                content = f.read()
            
            ext = Path(args).suffix.lower()
            lang_map = {
                ".py": "python", ".js": "javascript", ".ts": "typescript",
                ".sh": "bash", ".bash": "bash", ".json": "json",
                ".yaml": "yaml", ".yml": "yaml", ".md": "markdown",
                ".rs": "rust", ".go": "go", ".java": "java",
                ".c": "c", ".cpp": "cpp", ".h": "c",
            }
            lang = lang_map.get(ext, "")
            
            if lang:
                syntax = Syntax(content, lang, theme="monokai", line_numbers=True)
                console.print(syntax)
            else:
                console.print(content)
            return None
        except Exception as e:
            return f"Error: {str(e)}"
    
    def cmd_git(self, args):
        if not args:
            return "Usage: /git <args> (e.g., /git status)"
        return self.cmd_run(f"git {args}")
    
    def cmd_skills(self, args):
        table = Table(title="Available Skills", show_header=True, header_style="bold cyan")
        table.add_column("Skill", style="green")
        table.add_column("Description", style="white")
        table.add_column("Triggers", style="muted")
        
        for key, skill in SKILLS.items():
            table.add_row(key, skill["description"][:40], ", ".join(skill["trigger"][:3]))
        
        console.print(table)
        return None
    
    def cmd_mcp(self, args):
        table = Table(title="MCP Servers", show_header=True, header_style="bold cyan")
        table.add_column("Server", style="green")
        table.add_column("Description", style="white")
        
        for key, mcp in MCP_SERVERS.items():
            table.add_row(key, mcp["description"])
        
        console.print(table)
        return None
    
    def cmd_memory(self, args):
        stats = Table(title="Memory Statistics", show_header=True, header_style="bold cyan")
        stats.add_column("Metric", style="cyan")
        stats.add_column("Value", style="green")
        
        stats.add_row("Facts Stored", str(len(self.memory.memory.get("facts", []))))
        stats.add_row("Learnings", str(len(self.memory.learnings)))
        stats.add_row("Patterns", str(sum(len(v) for v in self.memory.patterns.values())))
        stats.add_row("Projects", str(len(self.memory.projects.get("completed", []))))
        stats.add_row("Preferences", str(len(self.memory.memory.get("preferences", {}))))
        
        console.print(stats)
        
        # Show recent learnings
        learnings = self.memory.get_learnings()
        if learnings:
            console.print("\n[bold]Recent Learnings:[/bold]")
            for l in learnings[-5:]:
                console.print(f"  [muted]-[/muted] {l}")
        
        return None
    
    def cmd_remember(self, args):
        if not args:
            return "Usage: /remember <fact>"
        
        self.memory.add_fact(args, "user")
        return f"Remembered: {args}"
    
    def cmd_recall(self, args):
        if not args:
            return "Usage: /recall <query>"
        
        results = self.memory.search(args)
        if results:
            return results
        return f"No memories found for: {args}"
    
    def cmd_project(self, args):
        if not args:
            # Show projects
            table = Table(title="Projects", show_header=True, header_style="bold cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Tech", style="muted")
            
            for p in self.memory.projects.get("completed", []):
                table.add_row(p["name"], "completed", ", ".join(p.get("tech_stack", [])[:3]))
            for p in self.memory.projects.get("in_progress", []):
                table.add_row(p["name"], "in progress", ", ".join(p.get("tech_stack", [])[:3]))
            
            console.print(table)
            return None
        
        # Record a project interactively
        console.print("[info]Recording project...[/info]")
        desc = Prompt.ask("Description")
        tech = Prompt.ask("Tech stack (comma-separated)")
        learnings = Prompt.ask("Key learnings (comma-separated)")
        
        self.memory.add_project(
            name=args,
            description=desc,
            tech_stack=[t.strip() for t in tech.split(",")],
            status="completed",
            learnings=[l.strip() for l in learnings.split(",")]
        )
        
        return f"Project '{args}' recorded!"
    
    def cmd_learn(self, args):
        if not args or " -> " not in args:
            return "Usage: /learn <what> -> <outcome>"
        
        parts = args.split(" -> ", 1)
        self.memory.add_learning(parts[0], parts[1], "", "general")
        return f"Learning recorded: {parts[0]} -> {parts[1]}"
    
    def cmd_suggest(self, args):
        """Get smart suggestions based on context."""
        suggestions = []
        
        # Check current directory
        cwd = Path.cwd()
        files = list(cwd.iterdir())
        
        if any(f.name == "package.json" for f in files):
            suggestions.append("Node.js project detected. Try: /run npm install")
        
        if any(f.name == "requirements.txt" for f in files):
            suggestions.append("Python project detected. Try: /run pip install -r requirements.txt")
        
        if any(f.name == "Cargo.toml" for f in files):
            suggestions.append("Rust project detected. Try: /run cargo build")
        
        if any(f.name == "go.mod" for f in files):
            suggestions.append("Go project detected. Try: /run go build")
        
        # Check memory for patterns
        recent_learnings = self.memory.get_learnings()
        if recent_learnings:
            suggestions.append(f"You have {len(recent_learnings)} stored learnings. Try: /memory")
        
        # Check git
        if (cwd / ".git").exists():
            suggestions.append("Git repo detected. Try: /git status")
        
        if not suggestions:
            suggestions.append("No specific suggestions. Try: /skills to see what I can do!")
        
        return "\n".join([f"- {s}" for s in suggestions])
    
    def cmd_template(self, args):
        """Get project templates."""
        templates = {
            "python": '''#!/usr/bin/env python3
"""Project: {name}"""

def main():
    print("Hello from {name}!")

if __name__ == "__main__":
    main()
''',
            "flask": '''from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from {name}!"

if __name__ == "__main__":
    app.run(debug=True)
''',
            "express": '''const express = require("express");
const app = express();

app.get("/", (req, res) => {
    res.send("Hello from {name}!");
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
''',
            "cli": '''#!/usr/bin/env python3
"""CLI Tool: {name}"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="{name}")
    parser.add_argument("command", help="Command to run")
    args = parser.parse_args()
    
    print(f"Running: {args.command}")

if __name__ == "__main__":
    main()
''',
        }
        
        if not args or args not in templates:
            return f"Available templates: {', '.join(templates.keys())}"
        
        name = Prompt.ask("Project name")
        return f"```{args}\n{templates[args].format(name=name)}\n```"
    
    def cmd_compact(self, args):
        """Run full system compaction."""
        console.print("[yellow]Running full compaction...[/yellow]")
        
        # Auto-compact before heavy operations
        with console.status("[muted]Cleaning caches and optimizing...[/muted]"):
            result = self.compactor.full_compaction()
        
        # Display results
        table = Table(title="Compaction Complete", show_header=True, header_style="bold green")
        table.add_column("Metric", style="cyan")
        table.add_column("Before", style="yellow")
        table.add_column("After", style="green")
        
        table.add_row(
            "Disk Used",
            f"{result['disk_before']['used_gb']}GB ({result['disk_before']['percent_used']}%)",
            f"{result['disk_after']['used_gb']}GB ({result['disk_after']['percent_used']}%)"
        )
        table.add_row(
            "Memory Used",
            f"{result['memory_before']['used_mb']}MB ({result['memory_before']['percent_used']}%)",
            f"{result['memory_after']['used_mb']}MB ({result['memory_after']['percent_used']}%)"
        )
        table.add_row(
            "Disk Freed",
            f"{result['disk_freed_gb']}GB",
            "âœ“"
        )
        
        console.print(table)
        
        # Show what was cleaned
        if result['cleaned']:
            console.print("\n[bold]Cleaned:[/bold]")
            for source, size in result['cleaned'].items():
                if size and size > 0:
                    console.print(f"  âœ“ {source}: {self.compactor._format_size(size)}")
        
        return None
    
    def cmd_status(self, args):
        """Show system status."""
        status = self.compactor.get_status()
        return status
    
    def cmd_clean(self, args):
        """Quick cache cleanup."""
        console.print("[yellow]Quick cleanup...[/yellow]")
        
        with console.status("[muted]Cleaning...[/muted]"):
            # Quick cleanup
            self.compactor.cleanup_pip()
            self.compactor.cleanup_npm()
            self.compactor.cleanup_temp()
            self.compactor.cleanup_pycache()
        
        disk = self.compactor.get_disk_usage()
        console.print(f"[green]Done! Disk: {disk['free_gb']}GB free ({disk['percent_used']}% used)[/green]")
        
        return None
    
    def cmd_privacy(self, args):
        """Show privacy status and controls."""
        security = get_security()
        
        table = Table(title="Privacy Status", show_header=True, header_style="bold green")
        table.add_column("Feature", style="cyan")
        table.add_column("Status", style="green")
        
        privacy_mode = self.config.get("privacy_mode", True)
        table.add_row("Privacy Mode", "ON" if privacy_mode else "OFF")
        table.add_row("API Keys", "Encrypted at rest")
        table.add_row("Prompt Sanitization", "Strips emails, phones, keys, passwords")
        table.add_row("Response Caching", "Local only, no data sent to providers")
        table.add_row("Prompt Logging", "Hash-only audit trail")
        
        console.print(table)
        
        # Show privacy report
        report = security.get_privacy_report()
        console.print(f"\n{report}")
        
        return None
    
    def cmd_create(self, args):
        """Create a new project from template."""
        pro = get_pro_tools()
        
        templates = ["flask-api", "fastapi", "react", "express", "django", "nextjs", "python-cli", "rust-cli", "go-api"]
        
        if not args:
            return f"Usage: /create <template> <name>\n\nAvailable templates:\n" + "\n".join([f"  - {t}" for t in templates])
        
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: /create <template> <name>\nExample: /create flask-api myapp"
        
        template = parts[0]
        name = parts[1]
        
        if template not in templates:
            return f"Unknown template: {template}\nAvailable: {', '.join(templates)}"
        
        console.print(f"[yellow]Creating {template} project: {name}...[/yellow]")
        
        with console.status("[muted]Setting up project...[/muted]"):
            result = pro.create_project(name, template)
        
        if result.get("success"):
            console.print(f"[green]Project created![/green]")
            console.print(f"  Path: {result['path']}")
            console.print(f"  Template: {result['template']}")
            console.print(f"\n  cd {result['path']}")
            return None
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    
    def cmd_analyze(self, args):
        """Analyze current project."""
        pro = get_pro_tools()
        
        path = args if args else "."
        
        with console.status("[muted]Analyzing project...[/muted]"):
            analysis = pro.analyze_project(path)
        
        table = Table(title="Project Analysis", show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Files", str(analysis["files"]))
        table.add_row("Languages", ", ".join(analysis["languages"]) or "None detected")
        table.add_row("Has Tests", "Yes" if analysis["has_tests"] else "No")
        table.add_row("Has Docker", "Yes" if analysis["has_docker"] else "No")
        table.add_row("Has CI/CD", "Yes" if analysis["has_ci"] else "No")
        table.add_row("Has Docs", "Yes" if analysis["has_docs"] else "No")
        
        console.print(table)
        
        if analysis["suggestions"]:
            console.print("\n[bold]Suggestions:[/bold]")
            for s in analysis["suggestions"]:
                console.print(f"  - {s}")
        
        return None
    
    def cmd_generate(self, args):
        """Generate code or tests."""
        pro = get_pro_tools()
        
        if not args:
            return "Usage: /generate <type> <file>\n\nTypes: tests, migration, deploy"
        
        parts = args.split(maxsplit=1)
        gen_type = parts[0]
        target = parts[1] if len(parts) > 1 else "."
        
        if gen_type == "tests":
            result = pro.generate_tests(target)
            console.print(Syntax(result, "python", theme="monokai"))
        elif gen_type == "deploy":
            result = pro.generate_deploy_config("docker", "app")
            console.print(Syntax(result, "yaml", theme="monokai"))
        else:
            return f"Unknown generation type: {gen_type}"
        
        return None
    
    def cmd_deploy(self, args):
        """Generate deployment config."""
        pro = get_pro_tools()
        
        platforms = ["docker", "heroku", "railway", "vercel"]
        
        if not args:
            return f"Usage: /deploy <platform>\n\nPlatforms: {', '.join(platforms)}"
        
        if args not in platforms:
            return f"Unknown platform: {args}\nAvailable: {', '.join(platforms)}"
        
        result = pro.generate_deploy_config(args, "app")
        console.print(Syntax(result, "yaml" if args != "heroku" else "bash", theme="monokai"))
        
        return None
    
    def cmd_test(self, args):
        """Run tests."""
        if not args:
            return "Usage: /test <file_or_directory>"
        
        try:
            result = subprocess.run(
                f"python -m pytest {args} -v",
                shell=True, capture_output=True, text=True, timeout=60
            )
            output = result.stdout
            if result.stderr:
                output += f"\n{result.stderr}"
            return output or "Tests completed"
        except subprocess.TimeoutExpired:
            return "Tests timed out (60s limit)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def cmd_version(self, args):
        from owura import __version__
        return f"OWURA v{__version__} - AI Coding Agent"
    
    def cmd_quit(self, args):
        # Save learnings before exit
        self.memory.save_all()
        raise SystemExit

# ============================================================
# MAIN TUI (Enhanced)
# ============================================================
def print_banner():
    banner = """
[bold cyan]
  ___   _   _  _   _  ___   ___ 
 / _ \\ | | | || | | | / _ \\ / _ \\
| | | || | | || | | || | | | (_) |
| |_| || |_| || |_| || |_| | \\__, |
 \\___/  \\__, | \\___/  \\___/    /_/
         __/ |                    
        |___/                     
[/bold cyan]
[dim]v1.0 - AI Coding Agent - Code Anywhere. Anytime.[/dim]
[dim]Memory: ON | Learning: ON | Skills: {skills} | MCPs: {mcps}[/dim]
""".format(skills=len(SKILLS), mcps=len(MCP_SERVERS))
    console.print(banner)

def main():
    """Main entry point."""
    # Initialize
    config = Config()
    ai = AIProvider(config)
    processor = CommandProcessor(config, ai)
    memory = get_memory()
    
    # Check if first run
    if not config.get("api_key"):
        console.print("[bold]Welcome to OWURA![/bold]")
        console.print("[info]Let's set up your AI provider.[/info]")
        console.print()
        console.print("[muted]Available providers:[/muted]")
        console.print("  [cyan]gemini[/cyan]  - Google Gemini (free tier available)")
        console.print("  [cyan]openai[/cyan]  - OpenAI GPT-4")
        console.print("  [cyan]groq[/cyan]    - Groq (fast inference)")
        console.print()
        
        provider = Prompt.ask("Choose provider", choices=["gemini", "openai", "groq"], default="gemini")
        config.set("provider", provider)
        
        defaults = {"gemini": "gemini-2.0-flash", "openai": "gpt-4", "groq": "llama3-70b-8192"}
        config.set("model", defaults.get(provider))
        
        api_key = Prompt.ask(f"Enter your {provider} API key")
        config.set("api_key", api_key)
        
        # Store preference
        memory.set_preference("provider", provider)
        
        console.print("[success]Configuration saved![/success]")
        console.print()
    
    # Print banner
    print_banner()
    
    # Show memory stats if enabled
    if config.get("memory_enabled") and memory.memory.get("facts"):
        console.print(f"[muted]Memory: {len(memory.memory['facts'])} facts, {len(memory.learnings)} learnings loaded[/muted]")
    
    console.print("[muted]Type /help for commands, /quit to exit[/muted]")
    console.print()
    
    # Main loop
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]owura[/bold cyan]")
            
            if not user_input.strip():
                continue
            
            # Add to history
            entry = {
                "input": user_input,
                "time": datetime.now().strftime("%H:%M:%S"),
            }
            processor.history.append(entry)
            
            # Process
            with console.status("[muted]Thinking...[/muted]"):
                response = processor.process(user_input)
            
            # Display response
            if response:
                console.print()
                try:
                    console.print(Markdown(response))
                except:
                    console.print(response)
                console.print()
            
            # Save history
            try:
                history_file = HISTORY_FILE
                history_file.parent.mkdir(parents=True, exist_ok=True)
                with open(history_file, "w") as f:
                    json.dump(processor.history[-config.get("max_history", 100):], f)
            except:
                pass
        
        except SystemExit:
            console.print("[info]Memory saved. Goodbye![/info]")
            break
        except KeyboardInterrupt:
            console.print("\n[muted]Use /quit to exit[/muted]")
        except Exception as e:
            console.print(f"[error]Error: {str(e)}[/error]")

if __name__ == "__main__":
    main()
