"""Fault tolerance tests for failure modes and error contracts."""

import pytest
from starlette.testclient import TestClient
from apps.api.main import app
from terraseek.quality.checker import QualityChecker
from terraseek.spatial.engine import SpatialEngine
from terraseek.models.adapters import GeoRSCLIPEmbeddingModel, UNetResNet34ChangeModel

client = TestClient(app)


def test_missing_file_quality_check():
    report = QualityChecker.inspect_raster("non_existent_file.tif")
    assert report.is_usable is False
    assert report.quality_score == 0.0
    assert "File does not exist" in report.issues


def test_unloaded_model_raises_explicit_error():
    model = GeoRSCLIPEmbeddingModel(model_weights_path=None)
    with pytest.raises(RuntimeError) as exc_info:
        model.embed_text("test query")
    assert "weights are not loaded" in str(exc_info.value)


def test_invalid_geometry_fails_safely():
    with pytest.raises(ValueError):
        SpatialEngine.parse_geometry({"type": "InvalidType", "coordinates": "invalid"})


def test_empty_search_query_returns_400():
    res = client.post("/api/v1/search", json={"query": "   "})
    assert res.status_code == 400


def test_invalid_site_id_returns_404():
    res = client.get("/api/v1/sites/invalid-site-id-999")
    assert res.status_code == 404
