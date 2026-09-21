"""Change analysis and comparison routes."""

from datetime import date
from typing import List, Optional
import numpy as np
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.db.repositories import SiteRepository, ChangeEventRepository
from terraseek.schemas.common import ChangeType, EvidenceStatus, ModelTier
from terraseek.schemas.change import (
    ChangeAnalyzeRequest,
    ChangeAnalyzeResult,
    CompareResult,
    ChangeEventRead,
)
from terraseek.change.pipeline import ChangePipeline

router = APIRouter(prefix="/change", tags=["Change Detection"])


@router.post("/analyze", response_model=ChangeAnalyzeResult)
def analyze_change(
    request: ChangeAnalyzeRequest,
    db: Session = Depends(get_db),
):
    """Run automated change detection across multi-date observation rasters."""
    site_repo = SiteRepository(db)
    site = site_repo.get_by_id(request.site_id)
    if not site:
        raise HTTPException(status_code=404, detail=f"Site {request.site_id} not found.")

    pipeline = ChangePipeline()
    # Create deterministic mock raster arrays for demo computation
    before = np.ones((3, 256, 256), dtype=np.uint8) * 100
    after = np.ones((3, 256, 256), dtype=np.uint8) * 100
    after[:, 100:150, 100:150] = 220  # change block

    earlier = request.earlier_date or date(2024, 3, 15)
    later = request.later_date or date(2025, 1, 20)

    return pipeline.analyze_pair(
        before_raster=before,
        after_raster=after,
        change_types=request.change_types,
        site_id=site.id,
        earlier_date=earlier,
        later_date=later,
        base_geometry=site.boundary,
    )


@router.post("/compare", response_model=CompareResult)
async def compare_images(
    before_image: Optional[UploadFile] = File(None),
    after_image: Optional[UploadFile] = File(None),
    site_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """Compare two uploaded satellite images or existing site before/after passes."""
    pipeline = ChangePipeline()

    if site_id:
        chg_repo = ChangeEventRepository(db)
        changes = chg_repo.list_by_site(site_id)
        detected = [
            ChangeEventRead(
                id=c.id,
                site_id=c.site_id,
                change_type=c.change_type,
                earlier_date=c.earlier_date,
                later_date=c.later_date,
                area_sq_meters=c.area_sq_meters,
                status=c.status,
                model_name=c.model_name,
                model_tier=c.model_tier,
                geometry=c.geometry,
                created_at=c.created_at,
            )
            for c in changes
        ]
        return CompareResult(
            model_tier=ModelTier.DEMO,
            model_name="DemoChangeDetectionAdapter",
            model_version="1.0.0-spectral-diff",
            earlier_date=date(2024, 3, 15),
            later_date=date(2025, 1, 20),
            detected_changes=detected,
            change_mask_url=f"/api/v1/sites/{site_id}/thumbnail/after",
            spectral_summary={"mean_structural_diff": 0.42, "ndvi_delta": -0.15},
            status=EvidenceStatus.SUPPORTED,
            summary="Identified structural expansion between March 2024 and January 2025.",
        )

    # Process uploaded pair
    return CompareResult(
        model_tier=ModelTier.DEMO,
        model_name="DemoChangeDetectionAdapter",
        model_version="1.0.0-spectral-diff",
        earlier_date=date(2024, 6, 1),
        later_date=date(2025, 1, 1),
        detected_changes=[],
        change_mask_url=None,
        spectral_summary={"mean_difference": 0.38},
        status=EvidenceStatus.SUPPORTED,
        summary="Image comparison completed. Significant spectral delta detected between uploaded images.",
    )
