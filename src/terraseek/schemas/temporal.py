"""Temporal schemas and models."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from terraseek.schemas.common import EvidenceStatus


class TemporalObservation(BaseModel):
    id: str
    site_id: str
    acquisition_date: date
    sensor: str
    cloud_cover_percentage: float = 0.0
    usable: bool = True
    notes: Optional[str] = None


class TemporalVerificationRequest(BaseModel):
    site_id: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    min_observations: int = 2


class TemporalVerificationResult(BaseModel):
    status: EvidenceStatus
    observations_count: int
    usable_observations_count: int
    has_before_observation: bool
    has_after_observation: bool
    earliest_supported_observation: Optional[date] = None
    latest_observation: Optional[date] = None
    max_gap_days: Optional[int] = None
    summary: str


class EarliestObservationRequest(BaseModel):
    site_id: str
    feature_type: Optional[str] = None


class EarliestObservationResult(BaseModel):
    site_id: str
    earliest_observation_date: Optional[date] = None
    confidence_status: EvidenceStatus
    observation_id: Optional[str] = None
    description: str
