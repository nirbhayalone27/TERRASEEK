"""Background jobs endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.db.repositories import JobRepository
from terraseek.schemas.job import JobCreate, JobRead

router = APIRouter(prefix="/jobs", tags=["Jobs & Async Workers"])


@router.post("", response_model=JobRead)
def submit_job(job: JobCreate, db: Session = Depends(get_db)):
    """Submit a long-running asynchronous geospatial task."""
    repo = JobRepository(db)
    db_job = repo.create(job)
    return JobRead(
        id=db_job.id,
        job_type=db_job.job_type,
        status=db_job.status,
        progress_percentage=db_job.progress_percentage,
        created_at=db_job.created_at,
        payload=db_job.payload or {},
        result=db_job.result,
        error_message=db_job.error_message,
    )


@router.get("/{job_id}", response_model=JobRead)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """Check status and progress of a background job."""
    repo = JobRepository(db)
    db_job = repo.get_by_id(job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")

    return JobRead(
        id=db_job.id,
        job_type=db_job.job_type,
        status=db_job.status,
        progress_percentage=db_job.progress_percentage,
        created_at=db_job.created_at,
        started_at=db_job.started_at,
        finished_at=db_job.finished_at,
        error_message=db_job.error_message,
        payload=db_job.payload or {},
        result=db_job.result,
    )
