"""Evidence schemas and Evidence Passport."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from terraseek.schemas.common import EvidenceStatus


class EvidenceType(str, Enum):
    RETRIEVAL = "RETRIEVAL"
    SPATIAL = "SPATIAL"
    TEMPORAL = "TEMPORAL"
    STRUCTURAL = "STRUCTURAL"
    SPECTRAL = "SPECTRAL"
    IMAGE = "IMAGE"
    METADATA = "METADATA"


class EvidenceItem(BaseModel):
    id: str
    evidence_type: EvidenceType
    title: str
    description: str
    status: EvidenceStatus
    source: str
    asset_id: Optional[str] = None
    observation_id: Optional[str] = None
    method: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    geometry: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvidencePassport(BaseModel):
    id: str
    site_id: str
    query: str
    status: EvidenceStatus
    items: List[EvidenceItem] = Field(default_factory=list)
    spatial_summary: str
    temporal_summary: str
    change_summary: str
    model_provenance: Dict[str, Any] = Field(default_factory=dict)
    limitations: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    needs_review_reason: Optional[str] = None
