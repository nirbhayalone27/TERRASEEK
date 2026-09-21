# TerraSeek Data Model & Database Architecture

TerraSeek employs PostgreSQL 16 with PostGIS spatial extensions (with SQLite fallback for lightweight development).

## Entities and Schema

### 1. `sites`
Represents an area of interest.
- `id` (UUID string, Primary Key)
- `name` (VARCHAR, Indexed)
- `location_name` (VARCHAR)
- `latitude`, `longitude` (FLOAT)
- `boundary` (JSON GeoJSON Polygon)
- `description` (TEXT)
- `tags` (JSON array)
- `meta_info` (JSON)
- `created_at` (TIMESTAMP)

### 2. `observations`
Specific satellite sensor passes over a site.
- `id` (UUID, PK)
- `site_id` (FK `sites.id`, Indexed)
- `acquisition_date` (DATE, Indexed)
- `sensor` (VARCHAR e.g. Sentinel-2A)
- `resolution_meters` (FLOAT e.g. 10.0)
- `cloud_cover` (FLOAT)
- `usable` (BOOLEAN)
- `asset_path` (VARCHAR)
- `thumbnail_url` (VARCHAR)
- `bands` (JSON array: B02, B03, B04, B08)

### 3. `spatial_features`
Physical landmarks used for topological proximity verification.
- `id` (UUID, PK)
- `site_id` (FK `sites.id`, Indexed)
- `feature_type` (VARCHAR e.g. river, road, lake)
- `name` (VARCHAR e.g. Danube River Channel)
- `geometry` (JSON GeoJSON LineString/Polygon)

### 4. `change_events`
Delineated surface changes between observation dates.
- `id` (UUID, PK)
- `site_id` (FK `sites.id`, Indexed)
- `change_type` (VARCHAR: BUILDING, ROAD, VEGETATION, WATER)
- `earlier_date`, `later_date` (DATE)
- `area_sq_meters` (FLOAT)
- `status` (VARCHAR: SUPPORTED, NEEDS_REVIEW)
- `model_name`, `model_tier` (VARCHAR)
- `geometry` (JSON GeoJSON Polygon)

### 5. `evidence_records` & `evidence_items`
Immutable evidence audit trail.
- Multi-domain checks: RETRIEVAL, SPATIAL, TEMPORAL, STRUCTURAL, SPECTRAL.
- Provenance details: source, method, timestamp, geometry.

### 6. `review_tasks` & `review_decisions`
Human-in-the-loop escalation queue and auditor log.

### 7. `jobs` & `reports`
Asynchronous job tracking and generated intelligence certifications.
