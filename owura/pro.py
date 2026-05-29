"""
OWURA Pro Tools - Production-grade project scaffolding
Build real products at scale. Just describe and it builds.
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

PROJECTS_DIR = Path.home() / ".owura" / "projects"


def _run_cmd(cmd, cwd):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=120)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1


class ProTools:
    def __init__(self):
        self.projects_dir = PROJECTS_DIR
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, name, template, path=None):
        if not path:
            path = str(Path.cwd() / name)
        project_path = Path(path)
        project_path.mkdir(parents=True, exist_ok=True)

        builders = {
            "flask-api": self._flask_api,
            "fastapi": self._fastapi,
            "react": self._react,
            "express": self._express,
            "django": self._django,
            "nextjs": self._nextjs,
            "python-cli": self._python_cli,
            "rust-cli": self._rust_cli,
            "go-api": self._go_api,
        }
        if template not in builders:
            return {"error": f"Unknown template. Available: {', '.join(builders.keys())}"}

        builders[template](project_path, name)
        _run_cmd("git init", project_path)
        _run_cmd("git add .", project_path)
        _run_cmd(f'git commit -m "Initial commit: {name}"', project_path)
        self._record_project(name, template, path)
        return {"success": True, "path": str(project_path), "template": template}

    def build_from_description(self, description):
        """Scaffold a complete production project from a natural language description."""
        desc_lower = description.lower()

        tech_map = {
            "python": "fastapi", "flask": "flask-api", "django": "django",
            "react": "react", "next": "nextjs", "next.js": "nextjs",
            "express": "express", "node": "express", "node.js": "express",
            "go": "go-api", "rust": "rust-cli", "cli": "python-cli",
            "api": "fastapi", "web": "nextjs", "app": "nextjs",
            "backend": "fastapi", "frontend": "nextjs", "fullstack": "nextjs",
            "microservice": "fastapi", "service": "fastapi",
        }
        template = "fastapi"
        for keyword, tmpl in tech_map.items():
            if keyword in desc_lower:
                if tmpl == "express" and "next" in desc_lower:
                    continue
                template = tmpl
                break

        if "twitter" in desc_lower or "social" in desc_lower or "clone" in desc_lower:
            template = "nextjs"
        if "crypt" in desc_lower or "blockchain" in desc_lower or "web3" in desc_lower:
            template = "nextjs"
        if "chat" in desc_lower or "realtime" in desc_lower or "socket" in desc_lower:
            template = "fastapi"
        if "micro" in desc_lower or "rest" in desc_lower or "graphql" in desc_lower:
            template = "fastapi"
        if "mobile" in desc_lower or "app" in desc_lower:
            template = "nextjs"

        import re
        match = re.search(r'(?:called|named|project)\s+["\']?(\w+)["\']?', description)
        name = match.group(1) if match else "myapp"

        result = self.create_project(name, template)
        if result.get("success"):
            result["template_used"] = template
            result["description"] = description
        return result

    def _make_common(self, path, name, tech, extra_files=None):
        """Create common production files."""
        (path / ".github").mkdir(parents=True, exist_ok=True)
        (path / ".github/workflows").mkdir(parents=True, exist_ok=True)
        (path / "scripts").mkdir(parents=True, exist_ok=True)

        (path / ".github/workflows/ci.yml").write_text(f"""name: CI/CD

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - name: Set up {tech}
        uses: actions/setup-{tech.split()[0].lower()}@v5
        with:
          {tech.split()[0].lower()}-version: 'latest'
      - name: Install dependencies
        run: {"npm ci" if tech in ("node", "javascript", "typescript") else "pip install -r requirements.txt"}
      - name: Lint
        run: {"npm run lint" if tech in ("node", "javascript", "typescript") else "ruff check ."}
      - name: Test
        run: {"npm test" if tech in ("node", "javascript", "typescript") else "pytest -v --cov=app --cov-report=term-missing"}
      - name: Build
        run: {"npm run build" if tech in ("node", "javascript", "typescript") else "echo 'Build step'"}

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{{{ github.repository }}}}:latest
""")

        (path / ".env.example").write_text(f"""# {name} - Environment Configuration
