# Technical Requirements Document — TerraSeek

> Version: 1.0
> Last updated: 2026-09-28
> Related: [PRD.md](./PRD.md), [ARCHITECTURE.md](./ARCHITECTURE.md), [DATA_MODEL.md](./DATA_MODEL.md), [API_CONTRACT.md](./API_CONTRACT.md)

---

## 1. System Objectives

Build a production-quality prototype that:

1. Accepts natural-language queries and retrieves semantically relevant satellite imagery
2. Performs multi-temporal change analysis on real satellite data
3. Explains detected changes with evidence and provenance
4. Operates fully offline after initial data staging
5. Uses real remote-sensing models, not keyword matching or random embeddings

---

## 2. Technical Constraints

| Constraint | Detail |
|---|---|
| Offline operation | No runtime internet access for final demo |
| Single-machine deployment | Must run on a single workstation or laptop |
| Real satellite data | Demo must use real satellite imagery, not synthetic |
| Explainable algorithms | Change detection must be interpretable |
| Local model inference | All ML runs locally — no cloud API calls |
| PostgreSQL required | PostGIS is needed for spatial queries |
| No unnecessary services | No Kubernetes, Kafka, Redis, or hosted vector DBs |

---

## 3. Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture.

**Summary:**

```
Frontend (React + TypeScript)
    ↓ REST/JSON
Backend (FastAPI + Python)
    ↓
Application Services
    ├── Search Service (query → embedding → FAISS → rank → filter)
    ├── Change Detection Service (align → diff → filter → evidence)
    ├── Ingestion Service (validate → preprocess → embed → index)
    └── Evidence/Provenance Service
    ↓
Data Layer
    ├── PostgreSQL + PostGIS (metadata, spatial, provenance)
    ├── Local Filesystem (GeoTIFF/COG rasters)
    ├── FAISS Index (vector similarity)
    └── Model Cache (RemoteCLIP weights)
```

---

## 4. Component Boundaries

| Component | Responsibility | Does NOT |
|---|---|---|
| **Frontend** | UI rendering, map display, user interaction | Run ML models, access filesystem |
| **API Layer** | Request validation, routing, response formatting | Business logic, direct DB queries |
| **Search Service** | Query embedding, FAISS search, result ranking | Change detection, ingestion |
| **Change Service** | Image alignment, differencing, morphological filtering | Search, ingestion |
| **Ingestion Service** | Validation, preprocessing, embedding, indexing | Search, change detection |
| **Evidence Service** | Evidence compilation, provenance tracking | Algorithm execution |
| **Database** | Metadata, spatial queries, provenance storage | Raster storage, vector search |
| **FAISS** | Approximate nearest neighbor search | Metadata filtering, spatial queries |
| **Raster Store** | GeoTIFF/COG file storage and retrieval | Metadata management |

---

## 5. Technology Choices

### 5.1 Backend: Python + FastAPI

**Why:** Python is the standard language for geospatial processing (rasterio, GDAL, shapely, numpy) and ML (PyTorch, transformers). FastAPI provides async capability, automatic OpenAPI docs, and Pydantic validation. No viable alternative provides the same ecosystem coverage.

### 5.2 Frontend: React + TypeScript + Vite

**Why:** React is the most widely supported frontend framework with the largest component ecosystem. TypeScript provides type safety. Vite provides fast builds. Tailwind CSS provides utility-first styling that matches the "clean, professional" design goal.

### 5.3 Map Library: Leaflet

**Why:** Leaflet is lightweight (~42KB), works offline with local tile sources, has excellent documentation, and supports GeoJSON overlays, markers, and custom layers. MapLibre GL is an alternative but adds WebGL complexity that isn't needed for this prototype.

### 5.4 Database: PostgreSQL + PostGIS

**Why:** PostGIS provides native spatial indexing, geometry types, spatial joins, and distance calculations. No alternative provides equivalent spatial query capability. PostgreSQL is the industry standard for geospatial applications.

