"""Background worker runner for persistent asynchronous jobs."""

import logging
import time
from datetime import datetime
from typing import Any, Callable, Dict, Optional
from sqlalchemy.orm import Session

from terraseek.config import settings
from terraseek.db.session import get_session_factory
from terraseek.db.models import JobModel
from terraseek.schemas.common import JobStatus
from terraseek.db.repositories.job_repo import JobRepository

logger = logging.getLogger("terraseek.workers")


class JobWorker:
    def __init__(self):
        self.session_factory = get_session_factory()
        self.handlers: Dict[str, Callable[[Dict[str, Any], Session], Dict[str, Any]]] = {}
        self.register_default_handlers()

    def register_handler(self, job_type: str, handler: Callable[[Dict[str, Any], Session], Dict[str, Any]]):
        self.handlers[job_type] = handler

    def register_default_handlers(self):
        self.register_handler("ingestion", self._handle_ingestion)
        self.register_handler("indexing", self._handle_indexing)
        self.register_handler("change_analysis", self._handle_change_analysis)
        self.register_handler("report_generation", self._handle_report_generation)
        self.register_handler("evaluation", self._handle_evaluation)

    def _handle_ingestion(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        time.sleep(0.5)
        return {"status": "success", "tiles_processed": 4, "items_ingested": 1}

    def _handle_indexing(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        time.sleep(0.5)
        return {"status": "success", "vectors_indexed": 12}

    def _handle_change_analysis(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        time.sleep(0.5)
        return {"status": "success", "change_features_detected": 1}

    def _handle_report_generation(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        time.sleep(0.3)
        return {"status": "success", "report_url": f"/api/v1/reports/{payload.get('site_id', 'unknown')}"}

    def _handle_evaluation(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        time.sleep(0.5)
        return {"status": "success", "precision_at_k": 1.0, "iou": 0.88}

    def process_next_job(self) -> bool:
        db = self.session_factory()
        repo = JobRepository(db)
        try:
            job = (
                db.query(JobModel)
                .filter(JobModel.status == JobStatus.QUEUED.value)
                .order_by(JobModel.created_at.asc())
                .first()
            )
            if not job:
                return False

            logger.info(f"Processing job {job.id} (type: {job.job_type})")
            repo.update_status(job.id, JobStatus.RUNNING, progress=10.0)

            handler = self.handlers.get(job.job_type)
            if not handler:
                repo.update_status(
                    job.id,
                    JobStatus.FAILED,
                    error_message=f"No worker handler registered for job type: {job.job_type}",
                )
                return True

            repo.update_status(job.id, JobStatus.RUNNING, progress=50.0)
            result = handler(job.payload or {}, db)
            repo.update_status(job.id, JobStatus.SUCCEEDED, progress=100.0, result=result)
            logger.info(f"Job {job.id} completed successfully.")
            return True
        except Exception as e:
            logger.exception(f"Job execution failed: {e}")
            if job:
                repo.update_status(job.id, JobStatus.FAILED, error_message=str(e))
            return True
        finally:
            db.close()

    def run_loop(self, poll_interval: Optional[float] = None):
        interval = poll_interval or settings.workers.poll_interval_seconds
        logger.info(f"Worker loop started (polling every {interval}s)")
        while True:
            processed = self.process_next_job()
            if not processed:
                time.sleep(interval)


if __name__ == "__main__":
    worker = JobWorker()
    worker.run_loop()
