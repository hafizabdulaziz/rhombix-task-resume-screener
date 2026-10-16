import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.nlp import NLPTokenizer

client = TestClient(app)

def test_nlp_tokenizer():
    text = "We are looking for a Senior Python Developer with 5+ years of experience in FastAPI, PostgreSQL, and Docker. Master's degree preferred."
    skills = NLPTokenizer.extract_skills(text)
    assert "python" in skills
    assert "fastapi" in skills
    assert "postgresql" in skills
    assert "docker" in skills

    exp = NLPTokenizer.extract_experience_years(text)
    assert exp == 5.0

    edu = NLPTokenizer.extract_education(text)
    assert "Master" in edu

def test_create_and_list_job():
    response = client.post(
        "/api/v1/jobs/",
        json={
            "title": "Backend Engineer",
            "department": "Engineering",
            "description": "Looking for Python, FastAPI and SQL developer with 3 years of experience.",
            "min_experience_years": 3.0
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Backend Engineer"
    assert "python" in data["required_skills"]
    assert data["min_experience_years"] == 3.0
    job_id = data["id"]

    # Test get job list
    response_list = client.get("/api/v1/jobs/")
    assert response_list.status_code == 200
    jobs = response_list.json()
    assert len(jobs) >= 1

    # Test get single job
    response_single = client.get(f"/api/v1/jobs/{job_id}")
    assert response_single.status_code == 200
    assert response_single.json()["id"] == job_id
