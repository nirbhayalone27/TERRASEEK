"""Change event repository."""

from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import ChangeEventModel
from terraseek.schemas.change import ChangeEventBase


class ChangeEventRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, change_id: str) -> Optional[ChangeEventModel]:
        return self.db.query(ChangeEventModel).filter(ChangeEventModel.id == change_id).first()

    def list_by_site(self, site_id: str) -> List[ChangeEventModel]:
        return (
            self.db.query(ChangeEventModel)
            .filter(ChangeEventModel.site_id == site_id)
            .order_by(ChangeEventModel.later_date.desc())
            .all()
        )

    def create(
        self,
        event: ChangeEventBase,
        geometry: Optional[dict] = None,
        event_id: Optional[str] = None,
    ) -> ChangeEventModel:
        db_event = ChangeEventModel(
            id=event_id,
            site_id=event.site_id,
            change_type=event.change_type.value if hasattr(event.change_type, "value") else str(event.change_type),
            earlier_date=event.earlier_date,
            later_date=event.later_date,
            earlier_observation_id=event.earlier_observation_id,
            later_observation_id=event.later_observation_id,
            area_sq_meters=event.area_sq_meters,
            status=event.status.value if hasattr(event.status, "value") else str(event.status),
            model_name=event.model_name,
            model_tier=event.model_tier.value if hasattr(event.model_tier, "value") else str(event.model_tier),
            geometry=geometry,
            provenance=event.provenance,
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event
