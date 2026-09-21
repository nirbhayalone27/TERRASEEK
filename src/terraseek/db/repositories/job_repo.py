"""Job repository for background task persistence."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import JobModel
from terraseek.schemas.common import JobStatus
from terraseek.schemas.job import JobCreate


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, job_id: str) -> Optional[JobModel]:
        return self.db.query(JobModel).filter(JobModel.id == job_id).first()

    def list_recent(self, limit: int = 50) -> List[JobModel]:
        return self.db.query(JobModel).order_by(JobModel.created_at.desc()).limit(limit).all()

    def create(self, job: JobCreate, job_id: Optional[str] = None) -> JobModel:
        db_job = JobModel(
            id=job_id,
            job_type=job.job_type,
            status=JobStatus.QUEUED.value,
            progress_percentage=0.0,
            payload=job.payload,
        )
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        progress: Optional[float] = None,
        result: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
    ) -> Optional[JobModel]:
        db_job = self.get_by_id(job_id)
        if not db_job:
            return None

        db_job.status = status.value if hasattr(status, "value") else str(status)
        if progress is not None:
            db_job.progress_percentage = progress
        if result is not None:
            db_job.result = result
        if error_message is not None:
            db_job.error_message = error_message

        if status == JobStatus.RUNNING and not db_job.started_at:
            db_job.started_at = datetime.utcnow()
        elif status in (JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELLED):
            db_job.finished_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(db_job)
        return db_job
