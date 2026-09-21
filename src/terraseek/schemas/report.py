"""Evidence report schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from terraseek.schemas.common import EvidenceStatus
from terraseek.schemas.evidence import EvidenceItem


class ReportCreate(BaseModel):
    site_id: str
    query: str
    evidence_id: Optional[str] = None
    notes: Optional[str] = None


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    site_id: str
    site_name: str
    query: str
    status: EvidenceStatus
    observation_timeline: List[Dict[str, Any]] = Field(default_factory=list)
    spatial_verification: Dict[str, Any] = Field(default_factory=dict)
    change_analysis: Dict[str, Any] = Field(default_factory=dict)
    temporal_verification: Dict[str, Any] = Field(default_factory=dict)
    evidence_items: List[EvidenceItem] = Field(default_factory=list)
    model_provenance: Dict[str, Any] = Field(default_factory=dict)
    limitations: List[str] = Field(default_factory=list)
    conclusion: str
    created_at: datetime
    format: str = "json"
