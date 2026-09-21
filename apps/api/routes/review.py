"""Human-in-the-loop review queue and decision routes."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.db.repositories import ReviewRepository, SiteRepository
from terraseek.schemas.review import (
    ReviewDecisionCreate,
    ReviewDecisionRead,
    ReviewTaskRead,
)

router = APIRouter(prefix="/review", tags=["Review Workflow"])


@router.get("/queue", response_model=List[ReviewTaskRead])
def get_review_queue(status: Optional[str] = "PENDING", db: Session = Depends(get_db)):
    """List pending or resolved analyst review tasks."""
    repo = ReviewRepository(db)
    site_repo = SiteRepository(db)
    tasks = repo.list_queue(status=status)

    results = []
    for t in tasks:
        site = site_repo.get_by_id(t.site_id)
        results.append(
            ReviewTaskRead(
                id=t.id,
                site_id=t.site_id,
                site_name=site.name if site else t.site_id,
                evidence_id=t.evidence_id,
                query=t.query,
                reason=t.reason,
                flagged_by=t.flagged_by,
                status=t.status,
                created_at=t.created_at,
            )
        )
    return results


@router.post("/{review_id}/decision", response_model=ReviewDecisionRead)
def submit_review_decision(
    review_id: str,
    decision: ReviewDecisionCreate,
    db: Session = Depends(get_db),
):
    """Record reviewer determination (APPROVE | REJECT | NEEDS_MORE_EVIDENCE)."""
    repo = ReviewRepository(db)
    task = repo.get_task(review_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Review task '{review_id}' not found.")

    dec = repo.add_decision(review_id, decision)
    return ReviewDecisionRead(
        id=dec.id,
        task_id=dec.task_id,
        decision=dec.decision,
        reviewer_notes=dec.reviewer_notes,
        reviewer_id=dec.reviewer_id,
        decided_at=dec.decided_at,
    )
