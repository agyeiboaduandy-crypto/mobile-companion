"""
OWURA Loophole Finder - Creative problem solving
Finds workarounds and alternative solutions when standard methods fail.
"""

import json
import re
from pathlib import Path
from datetime import datetime

class LoopholeFinder:
    def __init__(self):
        self.history_dir = Path.home() / ".owura" / "loopholes"
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    # ============================================================
    # MAIN ANALYSIS - Find loopholes in any problem
    # ============================================================
    def find_loopholes(self, problem: str, context: str = None) -> str:
        """Analyze a problem and find creative solutions."""
        
        analysis = [
            "## Loophole Analysis\n",
            f"**Problem:** {problem}\n",
        ]
        
        # 1. Break down the problem
        analysis.append("### Breaking Down the Problem")
        barriers = self._identify_barriers(problem)
        for barrier in barriers:
            analysis.append(f"- **Barrier:** {barrier}")
        analysis.append("")
        
        # 2. Find workarounds for each barrier
        analysis.append("### Potential Workarounds")
        
        solutions = []
        for barrier in barriers:
            workarounds = self._find_workarounds(barrier)
            solutions.extend(workarounds)
            for w in workarounds:
                analysis.append(f"- {w}")
        analysis.append("")
        
        # 3. Alternative approaches
        analysis.append("### Alternative Approaches")
        alternatives = self._find_alternatives(problem)
        for alt in alternatives:
            analysis.append(f"- {alt}")
        analysis.append("")
        
        # 4. Hidden options
        analysis.append("### Hidden/Undocumented Options")
        hidden = self._find_hidden_options(problem)
        for h in hidden:
            analysis.append(f"- {h}")
        analysis.append("")
        
        # 5. Creative hacks
        analysis.append("### Creative Hacks")
        hacks = self._creative_hacks(problem)
        for hack in hacks:
            analysis.append(f"- {hack}")
        
        # Save to history
        self._save_loophole(problem, solutions)
        
        return "\n".join(analysis)
    
    # ============================================================
    # BARRIER IDENTIFICATION
    # ============================================================
    def _identify_barriers(self, problem: str) -> list:
        """Identify what's blocking the solution."""
        barriers = []
        problem_lower = problem.lower()
        
        # Common barriers
        if any(w in problem_lower for w in ["permission", "access", "denied", "forbidden"]):
            barriers.append("Permission/Access restriction")
        
        if any(w in problem_lower for w in ["not supported", "doesn't work", "unsupported"]):
            barriers.append("Platform/feature limitation")
        
        if any(w in problem_lower for w in ["rate limit", "throttl", "too many"]):
            barriers.append("Rate limiting")
        
        if any(w in problem_lower for w in ["cost", "expensive", "paywall", "premium"]):
            barriers.append("Cost barrier")
        
        if any(w in problem_lower for w in ["not available", "unavailable", "deprecated"]):
            barriers.append("Service unavailability")
        
        if any(w in problem_lower for w in ["slow", "timeout", "performance"]):
            barriers.append("Performance limitation")
        
        if any(w in problem_lower for w in ["compatibility", "incompatible", "version"]):
            barriers.append("Compatibility issue")
        
        if any(w in problem_lower for w in ["legal", "terms", "policy", "restriction"]):
            barriers.append("Legal/policy restriction")
        
        if any(w in problem_lower for w in ["api", "endpoint", "request"]):
            barriers.append("API limitation")
        
        if any(w in problem_lower for w in ["storage", "space", "memory", "disk"]):
            barriers.append("Resource limitation")
        
        # If no specific barrier identified, add generic
        if not barriers:
            barriers.append("Standard approach blocked")
        
        return barriers
    
    # ============================================================
    # WORKAROUND FINDER
    # ============================================================
    def _find_workarounds(self, barrier: str) -> list:
        """Find workarounds for specific barriers."""
        
        workarounds = {
            "Permission/Access restriction": [
                "Try alternative authentication method",
                "Use different API key or account",
                "Check for public/anonymous access options",
                "Look for alternative endpoints with fewer restrictions",
                "Use proxy or different IP if IP-based restriction",
            ],
            "Platform/feature limitation": [
                "Use alternative library that supports your need",
                "Check for experimental/unstable features",
                "Look for third-party wrappers or extensions",
                "Use browser automation instead of API",
                "Combine multiple simpler features to achieve goal",
            ],
            "Rate limiting": [
                "Implement request batching",
                "Add delays between requests",
                "Use multiple API keys/accounts",
                "Cache responses to reduce calls",
                "Look for higher tier or alternative endpoints",
            ],
            "Cost barrier": [
                "Look for free tier or trial",
                "Use open-source alternatives",
                "Check for student/developer discounts",
                "Use self-hosted solutions",
                "Find community or shared resources",
            ],
            "Service unavailability": [
                "Check alternative regions or endpoints",
                "Use cached/archived versions",
                "Look for mirror services",
                "Try different time (off-peak)",
                "Use backup or fallback service",
            ],
            "Performance limitation": [
                "Optimize code for speed",
                "Use async/concurrent processing",
                "Implement caching",
                "Use lighter alternatives",
                "Batch operations",
            ],
            "Compatibility issue": [
                "Use compatibility layers",
                "Install missing dependencies",
                "Use older/newer version",
                "Wrap in adapter pattern",
                "Use abstraction layer",
            ],
            "Legal/policy restriction": [
                "Check terms of service carefully",
                "Look for exceptions or fair use",
                "Use official alternatives",
                "Contact support for permission",
                "Find open-source equivalents",
            ],
            "API limitation": [
                "Look for alternative endpoints",
                "Check for undocumented features",
                "Use GraphQL instead of REST (or vice versa)",
                "Implement pagination or streaming",
                "Use webhooks instead of polling",
            ],
            "Resource limitation": [
                "Optimize memory usage",
                "Use streaming instead of loading all",
                "Implement lazy loading",
                "Use external storage",
                "Compress data",
            ],
        }
        
        return workarounds.get(barrier, [
            "Research alternative approaches",
            "Check documentation for hidden options",
            "Look for community solutions",
            "Try combining multiple methods",
        ])
    
    # ============================================================
    # ALTERNATIVE FINDER
    # ============================================================
    def _find_alternatives(self, problem: str) -> list:
        """Find alternative approaches."""
        
        alternatives = []
        problem_lower = problem.lower()
        
        # General alternatives
        alternatives.extend([
            "Try a completely different approach",
            "Break the problem into smaller parts",
            "Use automation instead of manual work",
            "Find a library that already solves this",
            "Ask the AI to generate custom solution",
        ])
        
        # Problem-specific alternatives
        if "api" in problem_lower:
            alternatives.extend([
                "Use web scraping instead of API",
                "Look for unofficial APIs",
                "Use browser automation (Selenium/Playwright)",
                "Check if there's a CLI tool instead",
            ])
        
        if "install" in problem_lower:
            alternatives.extend([
                "Try pip install with --user flag",
                "Use conda instead of pip",
                "Install from source",
                "Use Docker container",
            ])
        
        if "error" in problem_lower or "bug" in problem_lower:
            alternatives.extend([
                "Check stack overflow for similar issues",
                "Look at GitHub issues for the project",
                "Try older version that worked",
                "Use different implementation",
            ])
        
        return alternatives
    
    # ============================================================
    # HIDDEN OPTIONS FINDER
    # ============================================================
    def _find_hidden_options(self, problem: str) -> list:
        """Find hidden or undocumented options."""
        
        hidden = []
        problem_lower = problem.lower()
        
        if "python" in problem_lower:
            hidden.extend([
                "Check Python environment variables",
                "Look for debug/verbose flags",
                "Check for __pycache__ or .pyc files",
                "Use sys.flags for runtime options",
            ])
        
        if "node" in problem_lower or "npm" in problem_lower:
            hidden.extend([
                "Check NODE_OPTIONS environment",
                "Use npm --ignore-scripts flag",
                "Check for .npmrc configuration",
                "Use npx for temporary packages",
            ])
        
        if "git" in problem_lower:
            hidden.extend([
                "Use git config for global settings",
                "Check for git hooks",
                "Use git aliases for shortcuts",
                "Check .gitignore for patterns",
            ])
        
        if "api" in problem_lower:
            hidden.extend([
                "Check for versioned endpoints (v1, v2)",
                "Look for /debug or /admin endpoints",
                "Check alternative HTTP methods",
                "Look for undocumented parameters",
            ])
        
        hidden.extend([
            "Check environment variables",
            "Look for configuration files",
            "Check for CLI flags not in help",
            "Look for experimental features",
        ])
        
        return hidden
    
    # ============================================================
    # CREATIVE HACKS
    # ============================================================
    def _creative_hacks(self, problem: str) -> list:
        """Generate creative hacks."""
        
        hacks = [
            "Use the '10-minute rule' - if stuck for 10 min, try something completely different",
            "Ask 'what would happen if I did the opposite?'",
            "Look for similar solved problems in different domains",
            "Use rubber duck debugging - explain the problem out loud",
            "Take a break and return with fresh eyes",
        ]
        
        problem_lower = problem.lower()
        
        if "permission" in problem_lower:
            hacks.extend([
                "Try running as different user",
                "Check if there's a guest/anonymous mode",
                "Look for API alternatives that don't need auth",
            ])
        
        if "slow" in problem_lower:
            hacks.extend([
                "Profile the code to find bottleneck",
                "Use caching aggressively",
                "Consider if you're solving the right problem",
            ])
        
        if "complex" in problem_lower:
            hacks.extend([
                "Simplify the problem to core requirement",
                "Use existing libraries instead of building",
                "Break into micro-problems",
            ])
        
        return hacks
    
    # ============================================================
    # SPECIFIC LOOPHOLE PATTERNS
    # ============================================================
    def bypass_rate_limit(self, service: str) -> str:
        """Suggest ways to handle rate limiting."""
        
        strategies = [
            f"## Rate Limit Bypass Strategies for {service}\n",
            "### Immediate Solutions",
            "- Add random delays (1-5 seconds) between requests",
            "- Implement exponential backoff",
            "- Batch multiple operations into single requests",
            "",
            "### Architecture Changes",
            "- Use caching (Redis, local file)",
            "- Implement request queuing",
            "- Use multiple API keys/accounts",
            "- Rotate through different endpoints",
            "",
            "### Alternative Approaches",
            "- Look for bulk/batch endpoints",
            "- Use webhooks instead of polling",
            "- Check for higher tier access",
            "- Use official SDKs (they often handle limits)",
            "",
            "### Creative Solutions",
            "- Use different IP (proxy, VPN)",
            "- Schedule requests during off-peak hours",
            "- Use cached data when possible",
            "- Implement smart request prioritization",
        ]
        
        return "\n".join(strategies)
    
    def find_free_alternative(self, paid_tool: str) -> str:
        """Find free alternatives to paid tools."""
        
        # Common paid to free mappings
        alternatives = {
            "github copilot": ["Codeium", "Tabnine", "Aider", "Open Interpreter"],
            "chatgpt plus": ["Gemini free tier", "Claude free tier", "Local LLMs"],
            "jetbrains": ["VS Code", "VSCodium", "Neovim"],
            "figma pro": ["Penpot", "Inkscape", "Figma free tier"],
            "slack paid": ["Discord", "Matrix", "Rocket.Chat"],
            "notion paid": ["Obsidian", "Logseq", "Notion free tier"],
            "aws": ["Oracle Cloud free tier", "Google Cloud free tier", "Linode"],
            "vercel": ["Netlify", "Cloudflare Pages", "Railway free tier"],
        }
        
        paid_lower = paid_tool.lower()
        
        lines = [f"## Free Alternatives to {paid_tool}\n"]
        
        found = False
        for paid, free_list in alternatives.items():
            if paid in paid_lower or paid_lower in paid:
                lines.append(f"**Free alternatives:**")
                for alt in free_list:
                    lines.append(f"- {alt}")
                found = True
                break
        
        if not found:
            lines.append("No specific mapping found. Try:")
            lines.append("- Search for 'open source [tool name]'")
            lines.append("- Check GitHub for alternatives")
            lines.append("- Look for free tiers of similar services")
            lines.append("- Search 'awesome [category]' on GitHub")
        
        return "\n".join(lines)
    
    def fix_impossible(self, problem: str) -> str:
        """When something seems impossible, find a way."""
        
        analysis = [
            f"## Fixing the 'Impossible': {problem}\n",
            "### Step 1: Question Assumptions",
            "- What exactly makes this seem impossible?",
            "- Are there hidden constraints?",
            "- Is the goal truly what we need?\n",
            
            "### Step 2: Reframe the Problem",
            "- Can we solve a different problem that achieves the same result?",
            "- Is there a simpler version that's 'good enough'?",
            "- What would success actually look like?\n",
            
            "### Step 3: Creative Solutions",
            "- Use AI to generate 10 different approaches",
            "- Look for solutions in unrelated fields",
            "- Combine multiple partial solutions",
            "- Accept trade-offs (speed vs quality, etc.)\n",
            
            "### Step 4: Technical Hacks",
            "- Check for undocumented features",
            "- Look for beta/experimental options",
            "- Use alternative libraries or APIs",
            "- Implement at a different layer (network, file, etc.)\n",
            
            "### Step 5: When All Else Fails",
            "- Build a minimal version first",
            "- Use a completely different technology",
            "- Ask for help (StackOverflow, GitHub, forums)",
            "- Consider if this is actually worth solving",
        ]
        
        return "\n".join(analysis)
    
    # ============================================================
    # HISTORY
    # ============================================================
    def _save_loophole(self, problem: str, solutions: list):
        """Save loophole to history."""
        history_file = self.history_dir / "history.json"
        
        if history_file.exists():
            history = json.loads(history_file.read_text())
        else:
            history = []
        
        entry = {
            "problem": problem[:200],
            "solutions_count": len(solutions),
            "timestamp": datetime.now().isoformat()
        }
        
        history.append(entry)
        
        # Keep last 100
        if len(history) > 100:
            history = history[-100:]
        
        history_file.write_text(json.dumps(history, indent=2))
    
    def get_history(self) -> str:
        """Get loophole history."""
        history_file = self.history_dir / "history.json"
        
        if not history_file.exists():
            return "No loophole history yet."
        
        history = json.loads(history_file.read_text())
        
        lines = ["## Loophole History\n"]
        
        for entry in history[-10:]:
            lines.append(f"- {entry['problem'][:60]}... ({entry['solutions_count']} solutions)")
        
        return "\n".join(lines)

# Global instance
_loophole = None

def get_loophole() -> LoopholeFinder:
    global _loophole
    if _loophole is None:
        _loophole = LoopholeFinder()
    return _loophole
