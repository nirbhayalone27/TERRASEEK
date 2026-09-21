"""Search and retrieval schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from terraseek.schemas.common import ChangeType, EvidenceStatus, GeoJSONFeatureCollection


class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    bbox: Optional[List[float]] = Field(default=None, description="Optional bounding box [min_lon, min_lat, max_lon, max_lat]")
    limit: int = Field(default=10, ge=1, le=50)


class SearchResultItem(BaseModel):
    site_id: str
    site_name: str
    location_name: str
    change_type: ChangeType
    earlier_date: Optional[str] = None
    later_date: Optional[str] = None
    status: EvidenceStatus
    evidence_summary: str
    spatial_summary: str
    temporal_summary: str
    change_summary: str
    latitude: float
    longitude: float
    geometry: Optional[Dict[str, Any]] = None
    relevance_score: Optional[float] = None
    evidence_id: Optional[str] = None


class MissionIntent(BaseModel):
    raw_query: str
    target_entity: str
    change_detected_required: bool
    change_type: ChangeType
    spatial_constraints: List[Dict[str, Any]] = Field(default_factory=list)
    temporal_required: bool
    earlier_imagery_required: bool
    is_known_unmatchable: bool = False


class SearchResponse(BaseModel):
    query: str
    mission: MissionIntent
    status: EvidenceStatus
    total_results: int
    results: List[SearchResultItem] = Field(default_factory=list)
    execution_plan: List[str] = Field(default_factory=list)
    summary: str


class SimilarRetrievalRequest(BaseModel):
    image_asset_id: Optional[str] = None
    limit: int = Field(default=5, ge=1, le=20)


class SimilarRetrievalItem(BaseModel):
    site_id: str
    site_name: str
    location_name: str
    similarity_score: float
    acquisition_date: Optional[str] = None
    thumbnail_url: Optional[str] = None
    latitude: float
    longitude: float
    evidence_status: EvidenceStatus
    model_provider: str = "DemoEmbeddingProvider"


class SimilarRetrievalResponse(BaseModel):
    query_reference: str
    model_provider: str
    is_demo: bool = True
    total: int
    results: List[SimilarRetrievalItem] = Field(default_factory=list)
