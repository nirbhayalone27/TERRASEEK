"""Vector similarity retrieval routes."""

from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from sqlalchemy.orm import Session

from terraseek.db.session import get_db
from terraseek.db.repositories import SiteRepository
from terraseek.schemas.common import EvidenceStatus
from terraseek.schemas.search import SimilarRetrievalItem, SimilarRetrievalResponse
from terraseek.models.adapters import get_embedding_provider
from terraseek.retrieval.qdrant_client import get_vector_manager

router = APIRouter(prefix="/retrieval", tags=["Vector Retrieval"])


@router.post("/similar", response_model=SimilarRetrievalResponse)
async def find_similar_places(
    image: Optional[UploadFile] = File(None),
    site_id: Optional[str] = Form(None),
    limit: int = Form(5),
    db: Session = Depends(get_db),
):
    """Retrieve sites and observations visually or semantically similar to an input image or site."""
    embedder = get_embedding_provider()
    vector_mgr = get_vector_manager()
    site_repo = SiteRepository(db)

    query_ref = "input_image"
    if image:
        content = await image.read()
        query_vec = embedder.embed_image(content)
        query_ref = image.filename or "uploaded_image"
    elif site_id:
        query_vec = embedder.embed_text(f"site {site_id}")
        query_ref = f"site:{site_id}"
    else:
        query_vec = embedder.embed_text("satellite optical surface reference")
        query_ref = "default_reference"

    q_results = vector_mgr.search_similar(query_vec, limit=limit)
    items = []

    # Map retrieved results
    all_sites = site_repo.list_all(limit=10)
    for idx, hit in enumerate(q_results):
        payload = hit.get("payload", {})
        s_id = payload.get("site_id")
        site = site_repo.get_by_id(s_id) if s_id else (all_sites[idx % len(all_sites)] if all_sites else None)

        if site:
            items.append(
                SimilarRetrievalItem(
                    site_id=site.id,
                    site_name=site.name,
                    location_name=site.location_name,
                    similarity_score=round(float(hit.get("score", 0.85)), 3),
                    acquisition_date="January 2025",
                    thumbnail_url=f"/api/v1/sites/{site.id}/thumbnail/after",
                    latitude=site.latitude,
                    longitude=site.longitude,
                    evidence_status=EvidenceStatus.SUPPORTED,
                    model_provider="DemoEmbeddingProvider",
                )
            )

    # If empty, provide top catalog sites with deterministic similarity scores
    if not items and all_sites:
        for s in all_sites[:limit]:
            items.append(
                SimilarRetrievalItem(
                    site_id=s.id,
                    site_name=s.name,
                    location_name=s.location_name,
                    similarity_score=0.88,
                    acquisition_date="January 2025",
                    thumbnail_url=f"/api/v1/sites/{s.id}/thumbnail/after",
                    latitude=s.latitude,
                    longitude=s.longitude,
                    evidence_status=EvidenceStatus.SUPPORTED,
                    model_provider="DemoEmbeddingProvider",
                )
            )

    return SimilarRetrievalResponse(
        query_reference=query_ref,
        model_provider="DemoEmbeddingProvider",
        is_demo=True,
        total=len(items),
        results=items,
    )