### 5.5 Vector Search: FAISS

**Why:** FAISS (Facebook AI Similarity Search) runs entirely in-process as a Python library. No external server needed. Supports exact and approximate nearest neighbor search. Serializes to a single file. Ideal for offline operation on a single machine. Qdrant (used in V1) requires a separate server process and adds unnecessary complexity.

### 5.6 Embedding Model: RemoteCLIP

**Why:** RemoteCLIP is a vision-language model specifically trained on remote sensing imagery. It produces embeddings that capture semantics relevant to satellite imagery (land use, vegetation, water, structures) rather than generic CLIP embeddings trained on internet photos. Alternative: SatCLIP or GeoRSCLIP. The model must be validated on remote sensing benchmarks before selection.

### 5.7 Raster Processing: Rasterio + GDAL + NumPy

**Why:** Rasterio is the standard Python wrapper for GDAL. It supports windowed reading (essential for large rasters), CRS reprojection, and COG access. NumPy provides efficient array operations for spectral indices and change detection. No alternative exists.

### 5.8 Image Processing: OpenCV

**Why:** OpenCV provides morphological operations (erosion, dilation, opening, closing), connected component analysis, contour detection, and image alignment (feature matching, homography) needed for change detection post-processing. scikit-image is an alternative but OpenCV is faster for the operations needed.

---

## 6. Backend Requirements

### 6.1 API Framework

- FastAPI with Pydantic v2 request/response models
- All routes under `/api/` prefix
- Structured JSON error responses with error codes
- Request ID tracking via middleware
- CORS configured for frontend origin

### 6.2 Application Services

Each service is a Python module with clear interfaces:

```python
# Search
class SearchService:
    def search(query: str, filters: SearchFilters) -> SearchResponse

# Change Detection
class ChangeDetectionService:
    def detect_changes(scene_a_id: str, scene_b_id: str) -> ChangeResult

# Ingestion
class IngestionService:
    def ingest(file_path: Path, metadata: AssetMetadata) -> IngestionResult

# Evidence
class EvidenceService:
    def compile_evidence(change_result_id: str) -> Evidence
```

### 6.3 Error Handling

- All exceptions caught at API layer
- Structured error responses: `{error: {code, message, request_id}}`
- No stack traces in production responses
- Domain exceptions for specific failure modes (AssetNotFound, InvalidRaster, ModelNotLoaded)

---

## 7. Frontend Requirements

### 7.1 Core Pages

| Page | Purpose |
|---|---|
| Search | Primary entry point — search bar + results + map |
| Scene Detail | Scene metadata, thumbnail, temporal options |
| Temporal Analysis | Before/after comparison + change detection results |
| Evidence | Evidence panel with provenance details |

### 7.2 Components

- Search bar with query input
- Result list with scene cards (thumbnail, date, sensor, relevance)
- Map with scene footprint overlays
- Before/after image viewer (side-by-side or slider)
- Change mask overlay on map
- Evidence panel (before, after, mask, confidence, provenance)
- Loading states, empty states, error states

### 7.3 Constraints

- No decorative AI visualizations
- No dashboard with meaningless metrics
- Search visible without scrolling
- Map does not dominate screen unless showing results
- Mobile-responsive but desktop-first
- Offline-capable (no external font/icon CDNs in production)

---

## 8. Database Requirements

See [DATA_MODEL.md](./DATA_MODEL.md) for full schema.

### 8.1 Core Entities

- Scene: source satellite scene metadata
- Tile: individual tiles from tiled scenes
- Embedding: vector embedding with model metadata
- TemporalPair: two scenes linked for comparison
- ChangeDetectionResult: change analysis output
- ChangeRegion: individual detected change polygon
- Evidence: compiled evidence for a result
- ProvenanceRecord: processing history

### 8.2 Spatial Requirements