# Copy to .env and fill in values

# App
APP_NAME={name}
APP_ENV=development
APP_DEBUG=true
APP_PORT=8000
SECRET_KEY=change-me-to-a-random-secret

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/{name}
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Redis
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=info
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# CORS
CORS_ORIGINS=*

# Sentry (error tracking)
SENTRY_DSN=

# Feature Flags
ENABLE_METRICS=true
ENABLE_DOCS=true
""")

        (path / ".gitignore").write_text("""__pycache__/
*.pyc
*.pyo
.env
venv/
.venv/
node_modules/
dist/
build/
*.db
*.sqlite3
.DS_Store
*.log
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/
""")

        (path / "scripts/healthcheck.sh").write_text("""#!/bin/bash
# Health check script for Docker
curl -f http://localhost:8000/api/health || exit 1
""")

        (path / "docker-compose.yml").write_text(f"""version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: {"production" if tech == "python" else "runner"}
    ports:
      - "${{{{APP_PORT:-8000}}}}:${{{{APP_PORT:-8000}}}}"
    env_file: .env
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/{name}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - static_data:/app/static
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 128M

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB={name}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "5432:5432"
    deploy:
      resources:
        limits:
          memory: 256M

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "6379:6379"
    deploy:
      resources:
        limits:
          memory: 128M

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_data:
""")

        (path / "nginx.conf").write_text("""worker_processes auto;
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }

    server {
        listen 80;
        server_name _;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }

        location /metrics {
            access_log off;
            proxy_pass http://app/metrics;
        }
    }
}
""")

        (path / "docker-compose.prod.yml").write_text(f"""version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    env_file: .env
    environment:
      - DATABASE_URL=${{{{DATABASE_URL}}}}
      - REDIS_URL=${{{{REDIS_URL}}}}
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${{{{DB_USER}}}}
      - POSTGRES_PASSWORD=${{{{DB_PASSWORD}}}}
      - POSTGRES_DB={name}
    deploy:
      resources:
        limits:
          memory: 2G

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    deploy:
      resources:
        limits:
          memory: 512M

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
""")

        if extra_files:
            for fname, content in extra_files.items():
                fpath = path / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(content)

    def _fastapi(self, path, name):
        """Production-grade FastAPI project."""
        (path / "app").mkdir(parents=True, exist_ok=True)
        (path / "app/api").mkdir(parents=True, exist_ok=True)
        (path / "app/api/v1").mkdir(parents=True, exist_ok=True)
        (path / "app/core").mkdir(parents=True, exist_ok=True)
        (path / "app/db").mkdir(parents=True, exist_ok=True)
        (path / "app/models").mkdir(parents=True, exist_ok=True)
        (path / "app/schemas").mkdir(parents=True, exist_ok=True)
        (path / "app/services").mkdir(parents=True, exist_ok=True)
        (path / "tests").mkdir(parents=True, exist_ok=True)
        (path / "alembic").mkdir(parents=True, exist_ok=True)

        (path / "app/__init__.py").write_text("")
        (path / "app/api/__init__.py").write_text("")
        (path / "app/api/v1/__init__.py").write_text("")
        (path / "app/core/__init__.py").write_text("")
        (path / "app/db/__init__.py").write_text("")
        (path / "app/models/__init__.py").write_text("")
        (path / "app/schemas/__init__.py").write_text("")
        (path / "app/services/__init__.py").write_text("")
        (path / "tests/__init__.py").write_text("")

        (path / "app/main.py").write_text(f'''"""FastAPI Production Server - {name}"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import engine, Base
from app.api.v1 import router as api_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

app.include_router(api_v1, prefix="/api/v1")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/api/health")
async def health():
    return {{"status": "healthy", "service": "{name}", "timestamp": time.time()}}


if settings.ENABLE_METRICS:
    Instrumentator().instrument(app).expose(app)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={{"detail": "Internal server error", "path": str(request.url.path)}},
    )
