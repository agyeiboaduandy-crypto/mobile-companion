"""
OWURA Memory System - Persistent learning and context storage
Makes OWURA smarter with every session.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

MEMORY_DIR = Path.home() / ".owura" / "memory"
MEMORY_FILE = MEMORY_DIR / "memory.json"
PROJECTS_FILE = MEMORY_DIR / "projects.json"
PATTERNS_FILE = MEMORY_DIR / "patterns.json"
LEARNINGS_FILE = MEMORY_DIR / "learnings.json"

class Memory:
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memory = self._load(MEMORY_FILE, {
            "facts": [],
            "preferences": {},
            "context": {},
            "last_updated": None
        })
        self.projects = self._load(PROJECTS_FILE, {"completed": [], "in_progress": []})
        self.patterns = self._load(PATTERNS_FILE, {"code": [], "commands": [], "solutions": []})
        self.learnings = self._load(LEARNINGS_FILE, [])
    
    def _load(self, path: Path, default: dict) -> dict:
        if path.exists():
            try:
                with open(path) as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save(self, path: Path, data: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def save_all(self):
        self.memory["last_updated"] = datetime.now().isoformat()
        self._save(MEMORY_FILE, self.memory)
        self._save(PROJECTS_FILE, self.projects)
        self._save(PATTERNS_FILE, self.patterns)
        self._save(LEARNINGS_FILE, self.learnings)
    
    # ============================================================
    # FACTS - Things to remember
    # ============================================================
    def add_fact(self, fact: str, category: str = "general"):
        """Add a fact to remember."""
        entry = {
            "fact": fact,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "times_recalled": 0
        }
        # Check for duplicates
        existing = [f for f in self.memory["facts"] if f["fact"] == fact]
        if not existing:
            self.memory["facts"].append(entry)
            self.save_all()
    
    def recall_facts(self, query: str = None, category: str = None) -> List[str]:
        """Recall relevant facts."""
        facts = self.memory["facts"]
        
        if category:
            facts = [f for f in facts if f["category"] == category]
        
        if query:
            query_lower = query.lower()
            relevant = []
            for f in facts:
                if query_lower in f["fact"].lower():
                    f["times_recalled"] = f.get("times_recalled", 0) + 1
                    relevant.append(f["fact"])
            return relevant
        
        return [f["fact"] for f in facts]
    
    # ============================================================
    # PREFERENCES - User patterns
    # ============================================================
    def set_preference(self, key: str, value: str):
        """Remember a user preference."""
        self.memory["preferences"][key] = {
            "value": value,
            "updated": datetime.now().isoformat()
        }
        self.save_all()
    
    def get_preference(self, key: str) -> Optional[str]:
        """Get a stored preference."""
        pref = self.memory["preferences"].get(key)
        return pref["value"] if pref else None
    
    # ============================================================
    # PROJECTS - Track what's been built
    # ============================================================
    def add_project(self, name: str, description: str, tech_stack: List[str], 
                   status: str = "completed", learnings: List[str] = None):
        """Record a project."""
        project = {
            "name": name,
            "description": description,
            "tech_stack": tech_stack,
            "status": status,
            "learnings": learnings or [],
            "created": datetime.now().isoformat()
        }
        
        if status == "completed":
            self.projects["completed"].append(project)
        else:
            self.projects["in_progress"].append(project)
        
        # Auto-extract patterns from project
        self._extract_patterns(project)
        self.save_all()
    
    def get_project_context(self, query: str = None) -> str:
        """Get context from past projects."""
        lines = []
        
        if self.projects["completed"]:
            lines.append("## Past Projects\n")
            for p in self.projects["completed"][-5:]:  # Last 5 projects
                lines.append(f"### {p['name']}")
                lines.append(f"- {p['description']}")
                lines.append(f"- Tech: {', '.join(p['tech_stack'])}")
                if p.get('learnings'):
                    lines.append(f"- Learnings: {'; '.join(p['learnings'][:3])}")
                lines.append("")
        
        if self.projects["in_progress"]:
            lines.append("## In Progress\n")
            for p in self.projects["in_progress"]:
                lines.append(f"- {p['name']}: {p['description']}")
        
        return "\n".join(lines) if lines else None
    
    # ============================================================
    # PATTERNS - Code patterns that work
    # ============================================================
    def add_pattern(self, pattern_type: str, pattern: str, context: str = ""):
        """Store a useful pattern."""
        entry = {
            "type": pattern_type,
            "pattern": pattern,
            "context": context,
            "times_used": 0,
            "created": datetime.now().isoformat()
        }
        
        if pattern_type not in self.patterns:
            self.patterns[pattern_type] = []
        
        # Check for duplicates
        existing = [p for p in self.patterns[pattern_type] if p["pattern"] == pattern]
        if not existing:
            self.patterns[pattern_type].append(entry)
            self.save_all()
    
    def get_pattern(self, pattern_type: str, query: str = None) -> List[str]:
        """Get patterns by type."""
        patterns = self.patterns.get(pattern_type, [])
        
        if query:
            query_lower = query.lower()
            return [p["pattern"] for p in patterns if query_lower in p["context"].lower() or query_lower in p["pattern"].lower()]
        
        return [p["pattern"] for p in patterns]
    
    def _extract_patterns(self, project: dict):
        """Extract patterns from a project."""
        tech_stack = project.get("tech_stack", [])
        
        # Pattern: tech stack combinations
        if len(tech_stack) > 1:
            self.add_pattern("tech_combos", " + ".join(tech_stack), 
                           f"Used in {project['name']}")
        
        # Pattern: project structure
        if "python" in [t.lower() for t in tech_stack]:
            self.add_pattern("structure", "Python project with setup.py and requirements.txt",
                           project["name"])
        if "node" in [t.lower() for t in tech_stack] or "javascript" in [t.lower() for t in tech_stack]:
            self.add_pattern("structure", "Node.js project with package.json",
                           project["name"])
    
    # ============================================================
    # LEARNINGS - What worked and what didn't
    # ============================================================
    def add_learning(self, what: str, outcome: str, context: str = "", 
                    category: str = "general"):
        """Record a learning experience."""
        learning = {
            "what": what,
            "outcome": outcome,
            "context": context,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check for duplicates
        existing = [l for l in self.learnings if l["what"] == what and l["outcome"] == outcome]
        if not existing:
            self.learnings.append(learning)
            
            # Also add as a fact for easy recall
            self.add_fact(f"{what} -> {outcome}", category)
            self.save_all()
    
    def get_learnings(self, category: str = None, query: str = None) -> List[str]:
        """Get relevant learnings."""
        learnings = self.learnings
        
        if category:
            learnings = [l for l in learnings if l["category"] == category]
        
        if query:
            query_lower = query.lower()
            learnings = [l for l in learnings if query_lower in l["what"].lower() or 
                        query_lower in l["outcome"].lower() or
                        query_lower in l.get("context", "").lower()]
        
        return [f"{l['what']} -> {l['outcome']}" for l in learnings[-10:]]
    
    # ============================================================
    # CONTEXT - Current session context
    # ============================================================
    def set_context(self, key: str, value: str):
        """Set current context."""
        self.memory["context"][key] = value
        self.save_all()
    
    def get_context(self, key: str = None) -> dict:
        """Get context."""
        if key:
            return self.memory["context"].get(key)
        return self.memory["context"]
    
    def clear_context(self):
        """Clear current context."""
        self.memory["context"] = {}
        self.save_all()

    def set_compacted_context(self, summary: str):
        """Store a compacted conversation summary."""
        self.memory["context"]["compacted"] = summary
        self.save_all()

    def get_compacted_context(self) -> Optional[str]:
        """Retrieve the compacted conversation summary."""
        return self.memory["context"].get("compacted")
    
    # ============================================================
    # SEARCH - Find relevant memories
    # ============================================================
    def search(self, query: str) -> str:
        """Search all memories for relevant information."""
        results = []
        
        # Search facts
        facts = self.recall_facts(query)
        if facts:
            results.append("### Relevant Facts")
            for f in facts[:5]:
                results.append(f"- {f}")
        
        # Search learnings
        learnings = self.get_learnings(query=query)
        if learnings:
            results.append("\n### Relevant Learnings")
            for l in learnings[:5]:
                results.append(f"- {l}")
        
        # Search patterns
        for ptype in self.patterns:
            patterns = self.get_pattern(ptype, query)
            if patterns:
                results.append(f"\n### {ptype.replace('_', ' ').title()} Patterns")
                for p in patterns[:3]:
                    results.append(f"- {p}")
        
        return "\n".join(results) if results else None
    
    # ============================================================
    # GET FULL CONTEXT - For AI prompts
    # ============================================================
    def get_full_context(self) -> str:
        """Get full memory context for AI prompts."""
        parts = []
        
        # User preferences
        if self.memory["preferences"]:
            prefs = "\n".join([f"- {k}: {v['value']}" for k, v in self.memory["preferences"].items()])
            parts.append(f"## User Preferences\n{prefs}")
        
        # Relevant learnings
        learnings = self.get_learnings()
        if learnings:
            parts.append(f"## Key Learnings\n" + "\n".join([f"- {l}" for l in learnings[:5]]))
        
        # Project context
        project_ctx = self.get_project_context()
        if project_ctx:
            parts.append(project_ctx)

        # Compacted conversation summary
        compacted = self.get_compacted_context()
        if compacted:
            parts.append(f"## Conversation Summary\n{compacted}")

        return "\n\n".join(parts) if parts else None

# Global memory instance
_memory = None

def get_memory() -> Memory:
    global _memory
    if _memory is None:
        _memory = Memory()
    return _memory