- Scene footprints stored as PostGIS `geometry(Polygon, 4326)`
- Change regions stored as PostGIS `geometry(MultiPolygon, 4326)`
- Spatial indexes on all geometry columns
- Spatial queries for intersection, containment, distance

### 8.3 Indexing

- B-tree indexes on: scene_id, acquisition_date, sensor, created_at
- GiST spatial indexes on all geometry columns
- Composite indexes for common query patterns

---

## 9. Geospatial Requirements

### 9.1 Coordinate Reference Systems

- All geographic coordinates in EPSG:4326 (WGS 84)
- Raster processing in UTM or scene-native CRS
- Area calculations in appropriate metric CRS
- CRS validation during ingestion

### 9.2 Raster Handling

- Support GeoTIFF and Cloud Optimized GeoTIFF (COG)
- Windowed reading for large rasters (no full-file loading)
- Efficient thumbnail generation (resampled read)
- Band-specific operations (RGB composite, spectral indices)

### 9.3 Spatial Operations

- Bounding box intersection for search filtering
- Distance calculations for proximity queries
- Area calculations for change regions
- Geometry simplification for API responses

---

## 10. ML Requirements

See [AI_SYSTEM.md](./AI_SYSTEM.md) for detailed ML documentation.

### 10.1 Semantic Embedding

- Generate 512-dimensional (or model-native) embeddings from text queries
- Generate embeddings from satellite image tiles
- Embeddings must capture remote-sensing semantics (land use, vegetation, water, structures)
- Model weights must be downloadable and cacheable locally
- Inference on CPU (GPU optional)

### 10.2 Change Detection

- For MVP: algorithmic approach (image differencing + spectral indices + morphological filtering)
- Inputs: two co-registered rasters at same location
- Outputs: binary change mask, change polygons, confidence scores
- Must handle: different acquisition dates, slight misalignment, different illumination

### 10.3 Model Management

- Clear separation between model interface and implementation
- Model metadata (name, version, tier) attached to every result
- Explicit failure if weights are not available — no silent fallback to random embeddings
- Demo mode clearly labeled in all outputs

---

## 11. Retrieval Requirements

See [INFORMATION_RETRIEVAL.md](./INFORMATION_RETRIEVAL.md).

- Text query → embedding → FAISS top-K → metadata filter → spatial filter → ranked results
- Similarity metric: cosine similarity
- Default K: 20 (configurable)
- Result metadata: scene_id, acquisition_date, location, relevance_score
- Pagination support for large result sets

---

## 12. Raster Processing Requirements

- Read GeoTIFF/COG files using rasterio
- Extract metadata: CRS, bounds, resolution, band count, nodata value
- Generate RGB thumbnails (512px max dimension)
- Compute spectral indices: NDVI, MNDWI
- Validate raster quality: dimensions, bands, nodata percentage, cloud cover estimate
- Windowed reading for memory efficiency

---

## 13. Change Detection Requirements

See [CHANGE_DETECTION.md](./CHANGE_DETECTION.md).

### Pipeline:

1. Load scene A and scene B rasters
2. Verify spatial overlap
3. Reproject to common CRS if needed
4. Align/co-register images
5. Normalize radiometry
6. Compute difference (pixel-level or spectral index)
7. Apply threshold to generate binary change mask
8. Apply morphological filtering (opening to remove noise, closing to fill holes)
9. Apply false-positive suppression (cloud mask, area threshold)
10. Extract connected components as change regions
11. Compute region properties (area, centroid, bounding box)
12. Generate evidence (before/after crops, change mask, metadata)

### Acceptance:

- Detects building-scale structural changes (>100m²)
- Detects vegetation loss (NDVI drop > 0.2)
- Suppresses clouds as false positives
- Produces change polygons with area and confidence
- Processing time < 30 seconds per pair

---

## 14. Evidence Requirements

See [EVIDENCE_MODEL.md](./EVIDENCE_MODEL.md).

Every detected change must include:

- Before image (cropped to change region)
- After image (cropped to change region)
- Change mask
- Location (coordinates, bounding box)
- Acquisition dates (before, after)
- Affected area (m²)
- Change type (structural, vegetation, water)
- Confidence score
- Quality indicators (cloud cover, nodata)
- Algorithm used
- Processing version
- Source scene identifiers

---

## 15. Provenance Requirements

See [PROVENANCE.md](./PROVENANCE.md).

Track for every result:

- Source dataset
- Source scene identifier
- Acquisition timestamp
- Processing pipeline version
- Preprocessing steps applied
- Model name and version
- Embedding model version
- Algorithm version and parameters
- Timestamp of processing
- Analyst actions (if any)

---

## 16. Security

See [SECURITY.md](./SECURITY.md).

- Input validation on all API endpoints
- File validation on all uploads (type, size, header checks)
- Path traversal prevention for file access
- No sensitive data in API error responses
- Database credentials via environment variables
- No hardcoded secrets in source code

---

## 17. Testing

See [TESTING.md](./TESTING.md).

| Level | Tools | Coverage Target |
|---|---|---|
| Unit | pytest | Core algorithms, schemas, services |
| Integration | pytest + TestClient | API routes, database operations |
| Geospatial | pytest + rasterio | Raster processing, spatial operations |
| ML | pytest | Embedding generation, similarity search |
| E2E | Playwright | Critical user workflows |
| Performance | pytest-benchmark | Search latency, ingestion throughput |

---

## 18. Performance Targets

| Operation | Target | Measurement |
|---|---|---|
| Search query | < 3 seconds | Time from submit to results displayed |
| Scene detail load | < 1 second | Time from click to detail rendered |
| Change detection | < 30 seconds | Time per scene pair |
| Ingestion | < 60 seconds | Time per scene (validation + embedding + index) |
| FAISS search | < 100ms | Time for top-K vector search |
| Thumbnail generation | < 5 seconds | Time per scene |

---

## 19. Offline Operation

- All satellite data staged as local files
- All model weights downloaded to local cache
- FAISS index stored on local filesystem
- PostgreSQL running locally
- Frontend served from local Nginx or dev server
- No CDN dependencies for fonts, icons, or map tiles
- Leaflet map uses locally served tiles or vector overlays

---

## 20. Deployment

- Docker Compose for all services (PostgreSQL, API, Frontend)
- Single `docker compose up` to start everything
- Environment configuration via `.env` file
- Data volumes mounted from local filesystem
- No cloud provider dependencies

---

## 21. Observability

- Structured JSON logging (timestamp, level, module, message)
- Request ID tracking through API middleware
- Processing time headers on all API responses
- Health check endpoint
- Ingestion status reporting
- Index statistics endpoint

---

## 22. Failure Handling

| Failure | Expected Behavior |
|---|---|
| Model weights missing | Explicit error with instructions to download |
| Corrupted raster | Reject during ingestion with quality report |
| FAISS index missing | Return empty results with warning |
| Database unavailable | API returns 503 with clear error |
| Insufficient disk space | Ingestion fails with disk space error |
| Invalid CRS | Reject during ingestion with CRS error |

---

## 23. Data Lifecycle

```
Raw Dataset → Staging → Validation → Preprocessing → Embedding → Indexing → Searchable
                                                                              ↓
                                                               Temporal Pair Selection
                                                                              ↓
                                                               Change Detection
                                                                              ↓
                                                               Evidence + Provenance
```

---

## 24. Acceptance Criteria

### System-level acceptance:

1. A natural-language query returns relevant satellite scenes within 3 seconds
2. Relevance ranking is based on real semantic similarity, not hardcoded scores
3. Change detection identifies real changes in real satellite imagery
4. Evidence panel shows before/after images, change mask, and provenance
5. The entire system runs offline after data staging
6. No external API calls during demo operation
7. Processing is reproducible (same input → same output)
