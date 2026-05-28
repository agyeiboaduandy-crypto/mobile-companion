"""
OWURA Pro Tools - Real-world application development
Complete toolkit for building production-ready apps.
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

PROJECTS_DIR = Path.home() / ".owura" / "projects"

class ProTools:
    def __init__(self):
        self.projects_dir = PROJECTS_DIR
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    # ============================================================
    # PROJECT SCAFFOLDING
    # ============================================================
    def create_project(self, name: str, template: str, path: str = None) -> dict:
        """Create a complete project from template."""
        if not path:
            path = str(Path.cwd() / name)
        
        project_path = Path(path)
        project_path.mkdir(parents=True, exist_ok=True)
        
        templates = {
            "flask-api": self._flask_api,
            "fastapi": self._fastapi_project,
            "react": self._react_project,
            "express": self._express_project,
            "django": self._django_project,
            "nextjs": self._nextjs_project,
            "python-cli": self._python_cli,
            "rust-cli": self._rust_cli,
            "go-api": self._go_api,
        }
        
        if template not in templates:
            return {"error": f"Unknown template: {template}. Available: {', '.join(templates.keys())}"}
        
        result = templates[template](project_path, name)
        
        # Initialize git
        self._run_cmd("git init", project_path)
        self._run_cmd("git add .", project_path)
        self._run_cmd(f'git commit -m "Initial commit: {name}"', project_path)
        
        # Record project
        self._record_project(name, template, path)
        
        return {"success": True, "path": str(project_path), "template": template}
    
    def _flask_api(self, path: Path, name: str):
        """Create Flask API project."""
        # Main app
        (path / "app.py").write_text(f'''#!/usr/bin/env python3
"""Flask API - {name}"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({{"name": "{name}", "status": "running"}})

@app.route("/api/health")
def health():
    return jsonify({{"status": "healthy"}})

