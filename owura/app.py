#!/usr/bin/env python3
"""
OWURA - AI Coding Agent for Mobile Terminal
A living, learning assistant that gets smarter with every session.
"""

import os
import sys
import json
import hashlib
import re
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import readline
except ImportError:
    pass

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from rich.theme import Theme
    from rich.table import Table
except ImportError:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from rich.theme import Theme
    from rich.table import Table

from owura.skills import SKILLS, MCP_SERVERS, get_skill_context
from owura.memory import get_memory
from owura.compactor import get_compactor
from owura.security import get_security
from owura.pro import get_pro_tools
from owura.creative import get_creative
from owura.web import get_web
from owura.smart import get_smart
from owura.loophole import get_loophole
from owura.creativity import get_creativity
from owura.awareness import get_awareness

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
# MODEL FETCHING
# ============================================================
PROVIDER_API_URLS = {
    "openai": "https://api.openai.com/v1",
    "groq": "https://api.groq.com/openai/v1",
    "nvidia": "https://integrate.api.nvidia.com/v1",
    "together": "https://api.together.xyz/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "mistral": "https://api.mistral.ai/v1",
    "perplexity": "https://api.perplexity.ai",
    "fireworks": "https://api.fireworks.ai/inference/v1",
    "cohere": "https://api.cohere.ai/v1",
    "xai": "https://api.x.ai/v1",
    "github": "https://models.inference.ai.azure.com",
    "anthropic": "https://api.anthropic.com/v1",
}

PROVIDER_NAMES = {
    "gemini": "Google Gemini",
    "openai": "OpenAI",
    "groq": "Groq",
    "nvidia": "NVIDIA NIM",
    "together": "Together AI",
    "openrouter": "OpenRouter",
    "deepseek": "DeepSeek",
    "mistral": "Mistral AI",
    "perplexity": "Perplexity",
    "fireworks": "Fireworks AI",
    "cohere": "Cohere",
    "xai": "xAI (Grok)",
    "github": "GitHub Models",
    "anthropic": "Anthropic",
    "custom": "Custom (OpenAI-compatible)",
}


