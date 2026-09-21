"""Evidence repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import EvidenceRecordModel, EvidenceItemModel
from terraseek.schemas.evidence import EvidenceItem, EvidencePassport


class EvidenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_record(self, record_id: str) -> Optional[EvidenceRecordModel]:
        return self.db.query(EvidenceRecordModel).filter(EvidenceRecordModel.id == record_id).first()

    def get_latest_by_site(self, site_id: str) -> Optional[EvidenceRecordModel]:
        return (
            self.db.query(EvidenceRecordModel)
            .filter(EvidenceRecordModel.site_id == site_id)
            .order_by(EvidenceRecordModel.created_at.desc())
            .first()
        )

    def save_passport(self, passport: EvidencePassport) -> EvidenceRecordModel:
        record = EvidenceRecordModel(
            id=passport.id,
            site_id=passport.site_id,
            query=passport.query,
            status=passport.status.value if hasattr(passport.status, "value") else str(passport.status),
            spatial_summary=passport.spatial_summary,
            temporal_summary=passport.temporal_summary,
            change_summary=passport.change_summary,
            model_provenance=passport.model_provenance,
            limitations=passport.limitations,
            needs_review_reason=passport.needs_review_reason,
            created_at=passport.created_at,
        )
        self.db.add(record)
        self.db.flush()

        for item in passport.items:
            db_item = EvidenceItemModel(
                id=item.id,
                record_id=record.id,
                evidence_type=item.evidence_type.value if hasattr(item.evidence_type, "value") else str(item.evidence_type),
                title=item.title,
                description=item.description,
                status=item.status.value if hasattr(item.status, "value") else str(item.status),
                source=item.source,
                asset_id=item.asset_id,
                observation_id=item.observation_id,
                method=item.method,
                timestamp=item.timestamp,
                geometry=item.geometry,
                meta_info=item.metadata,
            )
            self.db.add(db_item)

        self.db.commit()
        self.db.refresh(record)
        return record