@app.route("/api/<endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def api_handler(endpoint):
    if request.method == "GET":
        return jsonify({{"endpoint": endpoint, "action": "list"}})
    elif request.method == "POST":
        data = request.get_json()
        return jsonify({{"endpoint": endpoint, "action": "create", "data": data}})
    elif request.method == "PUT":
        data = request.get_json()
        return jsonify({{"endpoint": endpoint, "action": "update", "data": data}})
    elif request.method == "DELETE":
        return jsonify({{"endpoint": endpoint, "action": "delete"}})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
''')
        
        # Requirements
        (path / "requirements.txt").write_text("""flask>=3.0.0
flask-cors>=4.0.0
gunicorn>=21.0.0
python-dotenv>=1.0.0
""")
        
        # Config
        (path / ".env.example").write_text("""FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
PORT=5000
""")
        
        # Docker
        (path / "Dockerfile").write_text("""FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
""")
        
        (path / "docker-compose.yml").write_text(f"""version: '3.8'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///app.db
    volumes:
      - ./data:/app/data
""")
        
        # README
        (path / "README.md").write_text(f"""# {name}

Flask API project

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## Docker

```bash
docker-compose up
```

## API Endpoints

- GET `/` - Home
- GET `/api/health` - Health check
- GET `/api/<endpoint>` - List
- POST `/api/<endpoint>` - Create
- PUT `/api/<endpoint>` - Update
- DELETE `/api/<endpoint>` - Delete
""")
        
        # .gitignore
        (path / ".gitignore").write_text("""__pycache__/
*.pyc
.env
venv/
*.db
dist/
build/
""")
    
    def _fastapi_project(self, path: Path, name: str):
        """Create FastAPI project."""
        (path / "main.py").write_text(f'''#!/usr/bin/env python3
"""FastAPI - {name}"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="{name}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

items = []

@app.get("/")
def home():
    return {{"name": "{name}", "status": "running"}}

@app.get("/api/health")
def health():
    return {{"status": "healthy"}}

@app.get("/api/items")
def list_items():
    return items

@app.post("/api/items")
def create_item(item: Item):
    items.append(item.dict())
    return item

@app.get("/api/items/{{item_id}}")
def get_item(item_id: int):
    if item_id < len(items):
        return items[item_id]
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/api/items/{{item_id}}")
def update_item(item_id: int, item: Item):
    if item_id < len(items):
        items[item_id] = item.dict()
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/items/{{item_id}}")
def delete_item(item_id: int):
    if item_id < len(items):
        return items.pop(item_id)
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')
        
        (path / "requirements.txt").write_text("""fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
python-dotenv>=1.0.0
""")
        
        (path / "README.md").write_text(f"""# {name}

FastAPI project

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## API Docs

Visit http://localhost:8000/docs for auto-generated API docs.
""")
        
        (path / ".gitignore").write_text("""__pycache__/
*.pyc
.env
venv/
""")
    
    def _react_project(self, path: Path, name: str):
        """Create React project."""
        # Create with Vite
        self._run_cmd(f"npm create vite@latest . -- --template react", path)
        self._run_cmd("npm install", path)
        
        (path / "README.md").write_text(f"""# {name}

React project

## Setup

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```
""")
    
    def _express_project(self, path: Path, name: str):
        """Create Express.js project."""
        (path / "package.json").write_text(json.dumps({
            "name": name,
            "version": "1.0.0",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js"
            },
            "dependencies": {
                "express": "^4.18.0",
                "cors": "^2.8.5",
                "dotenv": "^16.0.0"
            },
            "devDependencies": {
                "nodemon": "^3.0.0"
            }
        }, indent=2))
        
        (path / "server.js").write_text(f'''const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {{
    res.json({{ name: "{name}", status: "running" }});}});

app.get("/api/health", (req, res) => {{
    res.json({{ status: "healthy" }});}});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {{
    console.log(`Server running on port ${{PORT}}`);}});
''')
        
        (path / ".env.example").write_text("PORT=3000\n")
        (path / ".gitignore").write_text("node_modules/\n.env\ndist/\n")
        
        self._run_cmd("npm install", path)
    
    def _django_project(self, path: Path, name: str):
        """Create Django project."""
        self._run_cmd(f"django-admin startproject {name} .", path)
        self._run_cmd(f"python manage.py startapp api", path)
    
    def _nextjs_project(self, path: Path, name: str):
        """Create Next.js project."""
        self._run_cmd(f"npx create-next-app@latest . --typescript --tailwind --app", path)
    
    def _python_cli(self, path: Path, name: str):
        """Create Python CLI tool."""
        (path / f"{name.replace('-', '_').replace(' ', '_')}.py").write_text(f'''#!/usr/bin/env python3
"""CLI Tool: {name}"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="{name}")
    subparsers = parser.add_subparsers(dest="command")
    
    # Add commands here
    subparsers.add_parser("run", help="Run the tool")
    subparsers.add_parser("build", help="Build project")
    subparsers.add_parser("test", help="Run tests")
    
    args = parser.parse_args()
    
    if args.command == "run":
        print("Running...")
    elif args.command == "build":
        print("Building...")
    elif args.command == "test":
        print("Testing...")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
''')
        
        (path / "requirements.txt").write_text("click>=8.0.0\nrich>=13.0.0\n")
        (path / "setup.py").write_text(f'''from setuptools import setup

setup(
    name="{name}",
    version="1.0.0",
    py_modules=["{name.replace('-', '_')}"],
    install_requires=["click", "rich"],
    entry_points={{
        "console_scripts": [
            "{name}={name.replace('-', '_')}:main",
        ],
    }},
)
''')
    
    def _rust_cli(self, path: Path, name: str):
        """Create Rust CLI project."""
        self._run_cmd(f"cargo init --name {name}", path)
    
    def _go_api(self, path: Path, name: str):
        """Create Go API project."""
        (path / "main.go").write_text(f'''package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
)

type Response struct {
    Name   string `json:"name"`
    Status string `json:"status"`
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(Response{Name: "{name}", Status: "running"})
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(Response{Status: "healthy"})
}

func main() {{
    http.HandleFunc("/", homeHandler)
    http.HandleFunc("/api/health", healthHandler)
    
    fmt.Println("Server running on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}}
''')
        
        (path / "go.mod").write_text(f"module {name}\n\ngo 1.21\n")
        (path / "README.md").write_text(f"# {name}\n\nGo API project\n\n## Setup\n\n```bash\ngo run main.go\n```\n")
    
    def _run_cmd(self, cmd: str, cwd: Path) -> tuple:
        """Run shell command."""
        try:
            result = subprocess.run(
                cmd, shell=True, cwd=cwd,
                capture_output=True, text=True, timeout=60
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1
    
    def _record_project(self, name: str, template: str, path: str):
        """Record project in memory."""
        from owura.memory import get_memory
        memory = get_memory()
        memory.add_project(
            name=name,
            description=f"{template} project",
            tech_stack=[template],
            status="in_progress"
        )
    
    # ============================================================
    # CODE GENERATION
    # ============================================================
    def generate_code(self, spec: str) -> str:
        """Generate production code from specification."""
        # This would normally call the AI, but here we return a template
        return f"""# Generated code for: {spec}
# Run with: python generated.py
"""
    
    # ============================================================
    # DATABASE HELPERS
    # ============================================================
    def create_migration(self, app_type: str, model_name: str, fields: dict) -> str:
        """Generate database migration."""
        if app_type in ["flask", "fastapi"]:
            return f'''from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class {model_name}(Base):
    __tablename__ = "{model_name.lower()}s"
    
    id = Column(Integer, primary_key=True, index=True)
    {chr(10).join(f'{k} = Column({v})' for k, v in fields.items())}
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
'''
        return "# Migration generated"
    
    # ============================================================
    # TEST GENERATION
    # ============================================================
    def generate_tests(self, file_path: str) -> str:
        """Generate tests for a Python file."""
        return f'''import pytest
from {Path(file_path).stem} import *

def test_basic():
    assert True

def test_api_endpoint():
    # Add your tests here
    pass
'''
    
    # ============================================================
    # DEPLOYMENT
    # ============================================================
    def generate_deploy_config(self, platform: str, project_name: str) -> str:
        """Generate deployment configuration."""
        configs = {
            "docker": f"""version: '3.8'
services:
  app:
    build: .
    ports:
      - "80:8000"
    environment:
      - ENV=production
""",
            "heroku": f"""web: gunicorn app:app
runtime: python-3.11
""",
            "railway": f"""[build]
builder = "nixpacks"

[deploy]
startCommand = "python app.py"
""",
            "vercel": f"""{{
  "version": 2,
  "builds": [
    {{ "src": "app.py", "use": "@vercel/python" }}
  ],
  "routes": [
    {{ "src": "/(.*)", "dest": "app.py" }}
  ]
}}
""",
        }
        return configs.get(platform, "# Unknown platform")
    
    # ============================================================
    # PROJECT ANALYSIS
    # ============================================================
    def analyze_project(self, path: str = ".") -> dict:
        """Analyze a project and suggest improvements."""
        project_path = Path(path)
        
        analysis = {
            "files": len(list(project_path.rglob("*"))),
            "languages": [],
            "has_tests": False,
            "has_docker": False,
            "has_ci": False,
            "has_docs": False,
            "suggestions": [],
        }
        
        # Detect languages
        for ext in [".py", ".js", ".ts", ".go", ".rs", ".java"]:
            if list(project_path.rglob(f"*{ext}")):
                lang_map = {".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
                           ".go": "Go", ".rs": "Rust", ".java": "Java"}
                analysis["languages"].append(lang_map[ext])
        
        # Check for common files
        if list(project_path.rglob("test_*")) or list(project_path.rglob("*_test.py")):
            analysis["has_tests"] = True
        else:
            analysis["suggestions"].append("Add tests (test_*.py)")
        
        if (project_path / "Dockerfile").exists():
            analysis["has_docker"] = True
        else:
            analysis["suggestions"].append("Add Dockerfile for containerization")
        
        if (project_path / ".github").exists():
            analysis["has_ci"] = True
        else:
            analysis["suggestions"].append("Add GitHub Actions CI/CD")
        
        if (project_path / "README.md").exists():
            analysis["has_docs"] = True
        else:
            analysis["suggestions"].append("Add README.md documentation")
        
        return analysis

# Global instance
_pro_tools = None

def get_pro_tools() -> ProTools:
    global _pro_tools
    if _pro_tools is None:
        _pro_tools = ProTools()
    return _pro_tools
