"""Spatial feature repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import SpatialFeatureModel


class SpatialFeatureRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_site(self, site_id: str) -> List[SpatialFeatureModel]:
        return self.db.query(SpatialFeatureModel).filter(SpatialFeatureModel.site_id == site_id).all()

    def list_by_site_and_type(self, site_id: str, feature_type: str) -> List[SpatialFeatureModel]:
        return (
            self.db.query(SpatialFeatureModel)
            .filter(
                SpatialFeatureModel.site_id == site_id,
                SpatialFeatureModel.feature_type.ilike(f"%{feature_type}%")
            )
            .all()
        )

    def create(
        self,
        site_id: str,
        feature_type: str,
        name: str,
        geometry: dict,
        meta_info: Optional[dict] = None,
        feature_id: Optional[str] = None,
    ) -> SpatialFeatureModel:
        db_feat = SpatialFeatureModel(
            id=feature_id,
            site_id=site_id,
            feature_type=feature_type,
            name=name,
            geometry=geometry,
            meta_info=meta_info or {},
        )
        self.db.add(db_feat)
        self.db.commit()
        self.db.refresh(db_feat)
        return db_feat
