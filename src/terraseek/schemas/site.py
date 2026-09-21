"""Site schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from terraseek.schemas.common import ChangeType, EvidenceStatus, GeoJSONFeature, GeoJSONGeometry


class SiteBase(BaseModel):
    name: str
    location_name: str
    latitude: float
    longitude: float
    boundary: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SiteCreate(SiteBase):
    id: Optional[str] = None


class SiteRead(SiteBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    primary_change_type: Optional[ChangeType] = None
    evidence_status: EvidenceStatus = EvidenceStatus.SUPPORTED
    earliest_observation_date: Optional[str] = None
    latest_observation_date: Optional[str] = None


class SiteDetail(SiteRead):
    spatial_verification_summary: Optional[str] = None
    temporal_verification_summary: Optional[str] = None
    change_evidence_summary: Optional[str] = None
    latest_evidence_id: Optional[str] = None
