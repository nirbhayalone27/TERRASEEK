# Ingestion & Catalog Pipeline

TerraSeek processes raw satellite imagery through an automated multi-stage pipeline:

```
Source Raster (GeoTIFF/COG)
       ↓
Metadata Discovery (Bands, Sensor, Acquisition Date)
       ↓
Quality Assessment (Cloud Cover, NoData Ratio, Dimensions)
       ↓
Raster Normalization & Windowing
       ↓
RGB Thumbnail Extraction
       ↓
Catalog Registration (PostgreSQL / PostGIS)
       ↓
Embedding Generation (GeoRSCLIP / Demo Adapter)
       ↓
Vector Indexing (Qdrant)
```

## Quality Assessment (`QualityChecker`)
- Validates raster dimensions (minimum 32x32).
- Validates spectral band counts (minimum 3 bands).
- Inspects nodata pixels (rejects files exceeding 20% nodata).
- Detects cloud occlusion via spectral reflectance thresholds.
- Verifies temporal metadata integrity.
