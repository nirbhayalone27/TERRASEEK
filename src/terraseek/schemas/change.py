"""Change analysis schemas and results."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from terraseek.schemas.common import ChangeType, EvidenceStatus, GeoJSONFeatureCollection, ModelTier


class ChangeEventBase(BaseModel):
    site_id: str
    change_type: ChangeType
    earlier_date: date
    later_date: date
    earlier_observation_id: Optional[str] = None
    later_observation_id: Optional[str] = None
    area_sq_meters: float = 0.0
    status: EvidenceStatus = EvidenceStatus.SUPPORTED
    model_name: str = "demo-change-detector"
    model_tier: ModelTier = ModelTier.DEMO
    provenance: Dict[str, Any] = Field(default_factory=dict)


class ChangeEventRead(ChangeEventBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    geometry: Optional[Dict[str, Any]] = None
    created_at: datetime


class CompareRequest(BaseModel):
    earlier_image_id: Optional[str] = None
    later_image_id: Optional[str] = None
    change_types: List[ChangeType] = Field(default_factory=lambda: [ChangeType.BUILDING])


class CompareResult(BaseModel):
    model_tier: ModelTier
    model_name: str
    model_version: str
    earlier_date: Optional[date] = None
    later_date: Optional[date] = None
    detected_changes: List[ChangeEventRead] = Field(default_factory=list)
    change_mask_url: Optional[str] = None
    spectral_summary: Optional[Dict[str, float]] = None
    status: EvidenceStatus
    summary: str


class ChangeAnalyzeRequest(BaseModel):
    site_id: str
    earlier_date: Optional[date] = None
    later_date: Optional[date] = None
    change_types: List[ChangeType] = Field(default_factory=lambda: [ChangeType.BUILDING])


class ChangeAnalyzeResult(BaseModel):
    site_id: str
    status: EvidenceStatus
    earlier_date: date
    later_date: date
    features: GeoJSONFeatureCollection
    changes: List[ChangeEventRead] = Field(default_factory=list)
    model_tier: ModelTier
    summary: str
