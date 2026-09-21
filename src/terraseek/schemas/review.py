"""Review schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from terraseek.schemas.common import EvidenceStatus, ReviewDecisionType


class ReviewTaskBase(BaseModel):
    site_id: str
    evidence_id: str
    query: str
    reason: str
    flagged_by: str = "system"


class ReviewTaskCreate(ReviewTaskBase):
    pass


class ReviewTaskRead(ReviewTaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: str = "PENDING"  # PENDING, RESOLVED
    created_at: datetime
    site_name: Optional[str] = None
    evidence_status: Optional[EvidenceStatus] = None
    details: Dict[str, Any] = Field(default_factory=dict)


class ReviewDecisionCreate(BaseModel):
    decision: ReviewDecisionType
    reviewer_notes: str
    reviewer_id: str = "analyst_1"


class ReviewDecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    task_id: str
    decision: ReviewDecisionType
    reviewer_notes: str
    reviewer_id: str
    decided_at: datetime
