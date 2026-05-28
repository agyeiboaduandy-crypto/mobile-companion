"""
OWURA Skills - Reusable capabilities for building anything
These skills help OWURA understand and execute coding tasks.
"""

SKILLS = {
    "web-search": {
        "name": "Web Search",
        "description": "Search the web for documentation, examples, and solutions",
        "trigger": ["search", "find", "look up", "google", "documentation"],
        "prompt": """When the user asks to search or find something:
1. Use curl to fetch information from URLs
2. Parse HTML/text content to extract relevant information
3. Summarize findings clearly
4. Provide links to sources

Example: curl -s "https://api.github.com/search/repositories?q=termux" | python3 -m json.tool""",
    },
    
    "file-operations": {
        "name": "File Operations",
        "description": "Create, read, update, and delete files",
        "trigger": ["create file", "write file", "read file", "delete file", "mkdir", "touch"],
        "prompt": """File operations skill:
- Create: echo "content" > file.txt or cat > file << 'EOF' ... EOF
- Read: cat file.txt or less file.txt
- Update: sed -i 's/old/new/g' file.txt
- Delete: rm file.txt
- Directory: mkdir -p path/to/dir
- List: ls -la or find . -name "*.py"
Always use proper paths and handle errors.""",
    },
    
    "git-operations": {
        "name": "Git Operations",
        "description": "Version control with git",
        "trigger": ["git", "commit", "push", "pull", "clone", "branch", "merge"],
        "prompt": """Git operations skill:
- Initialize: git init
- Clone: git clone <url>
- Status: git status
- Add: git add . or git add <file>
- Commit: git commit -m "message"
- Push: git push origin <branch>
- Pull: git pull
- Branch: git branch <name> / git checkout <name>
- Log: git log --oneline -10
Always commit with meaningful messages.""",
    },
    
    "python-dev": {
        "name": "Python Development",
        "description": "Write and run Python code",
        "trigger": ["python", "pip", "virtualenv", "pytest", "flask", "django"],
        "prompt": """Python development skill:
- Run: python3 script.py or python script.py
- Install: pip install <package>
- Virtual env: python3 -m venv venv && source venv/bin/activate
- Test: pytest or python -m unittest
- Format: black . or autopep8
- Lint: flake8 or pylint
- Type check: mypy .
Use type hints, docstrings, and follow PEP 8.""",
    },
    
    "nodejs-dev": {
        "name": "Node.js Development",
        "description": "Write and run JavaScript/Node.js code",
        "trigger": ["node", "npm", "yarn", "package.json", "express", "react"],
        "prompt": """Node.js development skill:
- Run: node script.js
- Install: npm install <package>
- Init: npm init -y
- Scripts: npm run <script>
- Dev: nodemon or node --watch
- Test: npm test
- Lint: eslint .
Use modern ES6+ syntax, async/await, and proper error handling.""",
    },
    
    "shell-scripting": {
        "name": "Shell Scripting",
        "description": "Write and execute bash/shell scripts",
        "trigger": ["bash", "shell", "script", "sh", "chmod", "bashrc"],
        "prompt": """Shell scripting skill:
- Shebang: #!/bin/bash or #!/bin/sh
- Make executable: chmod +x script.sh
- Run: ./script.sh or bash script.sh
- Variables: VAR="value" (no spaces around =)
- Conditionals: if [ condition ]; then ... fi
- Loops: for i in 1 2 3; do ... done
- Functions: func() { ... }
- Exit codes: exit 0 (success), exit 1 (error)
Use shellcheck to validate scripts.""",
    },
    
    "api-integration": {
        "name": "API Integration",
        "description": "Connect to REST APIs and web services",
        "trigger": ["api", "rest", "http", "curl", "fetch", "endpoint"],
        "prompt": """API integration skill:
- GET: curl -s "https://api.example.com/endpoint"
- POST: curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' URL
- Headers: curl -H "Authorization: Bearer TOKEN" URL
- JSON parsing: curl -s URL | python3 -m json.tool
- Python requests: import requests; r = requests.get(url); print(r.json())
Always handle errors and check response status codes.""",
    },
    
    "database": {
        "name": "Database Operations",
        "description": "Work with SQLite, PostgreSQL, MongoDB",
        "trigger": ["database", "sql", "sqlite", "postgres", "mongo", "query"],
        "prompt": """Database skill:
- SQLite: sqlite3 database.db
- Create table: CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
- Insert: INSERT INTO users (name) VALUES ('John');
- Select: SELECT * FROM users WHERE id = 1;
- Python: import sqlite3; conn = sqlite3.connect('db.db')
- MongoDB: mongosh or use pymongo
Use parameterized queries to prevent SQL injection.""",
    },
    
    "docker": {
        "name": "Docker Operations",
        "description": "Container management with Docker",
        "trigger": ["docker", "container", "image", "dockerfile", "compose"],
        "prompt": """Docker skill:
- Build: docker build -t name .
- Run: docker run -d -p 8080:80 name
- List: docker ps or docker ps -a
- Stop: docker stop <id>
- Remove: docker rm <id>
- Logs: docker logs <id>
- Compose: docker-compose up -d
- Exec: docker exec -it <id> bash
Use multi-stage builds for smaller images.""",
    },
    
    "security": {
        "name": "Security Best Practices",
        "description": "Secure coding and system hardening",
        "trigger": ["security", "encrypt", "hash", "password", "auth", "token"],
        "prompt": """Security skill:
- Hash: echo -n "password" | sha256sum
- Encrypt: openssl enc -aes-256-cbc -salt -in file -out file.enc
- Generate key: openssl rand -hex 32
- Check ports: netstat -tlnp or ss -tlnp
- SSH: ssh-keygen -t ed25519
- Never hardcode secrets, use environment variables
- Validate all user input
- Use HTTPS for all API calls""",
    },
    
    "testing": {
        "name": "Testing & Debugging",
        "description": "Write and run tests, debug code",
        "trigger": ["test", "debug", "assert", "mock", "coverage"],
        "prompt": """Testing skill:
- Python: pytest, python -m unittest
- Node: npm test, jest
- Debug: python -m pdb script.py
- Coverage: pytest --cov
- Lint: flake8, pylint, eslint
- Type check: mypy, typescript
Write tests first (TDD), aim for >80% coverage.""",
    },
    
    "deployment": {
        "name": "Deployment",
        "description": "Deploy apps to servers and cloud",
        "trigger": ["deploy", "server", "nginx", "systemd", "pm2", "heroku"],
        "prompt": """Deployment skill:
- Process manager: pm2 start app.js, pm2 save
- Nginx config: /etc/nginx/sites-available/
- Systemd: sudo systemctl enable/start <service>
- SSH deploy: rsync -avz ./dist user@server:/path/
- Environment: export VAR=value or use .env files
- Health check: curl -s http://localhost:port/health
Always use environment variables for config.""",
    },
}

