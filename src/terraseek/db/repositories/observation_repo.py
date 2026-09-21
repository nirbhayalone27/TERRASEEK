"""Observation repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import ObservationModel
from terraseek.schemas.observation import ObservationCreate


class ObservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obs_id: str) -> Optional[ObservationModel]:
        return self.db.query(ObservationModel).filter(ObservationModel.id == obs_id).first()

    def list_by_site(self, site_id: str) -> List[ObservationModel]:
        return (
            self.db.query(ObservationModel)
            .filter(ObservationModel.site_id == site_id)
            .order_by(ObservationModel.acquisition_date.asc())
            .all()
        )

    def create(self, obs: ObservationCreate, obs_id: Optional[str] = None) -> ObservationModel:
        db_obs = ObservationModel(
            id=obs_id,
            site_id=obs.site_id,
            acquisition_date=obs.acquisition_date,
            sensor=obs.sensor,
            resolution_meters=obs.resolution_meters,
            cloud_cover=obs.cloud_cover,
            usable=obs.usable,
            asset_path=obs.asset_path,
            thumbnail_url=obs.thumbnail_url,
            bands=obs.bands,
            meta_info=obs.metadata,
        )
        self.db.add(db_obs)
        self.db.commit()
        self.db.refresh(db_obs)
        return db_obs
