"""Unit tests for spatial and temporal reasoning engines."""

from datetime import date
from terraseek.spatial.engine import SpatialEngine
from terraseek.temporal.engine import TemporalEngine
from terraseek.schemas.common import EvidenceStatus
from terraseek.schemas.temporal import TemporalObservation


def test_spatial_distance_and_buffer():
    point1 = {"type": "Point", "coordinates": [16.3738, 48.2082]}
    # Line ~200m away
    line1 = {
        "type": "LineString",
        "coordinates": [[16.3710, 48.2080], [16.3760, 48.2085]],
    }
    dist = SpatialEngine.calculate_distance_meters(point1, line1)
    assert dist > 0.0

    features = [{"name": "Test River", "geometry": line1}]
    chk = SpatialEngine.verify_within_distance(point1, features, max_distance_meters=500.0, target_type="river")
    assert chk.satisfied is True


def test_temporal_continuity():
    obs = [
        TemporalObservation(id="1", site_id="s1", acquisition_date=date(2024, 3, 1), sensor="S2", usable=True),
        TemporalObservation(id="2", site_id="s1", acquisition_date=date(2024, 6, 1), sensor="S2", usable=True),
        TemporalObservation(id="3", site_id="s1", acquisition_date=date(2024, 9, 1), sensor="S2", usable=True),
        TemporalObservation(id="4", site_id="s1", acquisition_date=date(2025, 1, 1), sensor="S2", usable=True),
    ]
    res = TemporalEngine.verify_timeline(obs, min_required=2)
    assert res.status == EvidenceStatus.SUPPORTED
    assert res.usable_observations_count == 4
    assert res.earliest_supported_observation == date(2024, 3, 1)


def test_temporal_insufficient_evidence():
    # Only 1 observation -> cannot verify change
    obs = [
        TemporalObservation(id="1", site_id="s1", acquisition_date=date(2025, 1, 1), sensor="S2", usable=True)
    ]
    res = TemporalEngine.verify_timeline(obs, min_required=2)
    assert res.status == EvidenceStatus.INSUFFICIENT_EVIDENCE
    assert res.has_after_observation is False
