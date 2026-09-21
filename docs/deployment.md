# Deployment Guide

TerraSeek supports two deployment architectures: Full Docker Compose and Hybrid Local Development.

## Option A: Full Docker Compose Deployment (Recommended)

Starts PostgreSQL 16 + PostGIS, Qdrant, FastAPI backend, background worker, and React Nginx frontend:

```bash
# 1. Clone & enter repository
cd terraseek

# 2. Copy environment file
cp .env.example .env

# 3. Start all services in background
docker compose up -d

# 4. Check service status
docker compose ps

# 5. Access services:
# Web UI:    http://localhost:5173
# API Docs:  http://localhost:8000/docs
# Qdrant UI: http://localhost:6333/dashboard
```

## Option B: Hybrid Local Development

Run Python and Node directly on host:

```bash
# 1. Install Python dependencies
uv sync --extra dev

# 2. Install Node dependencies
cd apps/web && pnpm install

# 3. Seed demo dataset
.venv/bin/python scripts/seed_demo.py

# 4. Start API server
.venv/bin/python -m uvicorn apps.api.main:app --port 8000 --reload

# 5. Start Web client (in separate terminal)
cd apps/web && pnpm run dev
```
