"""Spatial schemas and constraint models."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from terraseek.schemas.common import EvidenceStatus, GeoJSONGeometry


class SpatialConstraint(BaseModel):
    feature_type: str = Field(..., description="Target feature type e.g., river, road, lake")
    relation: str = Field(default="within", description="within | intersects | contains | disjoint")
    distance_meters: float = Field(default=500.0, description="Buffer distance in meters")


class SpatialVerificationRequest(BaseModel):
    site_id: str
    constraints: List[SpatialConstraint]
    site_geometry: Optional[GeoJSONGeometry] = None


class SpatialCheckResult(BaseModel):
    constraint: SpatialConstraint
    satisfied: bool
    measured_distance_meters: Optional[float] = None
    target_feature_name: Optional[str] = None
    description: str


class SpatialVerificationResult(BaseModel):
    status: EvidenceStatus
    checks: List[SpatialCheckResult] = Field(default_factory=list)
    summary: str
