"""
OWURA Smart Skills - Self-review, self-optimize, reverse engineering
These skills activate automatically when the task demands them.
"""

import os
import re
import ast
import json
import subprocess
from pathlib import Path
from datetime import datetime

class SmartSkills:
    def __init__(self):
        self.skills_dir = Path.home() / ".owura" / "skills"
        self.skills_dir.mkdir(parents=True, exist_ok=True)
    
    # ============================================================
    # SELF-REVIEW - Analyze code quality
    # ============================================================
    def self_review(self, code: str = None, file_path: str = None) -> str:
        """Review code for issues, improvements, and best practices."""
        
        if file_path and not code:
            try:
                with open(file_path) as f:
                    code = f.read()
            except:
                return f"Cannot read file: {file_path}"
        
        if not code:
            return "No code to review. Provide code or file path."
        
        issues = []
        suggestions = []
        score = 100
        
        # Check for common issues
        lines = code.split("\n")
        
        # 1. Security issues
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password", -15),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key", -20),
            (r'eval\(', "Use of eval() (security risk)", -25),
            (r'exec\(', "Use of exec() (security risk)", -25),
            (r'subprocess\.call.*shell=True', "Shell injection risk", -10),
        ]
        
        for pattern, msg, penalty in security_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(f" Security: {msg}")
                score += penalty
        
        # 2. Code quality
        if len(lines) > 500:
            suggestions.append("Consider splitting into smaller functions/modules")
        
        long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 120]
        if long_lines:
            suggestions.append(f"Long lines (>120 chars) at: {long_lines[:5]}")
        
        # 3. Documentation
        if 'def ' in code and '"""' not in code and "'''" not in code:
            suggestions.append("Add docstrings to functions")
        
        # 4. Error handling
        if 'try:' in code and 'except:' in code:
            issues.append(" Bare except clause - catch specific exceptions")
            score -= 5
        
        # 5. Python specific
        if code.strip().startswith("import") or "from " in code:
            # Check for unused imports (basic check)
            imports = re.findall(r'import (\w+)', code)
            for imp in imports:
                if imp not in code.replace(f'import {imp}', '').replace(f'from {imp}', ''):
                    suggestions.append(f"Potentially unused import: {imp}")
        
        # 6. Type hints
        if 'def ' in code and '->' not in code and ':' not in code.split('def')[1].split(')')[0]:
            suggestions.append("Consider adding type hints")
        
        # Build report
        lines_out = ["## Code Review Report\n"]
        
        # Score
        score = max(0, min(100, score))
        if score >= 80:
            lines_out.append(f"**Score: {score}/100** Good code quality!")
        elif score >= 60:
            lines_out.append(f"**Score: {score}/100** Needs improvement")
        else:
            lines_out.append(f"**Score: {score}/100** Critical issues found")
        
        lines_out.append("")
        
        if issues:
            lines_out.append("### Issues Found")
            for issue in issues:
                lines_out.append(f"- {issue}")
            lines_out.append("")
        
        if suggestions:
            lines_out.append("### Suggestions")
            for sug in suggestions:
                lines_out.append(f"- {sug}")
            lines_out.append("")
        
        # Positive observations
        positives = []
        if '"""' in code or "'''" in code:
            positives.append("Has docstrings")
        if 'try:' in code:
            positives.append("Uses error handling")
        if 'class ' in code:
            positives.append("Uses OOP")
        if any(f'def test_' in code for _ in [1]):
            positives.append("Has tests")
        
        if positives:
            lines_out.append("### Good Practices")
            for pos in positives:
                lines_out.append(f"- {pos}")
        
        return "\n".join(lines_out)
    
    # ============================================================
    # SELF-OPTIMIZE - Improve performance
    # ============================================================
    def self_optimize(self, code: str = None, file_path: str = None) -> str:
        """Analyze and suggest optimizations."""
        
        if file_path and not code:
            try:
                with open(file_path) as f:
                    code = f.read()
            except:
                return f"Cannot read file: {file_path}"
        
        if not code:
            return "No code to optimize."
        
        optimizations = []
        
        # 1. Loop optimizations
        if 'for ' in code and 'range(len(' in code:
            optimizations.append({
                "issue": "Using range(len()) instead of enumerate()",
                "fix": "Use enumerate() for cleaner iteration",
                "example": "for i, item in enumerate(items):"
            })
        
        # 2. List comprehension vs loop
        loop_pattern = r'for .+ in .+:\s*\n\s+.+\.append\('
        if re.search(loop_pattern, code):
            optimizations.append({
                "issue": "Loop with append could be list comprehension",
                "fix": "Use list comprehension for better performance",
                "example": "[expr for item in iterable]"
            })
        
        # 3. String concatenation
        if '+=' in code and ('"' in code or "'" in code):
            optimizations.append({
                "issue": "String concatenation in loop",
                "fix": "Use join() or f-strings",
                'example': '" ".join(parts)'
            })
        
        # 4. Global variable access
        if 'global ' in code:
            optimizations.append({
                "issue": "Global variables used",
                "fix": "Pass as parameters or use class attributes",
                "example": "def func(data): process(data)"
            })
        
        # 5. Repeated computations
        # Simple heuristic: look for repeated function calls
        func_calls = re.findall(r'(\w+\([^)]*\))', code)
        if len(func_calls) > 2:
            from collections import Counter
            repeated = [item for item, count in Counter(func_calls).items() if count > 2]
            if repeated:
                optimizations.append({
                    "issue": f"Repeated calls to: {repeated[0]}",
                    "fix": "Cache the result in a variable",
                    "example": f"result = {repeated[0]}"
                })
        
        # 6. File handling
        if 'open(' in code and 'with' not in code:
            optimizations.append({
                "issue": "File opened without context manager",
                "fix": "Use 'with' statement for safe file handling",
                "example": "with open('file') as f: ..."
            })
        
        # 7. Import optimization
        imports = re.findall(r'^(?:from|import) (\w+)', code, re.MULTILINE)
        if len(imports) > 10:
            optimizations.append({
                "issue": f"Many imports ({len(imports)})",
                "fix": "Consider lazy imports or organize by category",
                "example": "import module only when needed"
            })
        
        # Build report
        lines = ["## Optimization Report\n"]
        
        if not optimizations:
            lines.append("No significant optimizations needed. Code looks good!")
        else:
            lines.append(f"Found {len(optimizations)} potential optimizations:\n")
            
            for i, opt in enumerate(optimizations, 1):
                lines.append(f"### {i}. {opt['issue']}")
                lines.append(f"**Fix:** {opt['fix']}")
                lines.append(f"**Example:** `{opt['example']}`")
                lines.append("")
        
        # Performance tips
        lines.append("### General Tips")
        lines.append("- Use built-in functions (map, filter, zip)")
        lines.append("- Avoid global variables")
        lines.append("- Use generators for large datasets")
        lines.append("- Cache expensive computations")
        lines.append("- Use set() for membership testing")
        
        return "\n".join(lines)
    
    # ============================================================
    # REVERSE ENGINEERING - Analyze and understand code
    # ============================================================
    def reverse_engineer(self, target: str, context: str = "code") -> str:
        """Analyze and explain code, APIs, or systems."""
        
        if context == "code":
            return self._analyze_code(target)
        elif context == "api":
            return self._analyze_api(target)
        elif context == "binary":
            return self._analyze_binary(target)
        elif context == "network":
            return self._analyze_network(target)
        else:
            return self._analyze_code(target)
    
    def _analyze_code(self, code: str) -> str:
        """Analyze code structure and explain it."""
        
        analysis = []
        
        # Detect language
        if 'def ' in code and ':' in code:
            lang = "Python"
        elif 'function ' in code or '=>' in code:
            lang = "JavaScript"
        elif 'func ' in code:
            lang = "Go"
        elif 'fn ' in code:
            lang = "Rust"
        elif 'public class' in code:
            lang = "Java"
        else:
            lang = "Unknown"
        
        analysis.append(f"## Code Analysis\n")
        analysis.append(f"**Language:** {lang}\n")
        
        # Extract components
        if lang == "Python":
            # Functions
            funcs = re.findall(r'def (\w+)\(', code)
            if funcs:
                analysis.append(f"**Functions:** {', '.join(funcs)}")
            
            # Classes
            classes = re.findall(r'class (\w+)', code)
            if classes:
                analysis.append(f"**Classes:** {', '.join(classes)}")
            
            # Imports
            imports = re.findall(r'^(?:from|import) (\w+)', code, re.MULTILINE)
            if imports:
                analysis.append(f"**Dependencies:** {', '.join(set(imports))}")
            
            # Decorators
            decorators = re.findall(r'@(\w+)', code)
            if decorators:
                analysis.append(f"**Decorators:** {', '.join(set(decorators))}")
        
        # Complexity estimate
        lines = code.split("\n")
        analysis.append(f"\n**Lines of code:** {len(lines)}")
        
        if len(lines) < 50:
            analysis.append("**Complexity:** Low")
        elif len(lines) < 200:
            analysis.append("**Complexity:** Medium")
        else:
            analysis.append("**Complexity:** High")
        
        # Dependencies
        if 'requests' in code or 'urllib' in code:
            analysis.append("**Network calls:** Yes")
        if 'sqlite' in code or 'mysql' in code or 'psycopg' in code:
            analysis.append("**Database:** Yes")
        if 'thread' in code or 'async' in code:
            analysis.append("**Concurrency:** Yes")
        
        # Purpose guess
        purposes = []
        if 'api' in code.lower() or 'route' in code.lower():
            purposes.append("API/Server")
        if 'test' in code.lower():
            purposes.append("Testing")
        if 'scrape' in code.lower() or 'beautifulsoup' in code.lower():
            purposes.append("Web scraping")
        if 'train' in code.lower() or 'model' in code.lower():
            purposes.append("Machine Learning")
        if 'cli' in code.lower() or 'argparse' in code.lower():
            purposes.append("CLI tool")
        
        if purposes:
            analysis.append(f"**Likely purpose:** {', '.join(purposes)}")
        
        return "\n".join(analysis)
    
    def _analyze_api(self, endpoint: str) -> str:
        """Analyze an API endpoint."""
        
        analysis = [
            "## API Analysis\n",
            f"**Endpoint:** {endpoint}\n",
        ]
        
        # Try to fetch API info
        try:
            import urllib.request
            req = urllib.request.Request(endpoint, headers={"User-Agent": "OWURA"})
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.status
                headers = dict(response.headers)
                body = response.read().decode()[:500]
                
                analysis.append(f"**Status:** {status}")
                analysis.append(f"**Content-Type:** {headers.get('Content-Type', 'N/A')}")
                analysis.append(f"**Server:** {headers.get('Server', 'N/A')}")
                analysis.append(f"\n**Response preview:**\n```\n{body}\n```")
        
        except Exception as e:
            analysis.append(f"**Connection:** Failed ({str(e)[:50]})")
        
        return "\n".join(analysis)
    
    def _analyze_binary(self, file_path: str) -> str:
        """Analyze a binary file."""
        
        try:
            with open(file_path, "rb") as f:
                header = f.read(1024)
            
            analysis = [
                "## Binary Analysis\n",
                f"**File:** {file_path}",
                f"**Size:** {os.path.getsize(file_path)} bytes",
                f"**Magic bytes:** {header[:4].hex()}",
            ]
            
            # Detect type
            if header[:4] == b'\x7fELF':
                analysis.append("**Type:** ELF executable (Linux)")
            elif header[:2] == b'MZ':
                analysis.append("**Type:** PE executable (Windows)")
            elif header[:4] == b'\xcf\xfa\xed\xfe':
                analysis.append("**Type:** Mach-O executable (macOS)")
            elif header[:4] == b'PK\x03\x04':
                analysis.append("**Type:** ZIP archive (or APK/JAR)")
            elif header[:4] == b'%PDF':
                analysis.append("**Type:** PDF document")
            elif header[:3] == b'\xff\xd8\xff':
                analysis.append("**Type:** JPEG image")
            elif header[:8] == b'\x89PNG\r\n\x1a\n':
                analysis.append("**Type:** PNG image")
            
            # Strings
            strings = re.findall(b'[\x20-\x7e]{4,}', header)
            if strings:
                analysis.append(f"\n**Found strings:** {len(strings)}")
                for s in strings[:5]:
                    analysis.append(f"  - {s.decode()}")
            
            return "\n".join(analysis)
        
        except Exception as e:
            return f"Error analyzing binary: {str(e)}"
    
    def _analyze_network(self, target: str) -> str:
        """Analyze network target."""
        
        analysis = [
            "## Network Analysis\n",
            f"**Target:** {target}\n",
        ]
        
        # Ping
        try:
            result = subprocess.run(
                f"ping -c 1 {target}",
                shell=True, capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                analysis.append("**Ping:** Reachable")
                # Extract time
                time_match = re.search(r'time=(\d+\.?\d*)', result.stdout)
                if time_match:
                    analysis.append(f"**Latency:** {time_match.group(1)}ms")
            else:
                analysis.append("**Ping:** Unreachable")
        except:
            analysis.append("**Ping:** Timeout")
        
        # DNS
        try:
            import socket
            ip = socket.gethostbyname(target)
            analysis.append(f"**IP:** {ip}")
        except:
            analysis.append("**DNS:** Failed")
        
        # Port scan (common ports)
        analysis.append("\n**Common ports:**")
        common_ports = [80, 443, 22, 21, 25, 53, 8080, 3000, 5000]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    analysis.append(f"  - {port}: OPEN")
                sock.close()
            except:
                pass
        
        return "\n".join(analysis)
    
    # ============================================================
    # AUTO-DETECT - Choose skill based on context
    # ============================================================
    def auto_detect_skill(self, user_input: str) -> str:
        """Automatically detect which skill to use."""
        
        input_lower = user_input.lower()
        
        # Review keywords
        review_keywords = ["review", "check", "analyze", "quality", "lint", "improve"]
        if any(kw in input_lower for kw in review_keywords):
            return "review"
        
        # Optimize keywords
        optimize_keywords = ["optimize", "performance", "speed", "faster", "efficient"]
        if any(kw in input_lower for kw in optimize_keywords):
            return "optimize"
        
        # Reverse engineer keywords
        reverse_keywords = ["reverse", "explain", "decompile", "analyze", "understand"]
        if any(kw in input_lower for kw in reverse_keywords):
            return "reverse"
        
        return None
    
    def handle_auto_skill(self, user_input: str, code: str = None) -> str:
        """Handle automatic skill detection and execution."""
        
        skill = self.auto_detect_skill(user_input)
        
        if skill == "review":
            if code:
                return self.self_review(code=code)
            return "Provide code to review. Use: review this code: ```...```"
        
        elif skill == "optimize":
            if code:
                return self.self_optimize(code=code)
            return "Provide code to optimize. Use: optimize this code: ```...```"
        
        elif skill == "reverse":
            return self.reverse_engineer(user_input, "code")
        
        return None

# Global instance
_smart = None

def get_smart() -> SmartSkills:
    global _smart
    if _smart is None:
        _smart = SmartSkills()
    return _smart
