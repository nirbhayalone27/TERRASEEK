"""End-to-End workflow tests verifying the complete analytical lifecycle."""

import pytest
from starlette.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_complete_end_to_end_investigation_flow():
    # 1. Search Query: "new buildings near a river"
    search_res = client.post("/api/v1/search", json={"query": "new buildings near a river"})
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert search_data["status"] == "SUPPORTED"
    assert search_data["total_results"] > 0

    top_result = search_data["results"][0]
    site_id = top_result["site_id"]
    evidence_id = top_result["evidence_id"]
    assert site_id == "site-01"
    assert top_result["status"] == "SUPPORTED"

    # 2. Select Site: GET /api/v1/sites/site-01
    site_res = client.get(f"/api/v1/sites/{site_id}")
    assert site_res.status_code == 200
    site_data = site_res.json()
    assert site_data["id"] == "site-01"
    assert "river" in site_data["spatial_verification_summary"].lower()

    # 3. View Observations: GET /api/v1/sites/site-01/observations
    obs_res = client.get(f"/api/v1/sites/{site_id}/observations")
    assert obs_res.status_code == 200
    obs_list = obs_res.json()
    assert len(obs_list) >= 2

    # 4. View Evidence: GET /api/v1/evidence/{evidence_id}
    if evidence_id:
        ev_res = client.get(f"/api/v1/evidence/{evidence_id}")
        assert ev_res.status_code == 200
        ev_data = ev_res.json()
        assert ev_data["status"] == "SUPPORTED"
        assert len(ev_data["items"]) > 0

    # 5. Generate Report: POST /api/v1/reports
    rep_res = client.post(
        "/api/v1/reports",
        json={"site_id": site_id, "query": "new buildings near a river"},
    )
    assert rep_res.status_code == 200
    rep_data = rep_res.json()
    assert rep_data["status"] == "SUPPORTED"
    assert "SUPPORTED" in rep_data["conclusion"]


def test_edge_case_unmatchable_airport():
    res = client.post("/api/v1/search", json={"query": "new airport"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "NO_MATCH"
    assert data["total_results"] == 0


def test_edge_case_missing_baseline_imagery():
    res = client.post(
        "/api/v1/search",
        json={"query": "new construction where earlier imagery is unavailable"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "INSUFFICIENT_EVIDENCE"
