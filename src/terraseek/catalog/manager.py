"""Catalog management for satellite assets and observations."""

from datetime import date
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from terraseek.db.models import SiteModel, ObservationModel
from terraseek.db.repositories import SiteRepository, ObservationRepository


class CatalogManager:
    def __init__(self, db: Session):
        self.db = db
        self.site_repo = SiteRepository(db)
        self.obs_repo = ObservationRepository(db)

    def search_catalog(
        self,
        sensor: Optional[str] = None,
        max_cloud_cover: Optional[float] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        query = self.db.query(ObservationModel)
        if sensor:
            query = query.filter(ObservationModel.sensor.ilike(f"%{sensor}%"))
        if max_cloud_cover is not None:
            query = query.filter(ObservationModel.cloud_cover <= max_cloud_cover)
        if start_date:
            query = query.filter(ObservationModel.acquisition_date >= start_date)
        if end_date:
            query = query.filter(ObservationModel.acquisition_date <= end_date)

        results = query.order_by(ObservationModel.acquisition_date.desc()).limit(limit).all()
        return [
            {
                "observation_id": o.id,
                "site_id": o.site_id,
                "acquisition_date": o.acquisition_date.isoformat(),
                "sensor": o.sensor,
                "resolution_meters": o.resolution_meters,
                "cloud_cover": o.cloud_cover,
                "usable": o.usable,
                "asset_path": o.asset_path,
                "thumbnail_url": o.thumbnail_url,
                "bands": o.bands,
            }
            for o in results
        ]
