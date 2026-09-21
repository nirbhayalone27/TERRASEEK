"""Integration tests for FastAPI endpoints."""

import pytest
from starlette.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_ready_endpoint():
    res = client.get("/api/v1/ready")
    assert res.status_code == 200
    assert "status" in res.json()


def test_list_sites():
    res = client.get("/api/v1/sites")
    assert res.status_code == 200
    sites = res.json()
    assert isinstance(sites, list)
    assert len(sites) >= 5


def test_get_site_01():
    res = client.get("/api/v1/sites/site-01")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "site-01"
    assert "Riverside Development" in data["name"]


def test_search_endpoint():
    res = client.post("/api/v1/search", json={"query": "new buildings near a river"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUPPORTED"
    assert len(data["results"]) > 0


def test_search_no_match_airport():
    res = client.post("/api/v1/search", json={"query": "new airport"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "NO_MATCH"
    assert data["total_results"] == 0


def test_search_insufficient_evidence():
    res = client.post(
        "/api/v1/search",
        json={"query": "new construction where earlier imagery is unavailable"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "INSUFFICIENT_EVIDENCE"


def test_change_analyze_endpoint():
    res = client.post(
        "/api/v1/change/analyze",
        json={"site_id": "site-01", "change_types": ["BUILDING"]},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["site_id"] == "site-01"
    assert "changes" in data


def test_review_queue_and_decision():
    # Fetch queue
    res = client.get("/api/v1/review/queue")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_generate_report():
    res = client.post(
        "/api/v1/reports",
        json={"site_id": "site-01", "query": "new buildings near a river"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["site_id"] == "site-01"
    assert "conclusion" in data
