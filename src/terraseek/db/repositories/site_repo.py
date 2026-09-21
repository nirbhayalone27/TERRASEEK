"""Site repository for database operations."""

from typing import List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import SiteModel
from terraseek.schemas.site import SiteCreate


class SiteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, site_id: str) -> Optional[SiteModel]:
        return self.db.query(SiteModel).filter(SiteModel.id == site_id).first()

    def get_by_name(self, name: str) -> Optional[SiteModel]:
        return self.db.query(SiteModel).filter(SiteModel.name == name).first()

    def list_all(self, limit: int = 50, offset: int = 0) -> List[SiteModel]:
        return self.db.query(SiteModel).offset(offset).limit(limit).all()

    def create(self, site: SiteCreate) -> SiteModel:
        db_site = SiteModel(
            id=site.id if site.id else None,
            name=site.name,
            location_name=site.location_name,
            latitude=site.latitude,
            longitude=site.longitude,
            boundary=site.boundary,
            description=site.description,
            tags=site.tags,
            meta_info=site.metadata,
        )
        self.db.add(db_site)
        self.db.commit()
        self.db.refresh(db_site)
        return db_site

    def count(self) -> int:
        return self.db.query(SiteModel).count()