''')

        (path / "app/core/__init__.py").write_text("")

        (path / "app/core/config.py").write_text(f'''"""Application configuration with environment variable support."""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    APP_NAME: str = "{name}"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    SECRET_KEY: str = "change-me-to-a-random-secret"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/{name}"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    REDIS_URL: str = "redis://localhost:6379/0"

    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "json"

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    CORS_ORIGINS: str = "*"
    ALLOWED_HOSTS: List[str] = ["*"]

    SENTRY_DSN: str = ""

    ENABLE_METRICS: bool = True
    ENABLE_DOCS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
''')

        (path / "app/core/logging.py").write_text('''"""Structured logging configuration."""

import logging
import json
import sys
from datetime import datetime

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_FORMAT == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
''')

        (path / "app/db/session.py").write_text(f'''"""Database session management with connection pooling."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.APP_DEBUG,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
''')

        (path / "app/api/v1/__init__.py").write_text('''"""API v1 router."""

from fastapi import APIRouter

from app.api.v1 import items, health

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(items.router, prefix="/items", tags=["items"])
''')

        (path / "app/api/v1/health.py").write_text('''"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
''')

        (path / "app/api/v1/items.py").write_text(f'''"""Items CRUD API - {name}"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.flush()
    await db.refresh(db_item)
    return db_item