def fetch_available_models(provider, api_key, base_url=""):
    """Fetch available models from a provider's API. Returns list of model IDs or None on failure."""
    import urllib.request
    try:
        if provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                models = [m["name"].replace("models/", "") for m in data.get("models", [])]
                models = [m for m in models if "generation" in m or "chat" in m or "gemini" in m]
                return models

        api_base = base_url if base_url else PROVIDER_API_URLS.get(provider, "")
        if not api_base:
            return None

        if provider == "anthropic" and not base_url:
            url = f"{api_base}/models"
            req = urllib.request.Request(url, headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                models = [m["id"] for m in data.get("data", [])]
                return models

        url = api_base.rstrip("/") + "/models"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            models = [m["id"] for m in data.get("data", [])]
            if not models:
                models = [m["id"] for m in data.get("models", [])]
            return models

    except Exception:
        return None


# ============================================================
# CONFIGURATION
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
        save_data = {k: v for k, v in data.items() if k != "api_key"}
        with open(self.config_file, "w") as f:
            json.dump(save_data, f, indent=2)

    def get(self, key, default=None):
        if key == "api_key":
            provider = self.data.get("provider", "custom")
            return self.security.decrypt_key(provider) or ""
        return self.data.get(key, default)

    def set(self, key, value):
        if key == "api_key":
            provider = self.data.get("provider", "custom")
            self.security.encrypt_key(provider, value)
        else:
            self.data[key] = value
            self.save()


# ============================================================
# AI PROVIDER
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

        cached = self.security.get_cached_response(message)
        if cached:
            return cached

        if self.config.get("privacy_mode", True):
            sanitized, redacted = self.security.sanitize_prompt(message)
            if redacted:
                self.security.log_prompt(provider, message, redacted)
                message = sanitized

        skill_context = get_skill_context(message)
        memory_context = ""
        if self.config.get("memory_enabled"):
            memory_context = self.memory.get_full_context()
            memory_search = self.memory.search(message)
            if memory_search:
                memory_context += f"\n\n## Relevant from Memory\n{memory_search}"

        system_prompt = self._build_system_prompt(skill_context, memory_context)
        system_prompt += "\n\n## Privacy\nDo not store or repeat any personal information. Keep all user data private."

        if provider == "gemini":
            response = self._call_gemini(message, api_key, system_prompt)
        elif provider in ("openai", "groq", "nvidia") or base_url:
            response = self._call_openai_compatible(message, api_key, system_prompt, provider, base_url)
        else:
            response = f"Unknown provider: {provider}"

        if response and not response.startswith("Error"):
            prompt_hash = hashlib.sha256(message.encode()).hexdigest()[:16]
            self.security.cache_response(prompt_hash, response, provider)

        return response

    def _build_system_prompt(self, skill_context, memory_context):
        prompt = """You are OWURA, an AI coding agent.
You are optimized for terminal use on mobile (Termux) and desktop.

## Core Capabilities
- Write, debug, and explain code in any language
- Execute shell commands and manage files
- Scaffold complete production projects from a description
- Set up Docker, CI/CD, databases, tests, monitoring
- Connect to APIs and manage deployments
- Learn from every interaction

## Building Software
When someone describes what they want to build:
- Think about real production use, not prototypes
- Include proper error handling, logging, security, and testing
- Set up containerization and deployment from the start
- Use the /build command for project scaffolding
- Scaffold projects that work at scale (caching, connection pooling, rate limiting)

## Personality
- Be concise but thorough
- Show code with syntax highlighting hints
- Explain what commands do before running
- Suggest improvements and alternatives
- Remember user preferences and patterns
- Meet the user where they are — beginners get more guidance, experts get concise answers

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

    def _call_gemini(self, message, api_key, system_prompt):
        import urllib.request
        model = self.config.get("model", "gemini-2.0-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": message}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode())
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                if self.config.get("auto_learn"):
                    self._auto_learn(message, text)
                return text
        except Exception as e:
            return f"Error: {e}"

    def _call_openai_compatible(self, message, api_key, system_prompt, provider, base_url=""):
        import urllib.request
        model_defaults = {
            "openai": ("gpt-4o", "https://api.openai.com/v1/chat/completions"),
            "groq": ("llama-3.3-70b-versatile", "https://api.groq.com/openai/v1/chat/completions"),
            "nvidia": ("meta/llama-3.1-70b-instruct", "https://integrate.api.nvidia.com/v1/chat/completions"),
            "together": ("mistralai/Mixtral-8x7B-Instruct-v0.1", "https://api.together.xyz/v1/chat/completions"),
            "openrouter": ("mistralai/mistral-7b-instruct", "https://openrouter.ai/api/v1/chat/completions"),
            "deepseek": ("deepseek-chat", "https://api.deepseek.com/v1/chat/completions"),
            "mistral": ("mistral-small-latest", "https://api.mistral.ai/v1/chat/completions"),
            "perplexity": ("llama-3-sonar-small-32k-chat", "https://api.perplexity.ai/chat/completions"),
            "fireworks": ("accounts/fireworks/models/llama-v3p1-8b-instruct", "https://api.fireworks.ai/inference/v1/chat/completions"),
            "cohere": ("command-r-plus", "https://api.cohere.ai/v1/chat/completions"),
            "xai": ("grok-beta", "https://api.x.ai/v1/chat/completions"),
            "github": ("gpt-4o", "https://models.inference.ai.azure.com/chat/completions"),
        }
        default_model, default_url = model_defaults.get(provider, ("default", base_url))
        model = self.config.get("model", default_model)
        url = base_url if base_url else default_url
        if not url.endswith("/chat/completions"):
            url = url.rstrip("/") + "/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            "max_tokens": 4096,
            "temperature": 0.7,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode())
                text = result["choices"][0]["message"]["content"]
                if self.config.get("auto_learn"):
                    self._auto_learn(message, text)
                return text
        except Exception as e:
            return f"Error: {e}"

    def _auto_learn(self, user_input, response):
        try:
            if "```" in response:
                languages = re.findall(r"```(\w+)", response)
                for lang in languages:
                    self.memory.add_pattern("languages", lang, "Used in conversation")
            project_keywords = ["project", "app", "build", "create", "make"]
            if any(kw in user_input.lower() for kw in project_keywords):
                self.memory.add_fact(f"User wanted to: {user_input[:100]}", "projects")
            if "error" in user_input.lower() or "fix" in user_input.lower():
                self.memory.add_learning(
                    f"Problem: {user_input[:80]}",
                    f"Solution approach: {response[:80]}",
                    user_input[:50],
                    "debugging",
                )
            if "prefer" in user_input.lower() or "like" in user_input.lower():
                self.memory.add_fact(f"User preference: {user_input[:100]}", "preferences")
            self.memory.save_all()
        except Exception:
            pass


# ============================================================
# COMMAND PROCESSOR
# ============================================================
class CommandProcessor:
    def __init__(self, config, ai):
        self.config = config
        self.ai = ai
        self.memory = get_memory()
        self.compactor = get_compactor()
        self.smart = get_smart()
        self.history = []

    def process(self, user_input):
        if user_input.startswith("/"):
            return self.handle_command(user_input)

        creativity = get_creativity()
        easter_egg = creativity.check_easter_egg(user_input)
        if easter_egg:
            return easter_egg

        mood = creativity.detect_mood(user_input)
        mood_response = creativity.get_mood_response(mood)

        code = None
        if "```" in user_input:
            code_match = re.search(r"```[\w]*\n(.*?)```", user_input, re.DOTALL)
            if code_match:
                code = code_match.group(1)

        smart_result = self.smart.handle_auto_skill(user_input, code)
        if smart_result:
            return smart_result

        response = self.ai.chat(user_input)
        if mood_response:
            response = f"*{mood_response}*\n\n{response}"
        return response

    def handle_command(self, cmd):
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        commands = {
            "/help": self.cmd_help,
            "/config": self.cmd_config,
            "/provider": self.cmd_provider,
            "/model": self.cmd_model,
            "/key": self.cmd_key,
            "/build": self.cmd_build,
            "/clear": self.cmd_clear,
            "/history": self.cmd_history,
            "/run": self.cmd_run,
            "/exec": self.cmd_run,
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
            "/error": self.cmd_error,
            "/save": self.cmd_save,
            "/snippets": self.cmd_snippets,
            "/commit": self.cmd_commit,
            "/api": self.cmd_api,
            "/usage": self.cmd_usage,
            "/json": self.cmd_json,
            "/regex": self.cmd_regex,
            "/color": self.cmd_color,
            "/sysinfo": self.cmd_sysinfo,
            "/ascii": self.cmd_ascii,
            "/search": self.cmd_search,
            "/github": self.cmd_github,
            "/pypi": self.cmd_pypi,
            "/npm": self.cmd_npm_search,
            "/so": self.cmd_stackoverflow,
            "/wiki": self.cmd_wikipedia,
            "/news": self.cmd_news,
            "/weather": self.cmd_weather,
            "/ip": self.cmd_ip,
            "/fetch": self.cmd_fetch,
            "/docs": self.cmd_docs,
            "/review": self.cmd_review,
            "/optimize": self.cmd_optimize,
            "/reverse": self.cmd_reverse,
            "/loophole": self.cmd_loophole,
            "/fix": self.cmd_fix,
            "/free": self.cmd_free,
            "/story": self.cmd_story,
            "/metaphor": self.cmd_metaphor,
            "/name": self.cmd_name,
            "/poem": self.cmd_poem,
            "/challenge": self.cmd_challenge,
            "/wisdom": self.cmd_wisdom,
            "/mood": self.cmd_mood,
            "/who": self.cmd_who,
            "/mission": self.cmd_mission,
            "/why": self.cmd_why,
            "/version": self.cmd_version,
            "/quit": self.cmd_quit,
            "/exit": self.cmd_quit,
            "/q": self.cmd_quit,
        }

        if command in commands:
            return commands[command](args)
        return f"Unknown command: {command}. Type /help for available commands."

    # ---- Basic ----
    def cmd_help(self, args):
        return """
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
| `/provider [name]` | Set AI provider — interactive, fetches models live from API (15+ providers) |
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

### System
| Command | Description |
|---------|-------------|
| `/status` | Show system status |
| `/compact` | Run full compaction |
| `/clean` | Quick cache cleanup |

### Web & Search
| Command | Description |
|---------|-------------|
| `/search <query>` | Search the web |
| `/github <query>` | Search GitHub |
| `/pypi <package>` | Search PyPI |
| `/npm <package>` | Search npm |
| `/so <query>` | Search StackOverflow |
| `/wiki <topic>` | Wikipedia lookup |
| `/weather <city>` | Get weather |
| `/news [topic]` | Get latest news |

### Creative
| Command | Description |
|---------|-------------|
| `/story <concept>` | Learn as stories |
| `/metaphor <concept>` | Understand with metaphors |
| `/challenge [easy]` | Get coding challenges |
| `/wisdom` | Programming wisdom |
| `/poem` | Code poetry |
"""

    def cmd_config(self, args):
        table = Table(title="Current Configuration", show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        for key, value in self.config.data.items():
            display = str(value)[:20] + "..." if key == "api_key" and value else str(value)
            table.add_row(key, display)
        table.add_row("---", "---")
        table.add_row("facts_stored", str(len(self.memory.memory.get("facts", []))))
        table.add_row("learnings_stored", str(len(self.memory.learnings)))
        table.add_row("patterns_stored", str(sum(len(v) for v in self.memory.patterns.values())))
        console.print(table)
        return None

    def cmd_provider(self, args):
        valid = ["gemini", "openai", "groq", "nvidia", "together", "openrouter",
                 "deepseek", "mistral", "perplexity", "fireworks", "cohere",
                 "xai", "github", "anthropic", "custom"]
        if args:
            parts = args.split(maxsplit=1)
            provider = parts[0].lower()
            base_url = parts[1] if len(parts) > 1 else ""
            if provider not in valid:
                return f"Invalid provider. Choose from: {', '.join(valid)}"
            if provider == "custom" and not base_url:
                return "Usage: /provider custom <base_url>"
        else:
            console.print("[info]Available providers:[/info]")
            for i, p in enumerate(valid, 1):
                name = PROVIDER_NAMES.get(p, p)
                console.print(f"  [cyan]{i}.[/cyan] {name}")
            choice = Prompt.ask("Select provider", choices=[str(i) for i in range(1, len(valid)+1)] + valid, default="1")
            if choice.isdigit():
                provider = valid[int(choice)-1]
            else:
                provider = choice.lower()
            base_url = ""
            if provider == "custom":
                base_url = Prompt.ask("Enter API base URL (e.g., https://api.together.xyz/v1)").rstrip("/")
                if not base_url:
                    return "Base URL required for custom provider"

        self.config.set("provider", provider)
        if base_url:
            self.config.set("base_url", base_url)
        self.memory.set_preference("provider", provider)

        api_key = self.config.get("api_key") or ""
        if not api_key:
            api_key = Prompt.ask(f"Enter your {provider} API key", password=True)
            self.config.set("api_key", api_key)
        else:
            if not args:
                change = Confirm.ask(f"Keep existing API key?", default=True)
                if not change:
                    api_key = Prompt.ask(f"Enter your {provider} API key", password=True)
                    self.config.set("api_key", api_key)

        models = fetch_available_models(provider, api_key, base_url)
        if models:
            console.print(f"[info]Found {len(models)} available models. Select one:[/info]")
            for i, m in enumerate(models[:30], 1):
                console.print(f"  [cyan]{i}.[/cyan] {m}")
            current_model = self.config.get("model", "")
            default_idx = "1"
            if current_model in models:
                default_idx = str(models.index(current_model) + 1)
            model_choices = [str(i) for i in range(1, min(len(models), 30)+1)] + models[:30]
            model_choice = Prompt.ask("Select model", choices=model_choices, default=default_idx)
            if model_choice.isdigit():
                selected = models[int(model_choice)-1]
            else:
                selected = model_choice
            self.config.set("model", selected)
            return f"Provider set to [bold]{provider}[/bold]. Model: [bold]{selected}[/bold]"
        else:
            model = Prompt.ask("Could not fetch models. Enter model name manually")
            self.config.set("model", model)
            return f"Provider set to [bold]{provider}[/bold]. Model: [bold]{model}[/bold] (manual)"

    def cmd_model(self, args):
        if not args:
            return f"Current model: {self.config.get('model')}"
        self.config.set("model", args)
        return f"Model set to {args}"

    def cmd_key(self, args):
        if not args:
            key = self.config.get("api_key")
            return f"API key: {key[:8]}...{key[-4:]}" if key else "No API key set"
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
        self.compactor.auto_compact(threshold_percent=85)
        try:
            result = subprocess.run(args, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout
            if result.stderr:
                output += f"\n[error]{result.stderr}[/error]"
            if result.returncode == 0:
                self.memory.add_pattern("commands", args, "Successful execution")
            else:
                self.memory.add_learning(f"Command failed: {args}", f"Exit code: {result.returncode}", args, "commands")
            return output or "Command executed (no output)"
        except subprocess.TimeoutExpired:
            return "Command timed out (30s limit)"
        except Exception as e:
            return f"Error: {e}"

    def cmd_ls(self, args):
        path = args if args else "."
        try:
            items = sorted(Path(path).iterdir(), key=lambda x: (not x.is_dir(), x.name))
            table = Table(show_header=False, show_lines=False, show_edge=False)
            table.add_column("Name")
            for item in items[:30]:
                name = item.name
                if item.is_dir():
                    table.add_row(f"[bold blue]{name}/[/bold blue]")
                elif name.endswith((".py", ".js", ".ts", ".sh", ".go", ".rs")):
                    table.add_row(f"[bold green]{name}[/bold green]")
                elif name.endswith((".md", ".txt", ".json", ".yaml")):
                    table.add_row(f"[bold yellow]{name}[/bold yellow]")
                else:
                    table.add_row(name)
            console.print(table)
            return None
        except Exception as e:
            return f"Error: {e}"

    def cmd_pwd(self, args):
        return str(Path.cwd())

    def cmd_cd(self, args):
        if not args:
            return str(Path.cwd())
        try:
            os.chdir(args)
            return f"Now in: {Path.cwd()}"
        except Exception as e:
            return f"Error: {e}"

    def cmd_cat(self, args):
        if not args:
            return "Usage: /cat <file>"
        try:
            with open(args) as f:
                content = f.read()
            ext = Path(args).suffix.lower()
            lang_map = {
                ".py": "python", ".js": "javascript", ".ts": "typescript",
                ".sh": "bash", ".json": "json", ".yaml": "yaml", ".yml": "yaml",
                ".md": "markdown", ".rs": "rust", ".go": "go", ".java": "java",
            }
            lang = lang_map.get(ext, "")
            if lang:
                console.print(Syntax(content, lang, theme="monokai", line_numbers=True))
            else:
                console.print(content)
            return None
        except Exception as e:
            return f"Error: {e}"

    def cmd_git(self, args):
        if not args:
            return "Usage: /git <args> (e.g., /git status)"
        return self.cmd_run(f"git {args}")

    def cmd_skills(self, args):
        table = Table(title="Available Skills", show_header=True, header_style="bold cyan")
        table.add_column("Skill", style="green")
        table.add_column("Description", style="white")
        for key, skill in SKILLS.items():
            table.add_row(key, skill["description"][:40])
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
        console.print(stats)
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
        return results if results else f"No memories found for: {args}"

    def cmd_project(self, args):
        if not args:
            table = Table(title="Projects", show_header=True, header_style="bold cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            for p in self.memory.projects.get("completed", []):
                table.add_row(p["name"], "completed")
            for p in self.memory.projects.get("in_progress", []):
                table.add_row(p["name"], "in progress")
            console.print(table)
            return None
        desc = Prompt.ask("Description")
        tech = Prompt.ask("Tech stack (comma-separated)")
        self.memory.add_project(name=args, description=desc, tech_stack=[t.strip() for t in tech.split(",")], status="completed")
        return f"Project '{args}' recorded!"

    def cmd_learn(self, args):
        if not args or " -> " not in args:
            return "Usage: /learn <what> -> <outcome>"
        parts = args.split(" -> ", 1)
        self.memory.add_learning(parts[0], parts[1], "", "general")
        return f"Learning recorded: {parts[0]} -> {parts[1]}"

    def cmd_suggest(self, args):
        suggestions = []
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
        if (cwd / ".git").exists():
            suggestions.append("Git repo detected. Try: /git status")
        if not suggestions:
            suggestions.append("No specific suggestions. Try: /skills to see what I can do!")
        return "\n".join(f"- {s}" for s in suggestions)

    def cmd_template(self, args):
        templates = {
            "python": '#!/usr/bin/env python3\n"""Project: {name}"""\n\ndef main():\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n',
            "flask": 'from flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef hello():\n    return "Hello from {name}!"\n\nif __name__ == "__main__":\n    app.run(debug=True)\n',
        }
        if not args or args not in templates:
            return f"Available templates: {', '.join(templates.keys())}"
        name = Prompt.ask("Project name")
        return f"```{args}\n{templates[args].format(name=name)}\n```"

    def cmd_compact(self, args):
        with console.status("[muted]Cleaning caches...[/muted]"):
            result = self.compactor.full_compaction()
        console.print(f"[green]Compacted! Freed {result.get('disk_freed_gb', 0)}GB[/green]")
        return None

    def cmd_status(self, args):
        return self.compactor.get_status()

    def cmd_clean(self, args):
        with console.status("[muted]Cleaning...[/muted]"):
            self.compactor.cleanup_pip()
            self.compactor.cleanup_npm()
            self.compactor.cleanup_temp()
            self.compactor.cleanup_pycache()
        disk = self.compactor.get_disk_usage()
        return f"Done! Disk: {disk['free_gb']}GB free ({disk['percent_used']}% used)"

    def cmd_privacy(self, args):
        table = Table(title="Privacy Status", show_header=True, header_style="bold green")
        table.add_column("Feature", style="cyan")
        table.add_column("Status", style="green")
        table.add_row("Privacy Mode", "ON" if self.config.get("privacy_mode", True) else "OFF")
        table.add_row("API Keys", "Encrypted at rest")
        table.add_row("Prompt Sanitization", "Strips emails, phones, keys, passwords")
        console.print(table)
        return None

    def cmd_create(self, args):
        pro = get_pro_tools()
        templates = ["flask-api", "fastapi", "react", "express", "django", "python-cli", "rust-cli", "go-api"]
        if not args:
            return f"Usage: /create <template> <name>\n\nAvailable: {', '.join(templates)}"
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: /create <template> <name>"
        template, name = parts
        if template not in templates:
            return f"Unknown: {template}\nAvailable: {', '.join(templates)}"
        result = pro.create_project(name, template)
        if result.get("success"):
            return f"Project created at: {result['path']}"
        return f"Error: {result.get('error', 'Unknown error')}"

    def cmd_build(self, args):
        if not args:
            return "Usage: /build <description>\n\nExample: /build a Twitter clone with Next.js and PostgreSQL\n\nJust describe what you want to build — I'll scaffold a complete production-grade project."
        with console.status("[info]Analyzing description and scaffolding project...[/info]"):
            pro = get_pro_tools()
            result = pro.build_from_description(args)
        if result.get("success"):
            template = result.get("template_used", "unknown")
            path = result["path"]
            msg = [
                f"[success]Project built successfully![/success]",
                f"[info]Template:[/info] {template}",
                f"[info]Path:[/info] {path}",
                f"",
                f"[bold]What's included:[/bold]",
                f"  - Multi-stage Docker build",
                f"  - Docker Compose (app + PostgreSQL + Redis + Nginx)",
                f"  - CI/CD pipeline (GitHub Actions)",
                f"  - Structured JSON logging",
                f"  - Rate limiting & security middleware",
                f"  - Database with migrations",
                f"  - Test suite with fixtures",
                f"  - Health checks & monitoring",
                f"  - Environment configuration",
                f"",
                f"[muted]Run: cd {path} && docker-compose up -d[/muted]",
            ]
            return "\n".join(msg)
        return f"Error building project: {result.get('error', 'Unknown error')}"

    def cmd_analyze(self, args):
        pro = get_pro_tools()
        analysis = pro.analyze_project(args if args else ".")
        table = Table(title="Project Analysis", show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Files", str(analysis["files"]))
        table.add_row("Languages", ", ".join(analysis["languages"]) or "None detected")
        table.add_row("Has Tests", "Yes" if analysis["has_tests"] else "No")
        table.add_row("Has Docker", "Yes" if analysis["has_docker"] else "No")
        console.print(table)
        return None

    def cmd_generate(self, args):
        pro = get_pro_tools()
        if not args:
            return "Usage: /generate <type> <file>\n\nTypes: tests, deploy"
        parts = args.split(maxsplit=1)
        gen_type, target = parts[0], parts[1] if len(parts) > 1 else "."
        if gen_type == "tests":
            result = pro.generate_tests(target)
            console.print(Syntax(result, "python", theme="monokai"))
        elif gen_type == "deploy":
            result = pro.generate_deploy_config("docker", "app")
            console.print(Syntax(result, "yaml", theme="monokai"))
        else:
            return f"Unknown type: {gen_type}"
        return None

    def cmd_deploy(self, args):
        pro = get_pro_tools()
        platforms = ["docker", "heroku", "railway", "vercel"]
        if not args:
            return f"Usage: /deploy <platform>\n\nPlatforms: {', '.join(platforms)}"
        if args not in platforms:
            return f"Unknown: {args}\nAvailable: {', '.join(platforms)}"
        result = pro.generate_deploy_config(args, "app")
        console.print(Syntax(result, "yaml", theme="monokai"))
        return None

    def cmd_test(self, args):
        if not args:
            return "Usage: /test <file_or_directory>"
        try:
            result = subprocess.run(f"python -m pytest {args} -v", shell=True, capture_output=True, text=True, timeout=60)
            return result.stdout or "Tests completed"
        except subprocess.TimeoutExpired:
            return "Tests timed out (60s limit)"
        except Exception as e:
            return f"Error: {e}"

    def cmd_error(self, args):
        if not args:
            return "Usage: /error <error_message>"
        return get_creative().decode_error(args)

    def cmd_save(self, args):
        if not args:
            return "Usage: /save <name>"
        get_creative().save_snippet(args, "# Your code here", "python", [])
        return f"Snippet '{args}' saved!"

    def cmd_snippets(self, args):
        return get_creative().list_snippets()

    def cmd_commit(self, args):
        message = get_creative().generate_commit_message()
        console.print(f"[bold]Suggested: {message}[/bold]")
        if Confirm.ask("Use this message?"):
            return self.cmd_run(f'git commit -m "{message}"')
        return None

    def cmd_api(self, args):
        if not args:
            return "Usage: /api <method> <url> [data]"
        parts = args.split(maxsplit=2)
        method, url = parts[0].upper(), parts[1] if len(parts) > 1 else ""
        data = parts[2] if len(parts) > 2 else None
        if not url:
            return "Usage: /api <method> <url>"
        return get_creative().test_api(method, url, data)

    def cmd_usage(self, args):
        return get_creative().get_usage_stats()

    def cmd_json(self, args):
        if not args:
            return "Usage: /json <json_string>"
        return get_creative().format_json(args)

    def cmd_regex(self, args):
        if not args:
            return "Usage: /regex <pattern> <text>"
        parts = args.split(maxsplit=1)
        pattern, text = parts[0], parts[1] if len(parts) > 1 else ""
        return get_creative().test_regex(pattern, text)

    def cmd_color(self, args):
        if not args:
            return "Usage: /color <hex_or_rgb>"
        return get_creative().convert_color(args)

    def cmd_sysinfo(self, args):
        return get_creative().get_system_info()

    def cmd_ascii(self, args):
        art = get_creative().get_ascii_art(args or "owura")
        console.print(art, style="cyan")
        return None

    def cmd_search(self, args):
        if not args:
            return "Usage: /search <query>"
        return get_web().search(args)

    def cmd_github(self, args):
        if not args:
            return "Usage: /github <query>"
        return get_web().search_github(args)

    def cmd_pypi(self, args):
        if not args:
            return "Usage: /pypi <package>"
        return get_web().search_pypi(args)

    def cmd_npm_search(self, args):
        if not args:
            return "Usage: /npm <package>"
        return get_web().search_npm(args)

    def cmd_stackoverflow(self, args):
        if not args:
            return "Usage: /so <query>"
        return get_web().search_stackoverflow(args)

    def cmd_wikipedia(self, args):
        if not args:
            return "Usage: /wiki <topic>"
        return get_web().search_wikipedia(args)

    def cmd_news(self, args):
        return get_web().get_news(args if args else "technology")

    def cmd_weather(self, args):
        if not args:
            return "Usage: /weather <city>"
        return get_web().get_weather(args)

    def cmd_ip(self, args):
        return get_web().get_ip_info()

    def cmd_fetch(self, args):
        if not args:
            return "Usage: /fetch <url>"
        return get_web().fetch_url(args)

    def cmd_docs(self, args):
        if not args:
            return "Usage: /docs <query> [python|javascript|node|react|flask]"
        parts = args.split(maxsplit=1)
        query, docs = parts[0], parts[1] if len(parts) > 1 else "python"
        return get_web().search_docs(query, docs)

    def cmd_review(self, args):
        if not args:
            return "Usage: /review <code or file>"
        if os.path.exists(args):
            return get_smart().self_review(file_path=args)
        return get_smart().self_review(code=args)

    def cmd_optimize(self, args):
        if not args:
            return "Usage: /optimize <code or file>"
        if os.path.exists(args):
            return get_smart().self_optimize(file_path=args)
        return get_smart().self_optimize(code=args)

    def cmd_reverse(self, args):
        if not args:
            return "Usage: /reverse <target> [context]"
        parts = args.split(maxsplit=1)
        target, context = parts[0], parts[1] if len(parts) > 1 else "code"
        return get_smart().reverse_engineer(target, context)

    def cmd_loophole(self, args):
        if not args:
            return "Usage: /loophole <problem description>"
        return get_loophole().find_loopholes(args)

    def cmd_fix(self, args):
        if not args:
            return "Usage: /fix <problem>"
        return get_loophole().fix_impossible(args)

    def cmd_free(self, args):
        if not args:
            return "Usage: /free <paid_tool>"
        return get_loophole().find_free_alternative(args)

    def cmd_story(self, args):
        if not args:
            return "Usage: /story <concept>"
        return get_creativity().tell_story(args)

    def cmd_metaphor(self, args):
        if not args:
            return "Usage: /metaphor <concept>"
        return get_creativity().generate_metaphor(args)

    def cmd_name(self, args):
        if not args:
            return "Usage: /name <purpose>"
        return get_creativity().generate_names(args)

    def cmd_poem(self, args):
        lang = args if args in ("python", "javascript") else "python"
        return get_creativity().code_poem(lang)

    def cmd_challenge(self, args):
        difficulty = args if args in ("easy", "medium", "hard") else "easy"
        return get_creativity().get_challenge(difficulty)

    def cmd_wisdom(self, args):
        return get_creativity().get_wisdom()

    def cmd_mood(self, args):
        return "I'll adapt my responses to match your mood. Just talk naturally - I'll detect it automatically."

    def cmd_who(self, args):
        return get_awareness().get_identity()

    def cmd_mission(self, args):
        awareness = get_awareness()
        values = "\n".join(f"- {v}" for v in awareness.values)
        return f"""## Our Mission
**{awareness.mission}**

### Our Vision
{awareness.vision}

### Our Values
{values}

### Why This Matters
Because coding shouldn't be limited to people with expensive laptops.
Because creativity doesn't need a desk.
Because your phone is powerful enough to build the future.

**That's why OWURA exists.**
"""

    def cmd_why(self, args):
        return get_awareness().get_pride_message()

    def cmd_version(self, args):
        from owura import __version__
        return f"OWURA v{__version__} - AI Coding Agent"

    def cmd_quit(self, args):
        self.memory.save_all()
        raise SystemExit


# ============================================================
# MAIN TUI
# ============================================================
def print_banner():
    banner = r"""
[bold cyan]
  _____        ___   _ ____      _    
 / _ \ \      / / | | |  _ \    / \   
| | | \ \ /\ / /| | | | |_) |  / _ \  
| |_| |\ V  V / | |_| |  _ <  / ___ \ 
 \___/  \_/\_/   \___/|_| \_\/_/   \_\
