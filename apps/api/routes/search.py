"""Natural language search route."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.schemas.search import SearchRequest, SearchResponse
from terraseek.workflow.orchestrator import MissionWorkflowOrchestrator

router = APIRouter(tags=["Search & Discovery"])


@router.post("/search", response_model=SearchResponse)
def execute_search(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    """Execute natural language satellite search with complete evidence reasoning."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    orchestrator = MissionWorkflowOrchestrator(db)
    return orchestrator.execute_search_mission(request.query, limit=request.limit)