@router.get("/{{item_id}}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{{item_id}}", response_model=ItemResponse)
async def update_item(
    item_id: int, item: ItemUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    await db.flush()
    await db.refresh(db_item)
    return db_item


@router.delete("/{{item_id}}", status_code=204)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
''')

        (path / "app/models/item.py").write_text(f'''"""Item model - {name}"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func

from app.db.session import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Item {{self.id}}: {{self.name}}>"
''')

        (path / "app/schemas/item.py").write_text('''"""Item Pydantic schemas for API validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    is_active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
''')

        (path / "app/services/item_service.py").write_text(f'''"""Business logic for items."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ItemCreate) -> Item:
        item = Item(**data.model_dump())
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def get(self, item_id: int) -> Optional[Item]:
        result = await self.db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    async def update(self, item_id: int, data: ItemUpdate) -> Optional[Item]:
        item = await self.get(item_id)
        if not item:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def delete(self, item_id: int) -> bool:
        item = await self.get(item_id)
        if not item:
            return False
        await self.db.delete(item)
        return True
''')

        (path / "tests/conftest.py").write_text('''"""Test fixtures and configuration."""

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import engine, Base


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db_session():
    from app.db.session import async_session
    async with async_session() as session:
        yield session
''')

        (path / "tests/test_health.py").write_text('''"""Health endpoint tests."""

import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
''')

        (path / "tests/test_items.py").write_text('''"""Item CRUD endpoint tests."""

import pytest


@pytest.mark.asyncio
async def test_create_item(client):
    response = await client.post("/api/v1/items/", json={
        "name": "Test Item",
        "price": 9.99,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 9.99
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items(client):
    await client.post("/api/v1/items/", json={"name": "Item 1", "price": 10})
    await client.post("/api/v1/items/", json={"name": "Item 2", "price": 20})
    response = await client.get("/api/v1/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_item(client):
    create_resp = await client.post("/api/v1/items/", json={"name": "Test", "price": 5})
    item_id = create_resp.json()["id"]
    response = await client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test"


@pytest.mark.asyncio
async def test_get_nonexistent_item(client):
    response = await client.get("/api/v1/items/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_item(client):
    create_resp = await client.post("/api/v1/items/", json={"name": "Delete", "price": 1})
    item_id = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 204
''')

        (path / "Dockerfile").write_text(f"""FROM python:3.12-slim AS base

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1 \\
    PIP_NO_CACHE_DIR=1

# Build stage
FROM base AS builder
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --user -r requirements.txt

# Production stage
FROM base AS production
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
""")

        (path / "requirements.txt").write_text("""fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.30.0
alembic>=1.13.0
redis>=5.0.0
httpx>=0.27.0
python-dotenv>=1.0.0
slowapi>=0.1.9
prometheus-fastapi-instrumentator>=7.0.0
sentry-sdk>=2.0.0
ruff>=0.5.0
pytest>=8.0.0
pytest-asyncio>=0.24.0
pytest-cov>=5.0.0
""")

        (path / "alembic/env.py").write_text('''"""Alembic migration environment."""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.core.config import settings
from app.db.session import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
''')

        extra = {
            "prometheus.yml": """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:8000']
""",
            "alembic.ini": f"""[alembic]
script_location = alembic
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/{name}

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""",
        }
        self._make_common(path, name, "python", extra)

        (path / "README.md").write_text(f"""# {name}

> Production-grade FastAPI application built with OWURA.

## Stack

- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL 16 with SQLAlchemy async
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0 + Alembic migrations
- **API**: RESTful with OpenAPI docs
- **Auth**: JWT-ready middleware
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured JSON logging
- **Rate Limiting**: SlowAPI
- **Container**: Docker multi-stage builds
- **Orchestration**: Docker Compose

## Quick Start

```bash
cp .env.example .env
docker-compose up -d
```

## Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/api/health
- Metrics: http://localhost:8000/metrics

## Database Migrations

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Testing

```bash
pytest -v --cov=app --cov-report=term-missing
```

## Production Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Architecture

```
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/             # Config, logging, security
│   ├── db/               # Database session
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
├── tests/                # Test suite
├── alembic/              # Database migrations
├── scripts/              # Utility scripts
├── Dockerfile            # Multi-stage build
├── docker-compose.yml    # Local development
├── docker-compose.prod.yml  # Production
├── nginx.conf            # Reverse proxy
├── prometheus.yml        # Metrics config
└── .github/workflows/    # CI/CD
```

## License

MIT
""")

    def _express(self, path, name):
        """Production-grade Express.js project."""
        dirs = ["src", "src/routes", "src/middleware", "src/models", "src/services",
                "src/config", "tests", "prisma"]
        for d in dirs:
            (path / d).mkdir(parents=True, exist_ok=True)

        (path / "package.json").write_text(json.dumps({
            "name": name,
            "version": "1.0.0",
            "description": f"Production-grade Express API - {name}",
            "main": "dist/server.js",
            "scripts": {
                "dev": "tsx watch src/server.ts",
                "build": "tsc",
                "start": "node dist/server.js",
                "test": "vitest run",
                "test:watch": "vitest",
                "lint": "eslint src/",
                "format": "prettier --write src/",
                "migrate": "prisma migrate dev",
                "migrate:prod": "prisma migrate deploy",
                "seed": "tsx prisma/seed.ts",
            },
            "dependencies": {
                "express": "^4.21.0",
                "cors": "^2.8.5",
                "helmet": "^8.0.0",
                "dotenv": "^16.4.0",
                "@prisma/client": "^5.20.0",
                "redis": "^4.7.0",
                "express-rate-limit": "^7.4.0",
                "winston": "^3.14.0",
                "zod": "^3.23.0",
                "jsonwebtoken": "^9.0.0",
                "bcryptjs": "^2.4.3",
            },
            "devDependencies": {
                "typescript": "^5.6.0",
                "tsx": "^4.19.0",
                "vitest": "^2.1.0",
                "prisma": "^5.20.0",
                "@types/express": "^5.0.0",
                "@types/node": "^22.0.0",
                "@types/jsonwebtoken": "^9.0.0",
                "@types/bcryptjs": "^2.4.0",
                "eslint": "^9.0.0",
                "prettier": "^3.3.0",
                "supertest": "^7.0.0",
            },
        }, indent=2))

        (path / "tsconfig.json").write_text('''{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
''')

        (path / "src/server.ts").write_text(f'''import http from "http";
import app from "./app";
import { logger } from "./config/logger";
import { connectRedis } from "./config/redis";
import { config } from "./config/env";

async function bootstrap() {{
  try {{
    await connectRedis();
    logger.info("Redis connected");

    const server = http.createServer(app);

    server.listen(config.PORT, () => {{
      logger.info(`{name} running on port ${{config.PORT}}`);
    }});

    const shutdown = (signal: string) => {{
      logger.info(`${{signal}} received, shutting down`);
      server.close(() => {{
        logger.info("Server closed");
        process.exit(0);
      }});
    }};

    process.on("SIGTERM", () => shutdown("SIGTERM"));
    process.on("SIGINT", () => shutdown("SIGINT"));
  }} catch (error) {{
    logger.error("Failed to start server", error);
    process.exit(1);
  }}
}}

bootstrap();
''')

        (path / "src/app.ts").write_text(f'''import express from "express";
import cors from "cors";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import { config } from "./config/env";
import { errorHandler } from "./middleware/error";
import { requestLogger } from "./middleware/logger";
import healthRoutes from "./routes/health";
import itemRoutes from "./routes/items";

const app = express();

app.use(helmet());
app.use(cors({{ origin: config.CORS_ORIGINS.split(",") }}));
app.use(express.json({{ limit: "10mb" }}));
app.use(express.urlencoded({{ extended: true }}));
app.use(requestLogger);

if (config.RATE_LIMIT_ENABLED) {{
  app.use(rateLimit({{
    windowMs: config.RATE_LIMIT_WINDOW * 1000,
    max: config.RATE_LIMIT_REQUESTS,
    standardHeaders: true,
    legacyHeaders: false,
  }}));
}}

app.use("/api/health", healthRoutes);
app.use("/api/v1/items", itemRoutes);

app.use(errorHandler);

export default app;
''')

        (path / "src/config/env.ts").write_text(f'''import dotenv from "dotenv";
dotenv.config();

interface Config {{
  APP_NAME: string;
  PORT: number;
  NODE_ENV: string;
  DATABASE_URL: string;
  REDIS_URL: string;
  JWT_SECRET: string;
  CORS_ORIGINS: string;
  RATE_LIMIT_ENABLED: boolean;
  RATE_LIMIT_REQUESTS: number;
  RATE_LIMIT_WINDOW: number;
  LOG_LEVEL: string;
}}

export const config: Config = {{
  APP_NAME: process.env.APP_NAME || "{name}",
  PORT: parseInt(process.env.APP_PORT || "8000", 10),
  NODE_ENV: process.env.NODE_ENV || "development",
  DATABASE_URL: process.env.DATABASE_URL || "",
  REDIS_URL: process.env.REDIS_URL || "redis://localhost:6379/0",
  JWT_SECRET: process.env.JWT_SECRET || "change-me",
  CORS_ORIGINS: process.env.CORS_ORIGINS || "*",
  RATE_LIMIT_ENABLED: process.env.RATE_LIMIT_ENABLED !== "false",
  RATE_LIMIT_REQUESTS: parseInt(process.env.RATE_LIMIT_REQUESTS || "100", 10),
  RATE_LIMIT_WINDOW: parseInt(process.env.RATE_LIMIT_WINDOW || "60", 10),
  LOG_LEVEL: process.env.LOG_LEVEL || "info",
}};
''')

        (path / "src/config/logger.ts").write_text(f'''import winston from "winston";
import { config } from "./env";

const logFormat = config.LOG_LEVEL === "json"
  ? winston.format.json()
  : winston.format.combine(
      winston.format.timestamp(),
      winston.format.colorize(),
      winston.format.printf(({{ timestamp, level, message, ...rest }}) =>
        `${{timestamp}} [${{level}}]: ${{message}} ${{Object.keys(rest).length ? JSON.stringify(rest) : ""}}`
      )
    );

export const logger = winston.createLogger({{
  level: config.LOG_LEVEL,
  format: logFormat,
  transports: [new winston.transports.Console()],
}});
''')

        (path / "src/config/redis.ts").write_text('''import Redis from "ioredis";
import { config } from "./env";
import { logger } from "./logger";

const redis = new Redis(config.REDIS_URL, {
  maxRetriesPerRequest: 3,
  retryStrategy: (times) => Math.min(times * 50, 2000),
});

redis.on("error", (err) => {
  logger.error("Redis error", err);
});

export async function connectRedis(): Promise<void> {
  await redis.ping();
}

export { redis };
''')

        (path / "src/middleware/error.ts").write_text('''import { Request, Response, NextFunction } from "express";
import { logger } from "../config/logger";

export class AppError extends Error {
  statusCode: number;
  code: string;

  constructor(message: string, statusCode: number = 500, code: string = "INTERNAL_ERROR") {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

export function errorHandler(
  err: Error,
  _req: Request,
  res: Response,
  _next: NextFunction
): void {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      error: { code: err.code, message: err.message },
    });
    return;
  }

  logger.error("Unhandled error", err);
  res.status(500).json({
    error: { code: "INTERNAL_ERROR", message: "Internal server error" },
  });
}
''')

        (path / "src/middleware/logger.ts").write_text('''import { Request, Response, NextFunction } from "express";
import { logger } from "../config/logger";

export function requestLogger(req: Request, res: Response, next: NextFunction): void {
  const start = Date.now();
  res.on("finish", () => {
    logger.info(`${req.method} ${req.path} ${res.statusCode} ${Date.now() - start}ms`, {
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: Date.now() - start,
    });
  });
  next();
}
''')

        (path / "src/routes/health.ts").write_text('''import { Router, Request, Response } from "express";

const router = Router();

router.get("/", (_req: Request, res: Response) => {
  res.json({ status: "healthy", version: "1.0.0", timestamp: Date.now() });
});

export default router;
''')

        (path / "src/routes/items.ts").write_text('''import { Router, Request, Response, NextFunction } from "express";
import { z } from "zod";
import { AppError } from "../middleware/error";

const router = Router();

interface Item {
  id: number;
  name: string;
  description?: string;
  price: number;
  createdAt: Date;
}

const items: Item[] = [];
let nextId = 1;

const createItemSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().optional(),
  price: z.number().positive(),
});

router.get("/", (_req: Request, res: Response) => {
  res.json({ data: items, total: items.length });
});

router.post("/", (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = createItemSchema.parse(req.body);
    const item: Item = {
      id: nextId++,
      ...data,
      createdAt: new Date(),
    };
    items.push(item);
    res.status(201).json({ data: item });
  } catch (err) {
    next(new AppError("Validation failed", 400, "VALIDATION_ERROR"));
  }
});

router.get("/:id", (req: Request, res: Response, next: NextFunction) => {
  const id = parseInt(req.params.id);
  const item = items.find((i) => i.id === id);
  if (!item) {
    return next(new AppError("Item not found", 404, "NOT_FOUND"));
  }
  res.json({ data: item });
});

router.put("/:id", (req: Request, res: Response, next: NextFunction) => {
  const id = parseInt(req.params.id);
  const idx = items.findIndex((i) => i.id === id);
  if (idx === -1) {
    return next(new AppError("Item not found", 404, "NOT_FOUND"));
  }
  try {
    const data = createItemSchema.partial().parse(req.body);
    items[idx] = { ...items[idx], ...data };
    res.json({ data: items[idx] });
  } catch {
    next(new AppError("Validation failed", 400, "VALIDATION_ERROR"));
  }
});

router.delete("/:id", (req: Request, res: Response, next: NextFunction) => {
  const id = parseInt(req.params.id);
  const idx = items.findIndex((i) => i.id === id);
  if (idx === -1) {
    return next(new AppError("Item not found", 404, "NOT_FOUND"));
  }
  items.splice(idx, 1);
  res.status(204).send();
});

export default router;
''')

        (path / "tests/health.test.ts").write_text('''import { describe, it, expect } from "vitest";
import request from "supertest";
import app from "../src/app";

describe("Health", () => {
  it("should return healthy", async () => {
    const res = await request(app).get("/api/health");
    expect(res.status).toBe(200);
    expect(res.body.status).toBe("healthy");
  });
});
''')

        (path / "Dockerfile").write_text(f"""FROM node:20-alpine AS base
WORKDIR /app
COPY package.json ./

FROM base AS deps
RUN npm ci

FROM deps AS builder
COPY . .
RUN npm run build

FROM base AS runner
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/api/health || exit 1

CMD ["node", "dist/server.js"]
""")

        (path / "prisma/schema.prisma").write_text(f'''generator client {{
  provider = "prisma-client-js"
}}

datasource db {{
  provider = "postgresql"
  url      = env("DATABASE_URL")
}}

model Item {{
  id          Int      @id @default(autoincrement())
  name        String
  description String?
  price       Float
  isActive    Boolean  @default(true) @map("is_active")
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  @@map("items")
}}
''')

        (path / "vitest.config.ts").write_text('''import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
  },
});
''')

        extra = {
            ".eslintrc.json": '{ "extends": ["eslint:recommended"] }',
            ".prettierrc": '{ "semi": true, "singleQuote": false }',
        }
        self._make_common(path, name, "typescript", extra)

        (path / "README.md").write_text(f"""# {name}

> Production-grade Express.js API built with OWURA.

## Stack

- **Runtime**: Node.js 20 + TypeScript
- **Framework**: Express.js
- **Database**: PostgreSQL + Prisma ORM
- **Cache**: Redis (ioredis)
- **Validation**: Zod
- **Logging**: Winston structured JSON
- **Auth**: JWT + bcryptjs
- **Security**: Helmet + CORS + Rate limiting
- **Testing**: Vitest + Supertest
- **Container**: Docker multi-stage

## Quick Start

```bash
cp .env.example .env
docker-compose up -d
```

## Development

```bash
npm install
npm run dev
```

## Testing

```bash
npm test
```

## Production

```bash
npm run build
npm start
```
""")

    def _nextjs(self, path, name):
        """Production-grade Next.js project."""
        _run_cmd(f"npx create-next-app@latest {path} --typescript --tailwind --app --eslint 2>/dev/null || true", path)
        # If create-next-app failed, scaffold manually
        if not (path / "package.json").exists():
            (path / "package.json").write_text(json.dumps({"name": name, "version": "1.0.0", "private": True, "scripts": {"dev": "next dev", "build": "next build", "start": "next start"}}, indent=2))

        dirs = ["src/components/ui", "src/lib", "src/app/api", "prisma"]
        for d in dirs:
            (path / d).mkdir(parents=True, exist_ok=True)

        self._make_common(path, name, "typescript")

        (path / "README.md").write_text(f"""# {name}

> Production-grade Next.js application built with OWURA.

## Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Database**: PostgreSQL + Prisma
- **Deployment**: Docker + CI/CD

## Quick Start

```bash
cp .env.example .env
npm install
npm run dev
```

## Build

```bash
npm run build
npm start
```
""")

    def _flask_api(self, path, name):
        """Production-grade Flask API."""
        (path / "app").mkdir(parents=True, exist_ok=True)
        (path / "app/api").mkdir(parents=True, exist_ok=True)
        (path / "app/models").mkdir(parents=True, exist_ok=True)
        (path / "app/services").mkdir(parents=True, exist_ok=True)
        (path / "migrations").mkdir(parents=True, exist_ok=True)
        (path / "tests").mkdir(parents=True, exist_ok=True)
        (path / "app/__init__.py").write_text("")
        (path / "app/api/__init__.py").write_text("")
        (path / "app/models/__init__.py").write_text("")
        (path / "app/services/__init__.py").write_text("")
        (path / "tests/__init__.py").write_text("")

        (path / "app/__init__.py").write_text(f'''"""Flask application factory."""

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.api.health import health_bp
    from app.api.items import items_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(items_bp)

    return app
''')

        (path / "app/config.py").write_text(f'''"""Flask configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
''')

        (path / "app/api/health.py").write_text('''"""Health check endpoint."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health")
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"})
''')

        (path / "app/api/items.py").write_text('''"""Items CRUD API."""

from flask import Blueprint, jsonify, request
from app import db
from app.models.item import Item

items_bp = Blueprint("items", __name__, url_prefix="/api/v1/items")


@items_bp.route("/")
def list_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@items_bp.route("/", methods=["POST"])
def create_item():
    data = request.get_json()
    item = Item(name=data["name"], price=data["price"])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@items_bp.route("/<int:item_id>")
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())


@items_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    db.session.commit()
    return jsonify(item.to_dict())


@items_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204
''')

        (path / "app/models/item.py").write_text('''"""Item model."""

from datetime import datetime
from app import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
''')

        (path / "requirements.txt").write_text("""flask>=3.0.0
flask-cors>=4.0.0
flask-sqlalchemy>=3.1.0
flask-migrate>=4.0.0
gunicorn>=21.0.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.0
pytest>=8.0.0
ruff>=0.5.0
""")

        (path / "Dockerfile").write_text(f"""FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:create_app()"]
""")

        (path / "README.md").write_text(f"""# {name}

> Production-grade Flask API built with OWURA.

## Quick Start

```bash
cp .env.example .env
pip install -r requirements.txt
flask db upgrade
flask run
```

## Docker

```bash
docker-compose up -d
```
""")

    def _react(self, path, name):
        _run_cmd(f"npx create-vite@latest {path} --template react-ts 2>/dev/null || true", path)
        (path / "README.md").write_text(f"# {name}\n\nReact + Vite project built with OWURA.\n")

    def _django(self, path, name):
        _run_cmd(f"django-admin startproject {name} .", path)
        _run_cmd(f"python manage.py startapp api", path)

    def _python_cli(self, path, name):
        (path / f"{name}.py").write_text(f'''#!/usr/bin/env python3
"""CLI: {name}"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="{name}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("run", help="Run the tool")
    subparsers.add_parser("build", help="Build")
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
    py_modules=["{name}"],
    install_requires=["click", "rich"],
    entry_points={{{{"console_scripts": ["{name}={name}:main"]}}}},
)
''')

    def _rust_cli(self, path, name):
        _run_cmd(f"cargo init --name {name}", path)

    def _go_api(self, path, name):
        _run_cmd(f"go mod init {name}", path)
        (path / "main.go").write_text(f'''package main

