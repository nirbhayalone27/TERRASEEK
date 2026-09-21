"""Unit tests for Evidence Policy Engine."""

from terraseek.evidence.engine import EvidencePolicyEngine
from terraseek.schemas.common import EvidenceStatus
from terraseek.schemas.evidence import EvidenceItem, EvidenceType


def test_policy_all_supported():
    item = EvidenceItem(
        id="1",
        evidence_type=EvidenceType.RETRIEVAL,
        title="Candidate",
        description="Found",
        status=EvidenceStatus.SUPPORTED,
        source="catalog",
        method="vector",
    )
    passport = EvidencePolicyEngine.evaluate(
        site_id="s1",
        query="new buildings near river",
        candidate_found=True,
        spatial_status=EvidenceStatus.SUPPORTED,
        temporal_status=EvidenceStatus.SUPPORTED,
        change_status=EvidenceStatus.SUPPORTED,
        items=[item],
    )
    assert passport.status == EvidenceStatus.SUPPORTED


def test_policy_no_match():
    passport = EvidencePolicyEngine.evaluate(
        site_id="s1",
        query="new airport",
        candidate_found=False,
        spatial_status=EvidenceStatus.NO_MATCH,
        temporal_status=EvidenceStatus.SUPPORTED,
        change_status=EvidenceStatus.NO_MATCH,
        items=[],
    )
    assert passport.status == EvidenceStatus.NO_MATCH


def test_policy_insufficient_evidence():
    passport = EvidencePolicyEngine.evaluate(
        site_id="s1",
        query="new construction without baseline",
        candidate_found=True,
        spatial_status=EvidenceStatus.SUPPORTED,
        temporal_status=EvidenceStatus.INSUFFICIENT_EVIDENCE,
        change_status=EvidenceStatus.SUPPORTED,
        items=[],
    )
    assert passport.status == EvidenceStatus.INSUFFICIENT_EVIDENCE


def test_policy_needs_review():
    passport = EvidencePolicyEngine.evaluate(
        site_id="s1",
        query="borderline construction",
        candidate_found=True,
        spatial_status=EvidenceStatus.SUPPORTED,
        temporal_status=EvidenceStatus.SUPPORTED,
        change_status=EvidenceStatus.NEEDS_REVIEW,
        items=[],
    )
    assert passport.status == EvidenceStatus.NEEDS_REVIEW
