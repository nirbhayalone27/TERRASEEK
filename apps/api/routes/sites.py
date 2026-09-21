"""Site detail, observations, and changes routes."""

from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.db.repositories import (
    SiteRepository,
    ObservationRepository,
    ChangeEventRepository,
    EvidenceRepository,
    SpatialFeatureRepository,
)
from terraseek.schemas.site import SiteDetail, SiteRead
from terraseek.schemas.observation import ObservationRead
from terraseek.schemas.change import ChangeEventRead
from terraseek.schemas.common import ChangeType, EvidenceStatus

router = APIRouter(prefix="/sites", tags=["Sites"])


@router.get("", response_model=List[SiteRead])
def list_sites(limit: int = 50, db: Session = Depends(get_db)):
    """List all registered sites in the catalog."""
    repo = SiteRepository(db)
    sites = repo.list_all(limit=limit)
    return [
        SiteRead(
            id=s.id,
            name=s.name,
            location_name=s.location_name,
            latitude=s.latitude,
            longitude=s.longitude,
            boundary=s.boundary,
            description=s.description,
            tags=s.tags or [],
            metadata=s.meta_info or {},
            created_at=s.created_at,
            primary_change_type=s.meta_info.get("primary_change"),
            evidence_status=EvidenceStatus.SUPPORTED,
        )
        for s in sites
    ]


@router.get("/{site_id}", response_model=SiteDetail)
def get_site(site_id: str, db: Session = Depends(get_db)):
    """Get site details, spatial verification summary, and temporal status."""
    site_repo = SiteRepository(db)
    site = site_repo.get_by_id(site_id)
    if not site:
        raise HTTPException(status_code=404, detail=f"Site '{site_id}' not found.")

    obs_repo = ObservationRepository(db)
    observations = obs_repo.list_by_site(site_id)
    earliest_date = observations[0].acquisition_date.strftime("%B %Y") if observations else None
    latest_date = observations[-1].acquisition_date.strftime("%B %Y") if observations else None

    spatial_repo = SpatialFeatureRepository(db)
    features = spatial_repo.list_by_site(site_id)
    feat_names = ", ".join([f.name for f in features]) if features else "None"

    ev_repo = EvidenceRepository(db)
    latest_ev = ev_repo.get_latest_by_site(site_id)

    spatial_summary = (
        f"Within proximity of: {feat_names}." if features else "No landmark constraints violated."
    )
    temporal_summary = (
        f"{len(observations)} usable observations available ({earliest_date} → {latest_date})."
        if observations
        else "No observations recorded."
    )

    return SiteDetail(
        id=site.id,
        name=site.name,
        location_name=site.location_name,
        latitude=site.latitude,
        longitude=site.longitude,
        boundary=site.boundary,
        description=site.description,
        tags=site.tags or [],
        metadata=site.meta_info or {},
        created_at=site.created_at,
        primary_change_type=site.meta_info.get("primary_change"),
        evidence_status=EvidenceStatus.SUPPORTED if (site.meta_info or {}).get("primary_change") != "CONSTRUCTION" else EvidenceStatus.NEEDS_REVIEW,
        earliest_observation_date=earliest_date,
        latest_observation_date=latest_date,
        spatial_verification_summary=spatial_summary,
        temporal_verification_summary=temporal_summary,
        change_evidence_summary=f"Detected {(site.meta_info or {}).get('primary_change', 'surface')} change event.",
        latest_evidence_id=latest_ev.id if latest_ev else None,
    )


@router.get("/{site_id}/observations", response_model=List[ObservationRead])
def get_site_observations(site_id: str, db: Session = Depends(get_db)):
    """List satellite observations for a site in chronological order."""
    repo = ObservationRepository(db)
    obs = repo.list_by_site(site_id)
    return [
        ObservationRead(
            id=o.id,
            site_id=o.site_id,
            acquisition_date=o.acquisition_date,
            sensor=o.sensor,
            resolution_meters=o.resolution_meters,
            cloud_cover=o.cloud_cover,
            usable=o.usable,
            asset_path=o.asset_path,
            thumbnail_url=o.thumbnail_url,
            bands=o.bands or [],
            metadata=o.meta_info or {},
            created_at=o.created_at,
        )
        for o in obs
    ]


@router.get("/{site_id}/changes", response_model=List[ChangeEventRead])
def get_site_changes(site_id: str, db: Session = Depends(get_db)):
    """List detected change events for a site."""
    repo = ChangeEventRepository(db)
    changes = repo.list_by_site(site_id)
    return [
        ChangeEventRead(
            id=c.id,
            site_id=c.site_id,
            change_type=c.change_type,
            earlier_date=c.earlier_date,
            later_date=c.later_date,
            earlier_observation_id=c.earlier_observation_id,
            later_observation_id=c.later_observation_id,
            area_sq_meters=c.area_sq_meters,
            status=c.status,
            model_name=c.model_name,
            model_tier=c.model_tier,
            geometry=c.geometry,
            provenance=c.provenance or {},
            created_at=c.created_at,
        )
        for c in changes
    ]


@router.get("/{site_id}/thumbnail/{view}")
def get_thumbnail(site_id: str, view: str):
    """Serve before or after visual thumbnail image for site comparison."""
    clean_view = "before" if view == "before" else "after"
    thumb_path = Path(f"./data/demo/thumbnails/{site_id}_{clean_view}.png")
    if not thumb_path.exists():
        thumb_path = Path(f"./data/demo/thumbnails/site-01_{clean_view}.png")
    if not thumb_path.exists():
        raise HTTPException(status_code=404, detail="Thumbnail not found.")
    return FileResponse(thumb_path, media_type="image/png")
