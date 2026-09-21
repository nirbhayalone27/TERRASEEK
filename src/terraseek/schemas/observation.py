"""Observation schemas."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from terraseek.schemas.common import GeoJSONGeometry


class BandMetadata(BaseModel):
    name: str
    wavelength_nm: Optional[float] = None
    resolution_m: float = 10.0


class ObservationBase(BaseModel):
    site_id: str
    acquisition_date: date
    sensor: str = "Sentinel-2"
    resolution_meters: float = 10.0
    cloud_cover: float = 0.0
    usable: bool = True
    asset_path: Optional[str] = None
    thumbnail_url: Optional[str] = None
    bands: List[str] = Field(default_factory=lambda: ["B02", "B03", "B04", "B08"])
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ObservationCreate(ObservationBase):
    pass


class ObservationRead(ObservationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