[/bold cyan]
[dim]v1.0 - AI Coding Agent - Code Anywhere. Anytime.[/dim]
[dim]Memory: ON | Learning: ON | Skills: {skills} | MCPs: {mcps} | Web: ON[/dim]

    [italic dim]"I'm not just a tool. I'm a partner in creation."[/italic dim]
""".format(skills=len(SKILLS), mcps=len(MCP_SERVERS))
    console.print(banner)


def main():
    config = Config()
    ai = AIProvider(config)
    processor = CommandProcessor(config, ai)
    memory = get_memory()

    if not config.get("api_key"):
        console.print("[bold]Welcome to OWURA![/bold]")
        console.print("[info]Let's set up your AI provider.[/info]\n")

        valid = ["gemini", "openai", "groq", "nvidia", "together", "openrouter",
                 "deepseek", "mistral", "perplexity", "fireworks", "cohere",
                 "xai", "github", "anthropic", "custom"]
        console.print("[muted]Available providers:[/muted]")
        for i, p in enumerate(valid, 1):
            name = PROVIDER_NAMES.get(p, p)
            console.print(f"  [cyan]{i}.[/cyan] {name}")
        choice = Prompt.ask("Choose provider", choices=[str(i) for i in range(1, len(valid)+1)] + valid, default="1")
        if choice.isdigit():
            provider = valid[int(choice)-1]
        else:
            provider = choice.lower()
        config.set("provider", provider)

        base_url = ""
        if provider == "custom":
            base_url = Prompt.ask("Enter API base URL (e.g., https://api.together.xyz/v1)").rstrip("/")
            if base_url:
                config.set("base_url", base_url)

        api_key = Prompt.ask(f"Enter your {provider} API key", password=True)
        config.set("api_key", api_key)

        models = fetch_available_models(provider, api_key, base_url)
        if models:
            console.print(f"[info]Found {len(models)} available models. Select one:[/info]")
            for i, m in enumerate(models[:30], 1):
                console.print(f"  [cyan]{i}.[/cyan] {m}")
            model_choices = [str(i) for i in range(1, min(len(models), 30)+1)] + models[:30]
            model_choice = Prompt.ask("Select model", choices=model_choices, default="1")
            if model_choice.isdigit():
                config.set("model", models[int(model_choice)-1])
            else:
                config.set("model", model_choice)
        else:
            model = Prompt.ask("Could not fetch models. Enter model name manually")
            config.set("model", model)

        memory.set_preference("provider", provider)
        console.print("[success]Configuration saved![/success]\n")

    print_banner()

    if config.get("memory_enabled") and memory.memory.get("facts"):
        console.print(f"[muted]Memory: {len(memory.memory['facts'])} facts, {len(memory.learnings)} learnings loaded[/muted]")

    console.print("[muted]Type /help for commands, /quit to exit[/muted]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]owura[/bold cyan]")
            if not user_input.strip():
                continue

            processor.history.append({"input": user_input, "time": datetime.now().strftime("%H:%M:%S")})

            with console.status("[muted]Thinking...[/muted]"):
                response = processor.process(user_input)

            if response:
                console.print()
                try:
                    console.print(Markdown(response))
                except Exception:
                    console.print(response)
                console.print()

            try:
                HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(HISTORY_FILE, "w") as f:
                    json.dump(processor.history[-config.get("max_history", 100):], f)
            except Exception:
                pass

        except SystemExit:
            console.print("[info]Memory saved. Goodbye![/info]")
            break
        except KeyboardInterrupt:
            console.print("\n[muted]Use /quit to exit[/muted]")
        except Exception as e:
            console.print(f"[error]Error: {e}[/error]")


if __name__ == "__main__":
    main()
