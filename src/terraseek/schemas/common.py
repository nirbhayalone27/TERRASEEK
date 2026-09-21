"""Common enums, base schemas, and GeoJSON models."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class EvidenceStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    NO_MATCH = "NO_MATCH"


class ChangeType(str, Enum):
    BUILDING = "BUILDING"
    ROAD = "ROAD"
    VEGETATION = "VEGETATION"
    WATER = "WATER"
    UNKNOWN = "UNKNOWN"


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ReviewDecisionType(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    NEEDS_MORE_EVIDENCE = "NEEDS_MORE_EVIDENCE"


class ModelTier(str, Enum):
    DEMO = "DEMO"
    LOCAL_MODEL = "LOCAL_MODEL"
    PRODUCTION = "PRODUCTION"
    UNAVAILABLE = "UNAVAILABLE"


class GeoJSONGeometry(BaseModel):
    type: str  # Point, Polygon, MultiPolygon, LineString, etc.
    coordinates: Any


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[str] = None


class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature] = Field(default_factory=list)


class APIErrorDetails(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class APIErrorResponse(BaseModel):
    error: APIErrorDetails
