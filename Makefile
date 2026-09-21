.PHONY: install dev test lint format typecheck migrate seed api web worker docker-up docker-down evaluate clean

UV ?= ~/.local/bin/uv
PYTHON ?= .venv/bin/python

install:
	$(UV) sync --extra dev
	cd apps/web && npm install

dev:
	@echo "Starting TerraSeek API and Web in development mode..."
	make -j 2 api web

test:
	$(PYTHON) -m pytest tests/unit tests/integration tests/fault tests/e2e -v

lint:
	$(PYTHON) -m ruff check src apps tests

format:
	$(PYTHON) -m ruff format src apps tests

typecheck:
	$(PYTHON) -m mypy src/terraseek

migrate:
	$(PYTHON) -m terraseek.cli db migrate

seed:
	$(PYTHON) scripts/seed_demo.py

api:
	$(PYTHON) -m uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload

web:
	cd apps/web && npm run dev

worker:
	$(PYTHON) -m terraseek.workers.runner

docker-up:
	docker compose up -d

docker-down:
	docker compose down

evaluate:
	$(PYTHON) -m terraseek.cli evaluate

clean:
	rm -rf .venv .pytest_cache .ruff_cache apps/web/dist apps/web/node_modules
	find . -type d -name "__pycache__" -exec rm -rf {} +