# MCP Servers - Model Context Protocol integrations
MCP_SERVERS = {
    "context7": {
        "name": "Context7",
        "description": "Up-to-date documentation for any library/framework",
        "url": "https://api.context7.com",
        "usage": """To fetch documentation:
curl -s "https://api.context7.com/v1/query" \\
  -H "Content-Type: application/json" \\
  -d '{"library": "rich", "topic": "console"}'""",
    },
    
    "web-search": {
        "name": "Web Search",
        "description": "Search the web for information",
        "provider": "duckduckgo",
        "usage": """To search:
curl -s "https://api.duckduckgo.com/?q=query&format=json" | python3 -m json.tool""",
    },
    
    "github": {
        "name": "GitHub",
        "description": "Access GitHub API for repos, issues, code",
        "url": "https://api.github.com",
        "usage": """GitHub API:
curl -s "https://api.github.com/repos/user/repo" | python3 -m json.tool
Search: curl -s "https://api.github.com/search/repositories?q=termux" """,
    },
    
    "pypi": {
        "name": "PyPI",
        "description": "Search Python packages",
        "url": "https://pypi.org/pypi",
        "usage": """Search PyPI:
curl -s "https://pypi.org/pypi/requests/json" | python3 -m json.tool""",
    },
    
    "npm": {
        "name": "npm",
        "description": "Search Node.js packages",
        "url": "https://registry.npmjs.org",
        "usage": """Search npm:
curl -s "https://registry.npmjs.org/express" | python3 -m json.tool""",
    },
    
    "stackoverflow": {
        "name": "Stack Overflow",
        "description": "Search Stack Overflow for solutions",
        "usage": """Search SO:
curl -s "https://api.stackexchange.com/2.3/search?intitle=termux&site=stackoverflow" | python3 -m json.tool""",
    },
    
    "devdocs": {
        "name": "DevDocs",
        "description": "Access developer documentation",
        "usage": """Fetch docs:
curl -s "https://devdocs.io/python~3.11/" """,
    },
    
    "github-copilot": {
        "name": "GitHub Copilot",
        "description": "Code suggestions (requires token)",
        "usage": "Configure with: /mcp copilot --token <token>",
    },
}

def get_skill_help():
    """Get formatted help for all skills."""
    lines = ["## Available Skills\n"]
    for key, skill in SKILLS.items():
        lines.append(f"- **{skill['name']}** ({key}): {skill['description']}")
    return "\n".join(lines)

def get_mcp_help():
    """Get formatted help for all MCPs."""
    lines = ["## Available MCPs\n"]
    for key, mcp in MCP_SERVERS.items():
        lines.append(f"- **{mcp['name']}** ({key}): {mcp['description']}")
    return "\n".join(lines)

def find_relevant_skill(user_input):
    """Find skills relevant to user input."""
    user_lower = user_input.lower()
    relevant = []
    
    for key, skill in SKILLS.items():
        for trigger in skill["trigger"]:
            if trigger in user_lower:
                relevant.append(skill)
                break
    
    return relevant

def get_skill_context(user_input):
    """Get context from relevant skills for AI prompt."""
    skills = find_relevant_skill(user_input)
    if not skills:
        return ""
    
    context = "\n\n## Relevant Skills\n"
    for skill in skills:
        context += f"\n### {skill['name']}\n{skill['prompt']}\n"
    
    return context