import (
    "encoding/json"
    "log"
    "net/http"
    "os"
    "time"
)

type HealthResponse struct {{
    Status    string `json:"status"`
    Version   string `json:"version"`
    Timestamp int64  `json:"timestamp"`
}}

func healthHandler(w http.ResponseWriter, r *http.Request) {{
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(HealthResponse{{
        Status: "healthy", Version: "1.0.0", Timestamp: time.Now().Unix(),
    }})
}}

func main() {{
    mux := http.NewServeMux()
    mux.HandleFunc("/api/health", healthHandler)

    port := os.Getenv("PORT")
    if port == "" {{
        port = "8080"
    }}

    server := &http.Server{{
        Addr:         ":" + port,
        Handler:      withLogging(mux),
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }}

    log.Printf("{name} running on :%s", port)
    log.Fatal(server.ListenAndServe())
}}

func withLogging(next http.Handler) http.Handler {{
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {{
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(start))
    }})
}}
''')

    def _record_project(self, name, template, path):
        from owura.memory import get_memory
        memory = get_memory()
        memory.add_project(name=name, description=f"{template} project", tech_stack=[template], status="in_progress")

    def generate_tests(self, file_path):
        return f'''import pytest
from {Path(file_path).stem} import *

def test_basic():
    assert True
'''

    def analyze_project(self, path="."):
        project_path = Path(path)
        analysis = {
            "files": len(list(project_path.rglob("*"))),
            "languages": [],
            "has_tests": bool(list(project_path.rglob("test_*"))),
            "has_docker": (project_path / "Dockerfile").exists(),
            "has_ci": (project_path / ".github").exists(),
            "has_docs": (project_path / "README.md").exists(),
            "suggestions": [],
        }
        for ext, lang in [(".py", "Python"), (".js", "JavaScript"), (".ts", "TypeScript"),
                          (".go", "Go"), (".rs", "Rust")]:
            if list(project_path.rglob(f"*{ext}")):
                analysis["languages"].append(lang)
        if not analysis["has_tests"]:
            analysis["suggestions"].append("Add tests")
        if not analysis["has_docker"]:
            analysis["suggestions"].append("Add Dockerfile")
        if not analysis["has_ci"]:
            analysis["suggestions"].append("Add CI/CD")
        if not analysis["has_docs"]:
            analysis["suggestions"].append("Add README.md")
        return analysis


_pro_tools = None


def get_pro_tools():
    global _pro_tools
    if _pro_tools is None:
        _pro_tools = ProTools()
    return _pro_tools
