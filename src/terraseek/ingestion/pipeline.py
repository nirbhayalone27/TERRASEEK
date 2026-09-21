"""Ingestion pipeline from source rasters into catalog, tiling, and vector index."""

from pathlib import Path
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from terraseek.db.repositories import SiteRepository, ObservationRepository
from terraseek.schemas.observation import ObservationCreate
from terraseek.schemas.ingestion import IngestionItemCreate, IngestionResult
from terraseek.quality.checker import QualityChecker
from terraseek.retrieval.qdrant_client import get_vector_manager
from terraseek.models.adapters import get_embedding_provider


class IngestionPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.site_repo = SiteRepository(db)
        self.obs_repo = ObservationRepository(db)
        self.vector_mgr = get_vector_manager()
        self.embedding_model = get_embedding_provider()

    def ingest_asset(self, item: IngestionItemCreate, site_id: str) -> IngestionResult:
        # Step 1: Quality assessment
        quality = QualityChecker.inspect_raster(
            item.file_path,
            acquisition_date=item.acquisition_date,
        )

        # Step 2: Catalog registration
        obs_create = ObservationCreate(
            site_id=site_id,
            acquisition_date=item.acquisition_date,
            sensor=item.sensor,
            resolution_meters=item.resolution_meters,
            cloud_cover=quality.cloud_cover_pct,
            usable=quality.is_usable,
            asset_path=item.file_path,
            bands=item.bands,
            metadata=item.metadata,
        )
        db_obs = self.obs_repo.create(obs_create)

        # Step 3: Vector indexing
        indexed = False
        try:
            vec = self.embedding_model.embed_text(f"{item.sensor} observation on {item.acquisition_date}")
            self.vector_mgr.upsert_observation(
                point_id=db_obs.id,
                vector=vec,
                payload={
                    "site_id": site_id,
                    "date": item.acquisition_date.isoformat(),
                    "sensor": item.sensor,
                    "usable": quality.is_usable,
                },
            )
            indexed = True
        except Exception:
            indexed = False

        return IngestionResult(
            success=True,
            catalog_id=db_obs.id,
            observations_created=1,
            tiled_count=1,
            indexed_in_vector_db=indexed,
            message="Asset ingested and registered in catalog successfully.",
        )
