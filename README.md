# TerraSeek

> **See Change. Find Answers.**

TerraSeek is a full-stack satellite-imagery search and change-analysis platform. Built around an evidence-first analytical protocol, TerraSeek allows analysts and public service teams to search remote sensing data using natural language, verify multi-temporal observations, detect physical changes, and establish ground truth with zero fabricated AI confidence scores.

```
SEARCH → FIND → VERIFY → UNDERSTAND
```

---

## 1. Problem & Solution

### The Problem
Traditional satellite imagery workflows force analysts to manually search catalogs by bounding box coordinates, cross-reference multiple sensor passes, and manually inspect pixel diffs. Conversely, modern generative AI tools often hallucinate or output arbitrary percentage scores (e.g. "98.7% confidence") without verifiable topological or temporal proof.

### The Solution
TerraSeek combines:
1. **Natural Language Mission Compilation**: Parsing user queries into verifiable spatial, temporal, and semantic constraints.
2. **Deterministic Topological & Temporal Verification**: Explicitly measuring distances to geographic landmarks (rivers, roads) and checking baseline observation continuity.
3. **Multi-Domain Change Detection**: Structural building analysis, linear infrastructure detection, NDVI vegetation loss, and MNDWI water dynamics.
4. **Evidence Passports**: Generating auditable, itemized proof distinguishing **SUPPORTED**, **NEEDS_REVIEW**, **INSUFFICIENT_EVIDENCE**, and **NO_MATCH**.

---

## 2. Core Truth Statuses

| Status | Determination Rule |
|---|---|
| **SUPPORTED** | Target candidate exists, mandatory spatial proximity constraints are mathematically satisfied, temporal baseline continuity is proven, and change features are confirmed. |
| **NEEDS_REVIEW** | Evidence exists but criteria is borderline (e.g. contrast near threshold, extended gap between passes). Automatically escalated to human review. |
| **INSUFFICIENT_EVIDENCE** | Baseline historical imagery is missing or observation is corrupted. Missing evidence is **never** converted into a false negative conclusion. |
| **NO_MATCH** | Target entity is absent from the catalog, or strict spatial boundaries are violated. No fabricated candidates are created. |

---

## 3. Technology Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic 2, SQLAlchemy 2, Alembic, Typer, Rich.
- **Geospatial & Rasters**: Rasterio, NumPy, Shapely, PyProj, GeoAlchemy2.
- **Databases**: PostgreSQL 16 + PostGIS (with automatic SQLite fallback for lightweight development), Qdrant Vector Database (with in-memory fallback).
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, MapLibre GL JS, Lucide React.
- **Packaging & Tooling**: `uv` (dependency resolution and lockfile), `pnpm`, Docker, Docker Compose.

---

## 4. Repository Structure

```
terraseek/
├── apps/
│   ├── api/                     # FastAPI backend application
│   │   ├── main.py              # Application entrypoint & middleware
│   │   ├── dependencies.py      # Route dependencies
│   │   └── routes/              # Modular API routes (search, sites, change, etc.)
│   └── web/                     # React + Vite + TypeScript frontend
│       ├── src/
│       │   ├── api/             # Centralized typed API client
│       │   ├── components/      # Reusable UI (MapView, Timeline, BeforeAfterViewer, etc.)
│       │   ├── pages/           # 11 routes (Home, Search, Similar, Compare, Change, etc.)
│       │   └── types/           # Strongly typed TypeScript contracts
├── src/
│   └── terraseek/               # Core intelligence package
│       ├── cli.py               # Typer CLI commands
│       ├── config.py            # Pydantic settings & YAML config loader
│       ├── schemas/             # Pydantic v2 domain schemas
│       ├── db/                  # SQLAlchemy models & clean repositories
│       ├── catalog/             # Imagery inventory & catalog search
│       ├── ingestion/           # Ingestion pipeline & tiling
│       ├── raster/              # Rasterio windows, reprojection, NDVI/MNDWI
│       ├── quality/             # Cloud cover, nodata, dimension verification
│       ├── models/              # GeoRSCLIP, UNet-ResNet34, and Demo adapters
│       ├── retrieval/           # Qdrant client & vector indexing
│       ├── spatial/             # Shapely & pyproj geodesic distance checks
│       ├── temporal/            # Continuity & earliest supported observation
│       ├── change/              # Change extraction & difference pipeline
│       ├── discovery/           # Mission compiler & natural language parser
│       ├── workflow/            # End-to-end mission orchestrator
│       ├── evidence/            # Evidence Passport & policy engine
│       ├── review/              # Human analyst escalation queue & decisions
│       ├── workers/             # Persistent background job runner
│       └── evaluation/          # Precision@K, Recall@K, IoU benchmarks
├── configs/                     # development.yaml, testing.yaml, production.yaml
├── manifests/                   # Benchmark dataset manifests
├── tests/                       # Unit, integration, fault, and e2e test suites
├── scripts/                     # seed_demo.py, generate_assets.py
├── infra/                       # Dockerfiles and docker-compose.yml
├── docs/                        # Complete technical specifications (11 docs)
├── pyproject.toml               # Python package configuration
├── uv.lock                      # Resolved dependency lockfile
├── Makefile                     # Standard developer commands
└── .env.example                 # Environment configuration template
```

