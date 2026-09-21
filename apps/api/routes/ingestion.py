"""Catalog ingestion route."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.db.repositories import SiteRepository
from terraseek.schemas.ingestion import IngestionItemCreate, IngestionResult
from terraseek.ingestion.pipeline import IngestionPipeline

router = APIRouter(prefix="/ingestion", tags=["Catalog Ingestion"])


@router.post("/catalog", response_model=IngestionResult)
def ingest_catalog_item(item: IngestionItemCreate, db: Session = Depends(get_db)):
    """Ingest, validate, quality-check, and index an imagery raster asset."""
    site_repo = SiteRepository(db)
    sites = site_repo.list_all(limit=1)
    if not sites:
        raise HTTPException(status_code=400, detail="No sites available for ingestion attachment.")

    pipeline = IngestionPipeline(db)
    return pipeline.ingest_asset(item, site_id=sites[0].id)
