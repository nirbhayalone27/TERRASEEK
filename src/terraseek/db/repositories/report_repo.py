"""Report repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import ReportModel
from terraseek.schemas.common import EvidenceStatus


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, report_id: str) -> Optional[ReportModel]:
        return self.db.query(ReportModel).filter(ReportModel.id == report_id).first()

    def list_by_site(self, site_id: str) -> List[ReportModel]:
        return self.db.query(ReportModel).filter(ReportModel.site_id == site_id).order_by(ReportModel.created_at.desc()).all()

    def create(
        self,
        site_id: str,
        query: str,
        status: EvidenceStatus,
        content: dict,
        report_format: str = "json",
        report_id: Optional[str] = None,
    ) -> ReportModel:
        db_report = ReportModel(
            id=report_id,
            site_id=site_id,
            query=query,
            status=status.value if hasattr(status, "value") else str(status),
            content=content,
            report_format=report_format,
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report