---

## 5. Quickstart & Local Development

### Option A: Local Python + Node Setup

```bash
# 1. Install dependencies
uv sync --extra dev
cd apps/web && pnpm install && cd ../..

# 2. Generate demo assets & seed database
.venv/bin/python scripts/generate_assets.py
.venv/bin/python scripts/seed_demo.py

# 3. Start FastAPI backend (Port 8000)
.venv/bin/python -m uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload

# 4. Start React frontend (Port 5173, in separate terminal)
cd apps/web && pnpm run dev
```

### Option B: Docker Compose Setup

```bash
# Copy configuration
cp .env.example .env

# Start PostGIS, Qdrant, API, Worker, and Web UI
docker compose up -d

# Verify services
docker compose ps
```

---

## 6. CLI Reference

TerraSeek includes a complete Typer CLI:

```bash
# Check system and provider health
python -m terraseek.cli health

# Run natural language search
python -m terraseek.cli search "new buildings near a river"

# Test negative match (Truth-in-AI validation)
python -m terraseek.cli search "new airport"

# Test missing baseline imagery handling
python -m terraseek.cli search "new construction where earlier imagery is unavailable"

# Delineate changes for a site
python -m terraseek.cli analyze-change site-01

# Verify temporal observation continuity
python -m terraseek.cli verify-temporal site-01

# Run benchmark evaluation
python -m terraseek.cli evaluate

# Generate JSON evidence report
python -m terraseek.cli report site-01
```

---

## 7. Testing Suite

The repository includes a 100% passing test suite across unit, integration, fault tolerance, and end-to-end workflows:

```bash
python -m pytest tests/unit tests/integration tests/fault tests/e2e -v
```

---

## 8. Implemented vs. Planned Production Components

### Implemented
- [x] Full-stack architecture with FastAPI backend and React/Vite/Tailwind frontend.
- [x] MapLibre GL JS with offline-first local canvas and GeoJSON layers.
- [x] Natural language discovery parser & inspectable mission compiler.
- [x] PostgreSQL + PostGIS database with clean repositories (and SQLite fallback).
- [x] Qdrant vector retrieval with in-memory fallback.
- [x] Synthetic 5-site deterministic demo dataset with multi-temporal GeoTIFF rasters.
- [x] Multi-domain change detection (Structural, NDVI, MNDWI).
- [x] Temporal continuity checks & earliest supported observation detection.
- [x] Evidence Passport generation and four-tier truth determination.
- [x] Human analyst review queue with persistent decisions.
- [x] Background job worker abstraction with persistent state.
- [x] Auditable JSON evidence report generation and print-ready view.
- [x] Complete Typer CLI and evaluation benchmark framework.

### Planned Production Components
- [ ] Connect production GeoRSCLIP neural model weights (swapped via `EMBEDDING_PROVIDER=georsclip`).
- [ ] Connect production Siamese U-Net ResNet-34 change weights (swapped via `CHANGE_DETECTION_PROVIDER=unet_resnet34`).
- [ ] Direct live STAC API ingestion from Sentinel-2 COG archives.
- [ ] Distributed Celery/Redis queue for high-throughput batch tiling.

---

## 9. License

Apache 2.0 License. Built for mission-critical remote sensing and truth-in-AI verification.
