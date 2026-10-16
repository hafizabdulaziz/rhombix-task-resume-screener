import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_screener_lifecycle():
    # 1. Create Job Description via API
    job_resp = client.post(
        "/api/v1/jobs/",
        json={
            "title": "Senior AI Engineer",
            "department": "AI Lab",
            "description": "Looking for Python, FastAPI, and Machine Learning expert with 5 years experience.",
            "required_skills": "Python, FastAPI, Machine Learning, Docker",
            "min_experience_years": 5.0
        }
    )
    assert job_resp.status_code == 201
    job_id = job_resp.json()["id"]

    # 2. Test ranking when no candidates exist
    rank_resp = client.post("/api/v1/screener/rank", json={"job_id": job_id})
    assert rank_resp.status_code == 200
    assert rank_resp.json() == []

    # 3. Test get rankings for job
    results_resp = client.get(f"/api/v1/screener/results/{job_id}")
    assert results_resp.status_code == 200
    assert results_resp.json() == []

def test_candidate_breakdown_404():
    resp = client.get("/api/v1/screener/candidate/99999/breakdown")
    assert resp.status_code == 404
