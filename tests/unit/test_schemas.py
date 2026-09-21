"""Unit tests for schemas and enums."""

import pytest
from datetime import date
from terraseek.schemas.common import EvidenceStatus, ChangeType, JobStatus, ModelTier
from terraseek.schemas.search import SearchRequest, MissionIntent
from terraseek.schemas.spatial import SpatialConstraint
from terraseek.schemas.temporal import TemporalObservation


def test_evidence_status_enum():
    assert EvidenceStatus.SUPPORTED == "SUPPORTED"
    assert EvidenceStatus.NEEDS_REVIEW == "NEEDS_REVIEW"
    assert EvidenceStatus.INSUFFICIENT_EVIDENCE == "INSUFFICIENT_EVIDENCE"
    assert EvidenceStatus.NO_MATCH == "NO_MATCH"


def test_search_request_validation():
    req = SearchRequest(query="new buildings near a river", limit=5)
    assert req.query == "new buildings near a river"
    assert req.limit == 5


def test_spatial_constraint():
    sc = SpatialConstraint(feature_type="river", relation="within", distance_meters=500.0)
    assert sc.feature_type == "river"
    assert sc.distance_meters == 500.0


def test_temporal_observation():
    obs = TemporalObservation(
        id="obs-01",
        site_id="site-01",
        acquisition_date=date(2024, 3, 15),
        sensor="Sentinel-2A",
        usable=True,
    )
    assert obs.sensor == "Sentinel-2A"
    assert obs.usable is True
