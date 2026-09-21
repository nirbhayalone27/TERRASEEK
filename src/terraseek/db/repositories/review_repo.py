"""Review repository."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from terraseek.db.models import ReviewTaskModel, ReviewDecisionModel
from terraseek.schemas.review import ReviewDecisionCreate, ReviewTaskCreate


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_queue(self, status: Optional[str] = "PENDING") -> List[ReviewTaskModel]:
        query = self.db.query(ReviewTaskModel)
        if status:
            query = query.filter(ReviewTaskModel.status == status)
        return query.order_by(ReviewTaskModel.created_at.desc()).all()

    def get_task(self, task_id: str) -> Optional[ReviewTaskModel]:
        return self.db.query(ReviewTaskModel).filter(ReviewTaskModel.id == task_id).first()

    def create_task(self, task: ReviewTaskCreate, task_id: Optional[str] = None) -> ReviewTaskModel:
        db_task = ReviewTaskModel(
            id=task_id,
            site_id=task.site_id,
            evidence_id=task.evidence_id,
            query=task.query,
            reason=task.reason,
            flagged_by=task.flagged_by,
            status="PENDING",
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def add_decision(self, task_id: str, decision: ReviewDecisionCreate) -> ReviewDecisionModel:
        db_decision = ReviewDecisionModel(
            task_id=task_id,
            decision=decision.decision.value if hasattr(decision.decision, "value") else str(decision.decision),
            reviewer_notes=decision.reviewer_notes,
            reviewer_id=decision.reviewer_id,
            decided_at=datetime.utcnow(),
        )
        self.db.add(db_decision)
        task = self.get_task(task_id)
        if task:
            task.status = "RESOLVED"
        self.db.commit()
        self.db.refresh(db_decision)
        return db_decision
