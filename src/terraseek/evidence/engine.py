"""Evidence Engine and Policy Evaluator for Truth-in-AI certification."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from terraseek.schemas.common import EvidenceStatus
from terraseek.schemas.evidence import EvidenceItem, EvidencePassport, EvidenceType


class EvidencePolicyEngine:
    """Evaluates multi-source evidence and establishes final truth decision."""

    @staticmethod
    def evaluate(
        site_id: str,
        query: str,
        candidate_found: bool,
        spatial_status: EvidenceStatus,
        temporal_status: EvidenceStatus,
        change_status: EvidenceStatus,
        items: List[EvidenceItem],
        spatial_summary: str = "",
        temporal_summary: str = "",
        change_summary: str = "",
        model_provenance: Optional[Dict[str, Any]] = None,
        limitations: Optional[List[str]] = None,
    ) -> EvidencePassport:
        # Rule 1: If no candidate exists in the catalog matching query
        if not candidate_found:
            return EvidencePassport(
                id=str(uuid.uuid4()),
                site_id=site_id,
                query=query,
                status=EvidenceStatus.NO_MATCH,
                items=items,
                spatial_summary="No candidate site found matching search criteria.",
                temporal_summary="N/A",
                change_summary="N/A",
                model_provenance=model_provenance or {},
                limitations=limitations or ["Catalog contains no matching geographic or semantic candidates."],
                needs_review_reason=None,
            )

        # Rule 2: If required temporal evidence is missing (e.g. no baseline imagery)
        if temporal_status == EvidenceStatus.INSUFFICIENT_EVIDENCE:
            return EvidencePassport(
                id=str(uuid.uuid4()),
                site_id=site_id,
                query=query,
                status=EvidenceStatus.INSUFFICIENT_EVIDENCE,
                items=items,
                spatial_summary=spatial_summary,
                temporal_summary=temporal_summary,
                change_summary="Cannot verify change without sufficient historical baseline imagery.",
                model_provenance=model_provenance or {},
                limitations=limitations or ["Missing required baseline observation prior to reported change."],
                needs_review_reason="Historical observation gaps prevent definitive change determination.",
            )

        # Rule 3: If spatial constraint failed
        if spatial_status == EvidenceStatus.NO_MATCH:
            return EvidencePassport(
                id=str(uuid.uuid4()),
                site_id=site_id,
                query=query,
                status=EvidenceStatus.NO_MATCH,
                items=items,
                spatial_summary=spatial_summary,
                temporal_summary=temporal_summary,
                change_summary=change_summary,
                model_provenance=model_provenance or {},
                limitations=limitations or ["Candidate violates mandatory spatial constraint."],
                needs_review_reason=None,
            )

        # Rule 4: If any component flagged for human review
        if (
            spatial_status == EvidenceStatus.NEEDS_REVIEW
            or temporal_status == EvidenceStatus.NEEDS_REVIEW
            or change_status == EvidenceStatus.NEEDS_REVIEW
        ):
            reasons = []
            if spatial_status == EvidenceStatus.NEEDS_REVIEW:
                reasons.append("Spatial distance borderline or ambiguous.")
            if temporal_status == EvidenceStatus.NEEDS_REVIEW:
                reasons.append("Extended gap between satellite passes.")
            if change_status == EvidenceStatus.NEEDS_REVIEW:
                reasons.append("Change spectral contrast near detection threshold.")

            return EvidencePassport(
                id=str(uuid.uuid4()),
                site_id=site_id,
                query=query,
                status=EvidenceStatus.NEEDS_REVIEW,
                items=items,
                spatial_summary=spatial_summary,
                temporal_summary=temporal_summary,
                change_summary=change_summary,
                model_provenance=model_provenance or {},
                limitations=limitations or [],
                needs_review_reason="; ".join(reasons),
            )

        # Rule 5: Fully supported
        if (
            spatial_status == EvidenceStatus.SUPPORTED
            and temporal_status == EvidenceStatus.SUPPORTED
            and change_status == EvidenceStatus.SUPPORTED
        ):
            return EvidencePassport(
                id=str(uuid.uuid4()),
                site_id=site_id,
                query=query,
                status=EvidenceStatus.SUPPORTED,
                items=items,
                spatial_summary=spatial_summary,
                temporal_summary=temporal_summary,
                change_summary=change_summary,
                model_provenance=model_provenance or {},
                limitations=limitations or ["Results calibrated against demo offline dataset."],
                needs_review_reason=None,
            )

        # Default fallback: Insufficient evidence
        return EvidencePassport(
            id=str(uuid.uuid4()),
            site_id=site_id,
            query=query,
            status=EvidenceStatus.INSUFFICIENT_EVIDENCE,
            items=items,
            spatial_summary=spatial_summary,
            temporal_summary=temporal_summary,
            change_summary=change_summary,
            model_provenance=model_provenance or {},
            limitations=limitations or ["Incomplete evidence set."],
            needs_review_reason="Evidence incomplete across required domains.",
        )
