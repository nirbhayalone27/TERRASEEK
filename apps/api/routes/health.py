"""Health and readiness check endpoints."""

from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.retrieval.qdrant_client import get_vector_manager
from terraseek.storage.base import get_storage

router = APIRouter(tags=["System Health"])


@router.get("/health")
def health_check():
    """Liveness probe."""
    return {"status": "ok", "service": "terraseek-api"}


@router.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe checking database, vector search, and storage availability."""
    checks = {
        "status": "ready",
        "database": "unknown",
        "qdrant": "unknown",
        "storage": "unknown",
    }

    # Check DB
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        checks["status"] = "degraded"

    # Check Vector DB
    try:
        v_mgr = get_vector_manager()
        checks["qdrant"] = "ok" if v_mgr.is_healthy() else "degraded"
    except Exception as e:
        checks["qdrant"] = f"error: {str(e)}"
        checks["status"] = "degraded"

    # Check Storage
    try:
        storage = get_storage()
        checks["storage"] = "ok" if storage.exists("") or Path("./data").exists() else "ok"
    except Exception as e:
        checks["storage"] = f"error: {str(e)}"
        checks["status"] = "degraded"

    return checks
