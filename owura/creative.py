"""
OWURA Creative Tools - Unique features that make it special
"""

import os
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess

CREATIVE_DIR = Path.home() / ".owura" / "creative"
SNIPPETS_FILE = CREATIVE_DIR / "snippets.json"
ERROR_LOG = CREATIVE_DIR / "error_log.json"

class CreativeTools:
    def __init__(self):
        self.creative_dir = CREATIVE_DIR
        self.creative_dir.mkdir(parents=True, exist_ok=True)
    
    # ============================================================
    # 1. ERROR DECODER - Paste error, get solution
    # ============================================================
    def decode_error(self, error_message: str) -> str:
        """Analyze error and provide solution."""
        error_patterns = {
            "ModuleNotFoundError": {
                "cause": "Missing Python package",
                "fix": "pip install {module}",
                "prevention": "Always use requirements.txt"
            },
            "SyntaxError": {
                "cause": "Code syntax is invalid",
                "fix": "Check for missing colons, brackets, or quotes",
                "prevention": "Use an IDE with syntax highlighting"
            },
            "IndentationError": {
                "cause": "Inconsistent indentation",
                "fix": "Use 4 spaces or tabs consistently",
                "prevention": "Configure editor to use spaces"
            },
            "NameError": {
                "cause": "Variable not defined",
                "fix": "Define the variable before using it",
                "prevention": "Check variable names for typos"
            },
            "TypeError": {
                "cause": "Wrong data type operation",
                "fix": "Convert types: int(), str(), float()",
                "prevention": "Use type hints"
            },
            "ValueError": {
                "cause": "Invalid value",
                "fix": "Validate input before processing",
                "prevention": "Add input validation"
            },
            "FileNotFoundError": {
                "cause": "File doesn't exist",
                "fix": "Check file path and name",
                "prevention": "Use os.path.exists() check"
            },
            "ImportError": {
                "cause": "Cannot import module",
                "fix": "Install: pip install {module}",
                "prevention": "Check package name"
            },
            "ECONNREFUSED": {
                "cause": "Server not running",
                "fix": "Start the server first",
                "prevention": "Check server status"
            },
            "PermissionError": {
                "cause": "Insufficient permissions",
                "fix": "Run with sudo or check file permissions",
                "prevention": "Use appropriate user"
            },
            "npm ERR!": {
                "cause": "npm package issue",
                "fix": "Delete node_modules, run npm install",
                "prevention": "Use package-lock.json"
            },
            "EACCES": {
                "cause": "Permission denied",
                "fix": "chmod +x or use sudo",
                "prevention": "Don't run as root"
            },
        }
        
        for error_type, info in error_patterns.items():
            if error_type.lower() in error_message.lower():
                # Extract module name if present
                module = ""
                if "{module}" in info["fix"]:
                    match = re.search(r"No module named '(\w+)'", error_message)
                    if match:
                        module = match.group(1)
                    else:
                        match = re.search(r"Cannot find module '(\w+)'", error_message)
                        if match:
                            module = match.group(1)
                
                fix = info["fix"].replace("{module}", module)
                
                return f"""## Error: {error_type}

**Cause:** {info['cause']}

**Fix:**
```bash
{fix}
```

**Prevention:** {info['prevention']}

**Similar errors in your history:** Check `/recall {error_type}`"""
        
        # Generic error handling
        return f"""## Error Analysis

**Error:** {error_message[:200]}...

**Common causes:**
1. Check if all dependencies are installed
2. Verify file paths and permissions
3. Check for typos in variable/function names
4. Ensure proper indentation

**Next steps:**
- Run: `/run python -m py_compile <file>` to check syntax
- Search: `/web-search {error_message[:50]}`
- Ask: `How to fix: {error_message[:100]}`
"""
    
    # ============================================================
    # 2. CODE SNIPPETS LIBRARY
    # ============================================================
    def save_snippet(self, name: str, code: str, language: str, tags: list = None):
        """Save a code snippet."""
        snippets = self._load_snippets()
        
        snippet = {
            "name": name,
            "code": code,
            "language": language,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "uses": 0
        }
        
        snippets[name] = snippet
        self._save_snippets(snippets)
        return f"Snippet '{name}' saved!"
    
    def get_snippet(self, name: str) -> str:
        """Get a code snippet."""
        snippets = self._load_snippets()
        snippet = snippets.get(name)
        
        if snippet:
            snippet["uses"] = snippet.get("uses", 0) + 1
            self._save_snippets(snippets)
            return f"```{snippet['language']}\n{snippet['code']}\n```\n\nTags: {', '.join(snippet.get('tags', []))}"
        
        return f"Snippet '{name}' not found. Use /snippets to list all."
    
    def list_snippets(self, filter_tag: str = None) -> str:
        """List all snippets."""
        snippets = self._load_snippets()
        
        if not snippets:
            return "No snippets saved yet. Use /save <name> to save one."
        
        lines = ["## Saved Snippets\n"]
        
        for name, snippet in snippets.items():
            tags = ", ".join(snippet.get("tags", []))
            lines.append(f"- **{name}** ({snippet['language']}) - Used {snippet.get('uses', 0)} times")
            if tags:
                lines.append(f"  Tags: {tags}")
        
        return "\n".join(lines)
    
    def _load_snippets(self) -> dict:
        if SNIPPETS_FILE.exists():
            try:
                return json.loads(SNIPPETS_FILE.read_text())
            except:
                return {}
        return {}
    
    def _save_snippets(self, snippets: dict):
        SNIPPETS_FILE.write_text(json.dumps(snippets, indent=2))
    
    # ============================================================
    # 3. SMART GIT COMMIT
    # ============================================================
    def generate_commit_message(self, changes: str = None) -> str:
        """Generate meaningful commit message."""
        try:
            # Get git status
            result = subprocess.run(
                "git status --short",
                shell=True, capture_output=True, text=True
            )
            files = result.stdout.strip().split("\n")
            
            # Analyze changes
            added = []
            modified = []
            deleted = []
            
            for f in files:
                if not f.strip():
                    continue
                status = f[:2].strip()
                name = f[2:].strip()
                
                if status == "A":
                    added.append(name)
                elif status == "M":
                    modified.append(name)
                elif status == "D":
                    deleted.append(name)
            
            # Generate message
            parts = []
            
            if added:
                if len(added) == 1:
                    parts.append(f"Add {added[0]}")
                else:
                    parts.append(f"Add {len(added)} files")
            
            if modified:
                if len(modified) == 1:
                    parts.append(f"Update {modified[0]}")
                else:
                    parts.append(f"Update {len(modified)} files")
            
            if deleted:
                if len(deleted) == 1:
                    parts.append(f"Remove {deleted[0]}")
                else:
                    parts.append(f"Remove {len(deleted)} files")
            
            if parts:
                return " | ".join(parts)
            
            return "Update project files"
            
        except:
            return "Update project"
    
    # ============================================================
    # 4. API TESTER - Test endpoints
    # ============================================================
    def test_api(self, method: str, url: str, data: str = None, headers: dict = None) -> str:
        """Test an API endpoint."""
        import urllib.request
        
        try:
            req_data = None
            if data:
                req_data = data.encode("utf-8")
            
            req_headers = {"Content-Type": "application/json"}
            if headers:
                req_headers.update(headers)
            
            req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                body = response.read().decode()
                
                try:
                    json_body = json.loads(body)
                    formatted = json.dumps(json_body, indent=2)
                except:
                    formatted = body
                
                return f"""## API Response

**Status:** {status}
**URL:** {url}

```json
{formatted}
```"""
        
        except Exception as e:
            return f"## API Error\n\n**Error:** {str(e)}\n\n**URL:** {url}"
    
    # ============================================================
    # 5. TOKEN TRACKER - Track API usage
    # ============================================================
    def log_usage(self, provider: str, tokens: int, cost: float = 0):
        """Log API usage."""
        usage_file = self.creative_dir / "usage.json"
        
        if usage_file.exists():
            usage = json.loads(usage_file.read_text())
        else:
            usage = {"total_tokens": 0, "total_cost": 0, "sessions": []}
        
        usage["total_tokens"] += tokens
        usage["total_cost"] += cost
        usage["sessions"].append({
            "provider": provider,
            "tokens": tokens,
            "cost": cost,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 100 sessions
        if len(usage["sessions"]) > 100:
            usage["sessions"] = usage["sessions"][-100:]
        
        usage_file.write_text(json.dumps(usage, indent=2))
    
    def get_usage_stats(self) -> str:
        """Get usage statistics."""
        usage_file = self.creative_dir / "usage.json"
        
        if not usage_file.exists():
            return "No usage data yet."
        
        usage = json.loads(usage_file.read_text())
        
        lines = [
            "## API Usage Statistics",
            "",
            f"**Total Tokens:** {usage['total_tokens']:,}",
            f"**Total Cost:** ${usage['total_cost']:.4f}",
            "",
            "**Recent Sessions:**",
        ]
        
        for session in usage["sessions"][-5:]:
            lines.append(f"- {session['provider']}: {session['tokens']} tokens (${session['cost']:.4f})")
        
        return "\n".join(lines)
    
    # ============================================================
    # 6. JSON FORMATTER
    # ============================================================
    def format_json(self, data: str) -> str:
        """Format and validate JSON."""
        try:
            parsed = json.loads(data)
            formatted = json.dumps(parsed, indent=2)
            return f"```json\n{formatted}\n```\n\n**Valid JSON** ({len(formatted)} chars)"
        except json.JSONDecodeError as e:
            return f"**Invalid JSON**\n\nError: {str(e)}\n\nCheck line {e.lineno}, column {e.colno}"
    
    # ============================================================
    # 7. REGEX TESTER
    # ============================================================
    def test_regex(self, pattern: str, text: str) -> str:
        """Test a regex pattern."""
        try:
            matches = re.findall(pattern, text)
            
            lines = [
                f"**Pattern:** `{pattern}`",
                "",
                f"**Matches found:** {len(matches)}",
            ]
            
            if matches:
                lines.append("")
                lines.append("**Matches:**")
                for i, match in enumerate(matches[:10], 1):
                    lines.append(f"{i}. `{match}`")
            
            # Highlight matches in text
            highlighted = re.sub(pattern, lambda m: f"**[{m.group()}]**", text)
            lines.append("")
            lines.append("**Text with highlights:**")
            lines.append(highlighted[:500])
            
            return "\n".join(lines)
        
        except re.error as e:
            return f"**Invalid regex:** {str(e)}"
    
    # ============================================================
    # 8. COLOR CODE CONVERTER
    # ============================================================
    def convert_color(self, color: str) -> str:
        """Convert color between formats."""
        import re
        
        # Hex to RGB
        hex_match = re.match(r'^#?([0-9a-fA-F]{6})$', color)
        if hex_match:
            hex_val = hex_match.group(1)
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            return f"""## Color Conversion

**HEX:** #{hex_val}
**RGB:** rgb({r}, {g}, {b})
**HSL:** hsl({self._rgb_to_hsl(r, g, b)})
**RGBA:** rgba({r}, {g}, {b}, 1)
"""
        
        # RGB to Hex
        rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
        if rgb_match:
            r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
            hex_val = f"#{r:02x}{g:02x}{b:02x}"
            return f"""## Color Conversion

**RGB:** rgb({r}, {g}, {b})
**HEX:** {hex_val}
**HSL:** hsl({self._rgb_to_hsl(r, g, b)})
"""
        
        return "Format not recognized. Use #RRGGBB or rgb(r, g, b)"
    
    def _rgb_to_hsl(self, r, g, b):
        r, g, b = r/255, g/255, b/255
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        l = (max_val + min_val) / 2
        
        if max_val == min_val:
            h = s = 0
        else:
            d = max_val - min_val
            s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
            if max_val == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return f"{int(h*360)}, {int(s*100)}%, {int(l*100)}%"
    
    # ============================================================
    # 9. SYSTEM INFO
    # ============================================================
    def get_system_info(self) -> str:
        """Get system information."""
        import platform
        
        lines = [
            "## System Information",
            "",
            f"**OS:** {platform.system()} {platform.release()}",
            f"**Python:** {platform.python_version()}",
            f"**Machine:** {platform.machine()}",
            f"**Processor:** {platform.processor() or 'N/A'}",
        ]
        
        # Get disk usage
        try:
            import shutil
            usage = shutil.disk_usage("/")
            lines.append(f"**Disk:** {usage.free // (1024**3)}GB free of {usage.total // (1024**3)}GB")
        except:
            pass
        
        # Get memory
        try:
            with open("/proc/meminfo") as f:
                mem = f.readline()
                total = int(mem.split()[1]) // 1024
                lines.append(f"**Memory:** {total}MB total")
        except:
            pass
        
        return "\n".join(lines)
    
    # ============================================================
    # 10. ASCII ART
    # ============================================================
    def get_ascii_art(self, text: str = "OWURA") -> str:
        """Generate ASCII art."""
        arts = {
            "owura": """
  ___   _   _  _   _  ___   ___ 
 / _ \\ | | | || | | | / _ \\ / _ \\
| | | || | | || | | || | | | (_) |
| |_| || |_| || |_| || |_| | \\__, |
 \\___/  \\__, | \\___/  \\___/    /_/
         __/ |                    
        |___/                     
""",
            "code": """
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘   CODE > COMPILE > RUN  â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
""",
            "hack": """
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ > ACCESS GRANTED_        â”‚
â”‚ > LOADING SYSTEM...      â”‚
â”‚ > READY FOR INPUT        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
""",
        }
        
        return arts.get(text.lower(), arts["owura"])

# Global instance
_creative = None

def get_creative() -> CreativeTools:
    global _creative
    if _creative is None:
        _creative = CreativeTools()
    return _creative
