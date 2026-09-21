# Local Development Guide

## Prerequisites
- Python 3.11+
- Node.js 18+ and pnpm / npm
- uv package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Useful Development Commands

```bash
# Install all dependencies
make install

# Run database migrations
make migrate

# Seed deterministic demo sites
make seed

# Run test suite
make test

# Start both API and Web concurrently
make dev

# Type check
make typecheck

# Code formatting & linting
make lint
make format
```
