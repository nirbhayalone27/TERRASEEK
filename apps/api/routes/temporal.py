"""Temporal verification routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.db.repositories import ObservationRepository, ChangeEventRepository
from terraseek.schemas.temporal import (
    EarliestObservationRequest,
    EarliestObservationResult,
    TemporalObservation,
    TemporalVerificationRequest,
    TemporalVerificationResult,
)
from terraseek.temporal.engine import TemporalEngine

router = APIRouter(prefix="/temporal", tags=["Temporal Reasoning"])


@router.post("/verify", response_model=TemporalVerificationResult)
def verify_temporal_timeline(
    request: TemporalVerificationRequest,
    db: Session = Depends(get_db),
):
    """Verify satellite observation continuity and temporal coverage for a site."""
    obs_repo = ObservationRepository(db)
    observations = obs_repo.list_by_site(request.site_id)

    temp_obs = [
        TemporalObservation(
            id=o.id,
            site_id=o.site_id,
            acquisition_date=o.acquisition_date,
            sensor=o.sensor,
            cloud_cover_percentage=o.cloud_cover,
            usable=o.usable,
        )
        for o in observations
    ]

    return TemporalEngine.verify_timeline(temp_obs, min_required=request.min_observations)


@router.post("/earliest", response_model=EarliestObservationResult)
def get_earliest_supported_observation(
    request: EarliestObservationRequest,
    db: Session = Depends(get_db),
):
    """Determine the earliest satellite observation where target change/event is evidenced."""
    obs_repo = ObservationRepository(db)
    chg_repo = ChangeEventRepository(db)

    observations = obs_repo.list_by_site(request.site_id)
    changes = [
        {"later_date": c.later_date, "earlier_date": c.earlier_date, "type": c.change_type}
        for c in chg_repo.list_by_site(request.site_id)
    ]

    temp_obs = [
        TemporalObservation(
            id=o.id,
            site_id=o.site_id,
            acquisition_date=o.acquisition_date,
            sensor=o.sensor,
            usable=o.usable,
        )
        for o in observations
    ]

    res = TemporalEngine.determine_earliest_supported_observation(temp_obs, changes)

    return EarliestObservationResult(
        site_id=request.site_id,
        earliest_observation_date=res.get("earliest_date"),
        confidence_status=res.get("status"),
        observation_id=res.get("observation_id"),
        description=res.get("description"),
    )
