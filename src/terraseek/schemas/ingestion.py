"""Catalog ingestion schemas."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class IngestionItemCreate(BaseModel):
    source_name: str
    sensor: str = "Sentinel-2"
    acquisition_date: date
    bbox: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    resolution_meters: float = 10.0
    cloud_cover_percentage: float = 0.0
    file_path: str
    bands: List[str] = Field(default_factory=lambda: ["B02", "B03", "B04", "B08"])
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestionResult(BaseModel):
    success: bool
    catalog_id: str
    observations_created: int
    tiled_count: int
    indexed_in_vector_db: bool
    message: str
