from fastapi.testclient import TestClient

from src.main import app
from src.services.nlp import NLPTokenizer
from src.services.taxonomy import TaxonomyCategorizer
from src.services.weighting import WeightingMatrix

client = TestClient(app)

def test_nlp_tokenizer_and_extraction():
    text = "We are looking for a Senior Python Developer with FastAPI and 5+ years of experience in PostgreSQL and Docker."
    tokens = NLPTokenizer.tokenize(text)
    assert "python" in tokens
    assert "fastapi" in tokens

    skills = NLPTokenizer.extract_skills(text)
    assert "python" in skills
    assert "fastapi" in skills
    assert "postgresql" in skills

    exp = NLPTokenizer.extract_experience_years(text)
    assert exp == 5.0

    edu = NLPTokenizer.extract_education("Bachelor of Science in Computer Science")
    assert edu == "Bachelor's Degree"

def test_taxonomy_and_weighting():
    taxonomy = TaxonomyCategorizer.extract_full_taxonomy("Python, FastAPI, communication, teamwork, Master's degree, 4 years experience")
    assert "python" in taxonomy["hard_skills"]
    assert "communication" in taxonomy["soft_skills"]
    assert taxonomy["education_level"] == "Master's Degree"
    assert taxonomy["experience_years"] == 4.0

    composite = WeightingMatrix.calculate_composite_score(80.0, 90.0, 70.0)
    assert 0.0 <= composite <= 100.0

def test_job_crud_api():
    response = client.post("/api/v1/jobs/", json={
        "title": "Backend Engineer",
        "department": "Engineering",
        "description": "Looking for Python and FastAPI developer with 3 years experience.",
        "required_skills": "Python, FastAPI",
        "min_experience_years": 3.0
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Backend Engineer"
    job_id = data["id"]

    # List jobs
    get_all = client.get("/api/v1/jobs/")
    assert get_all.status_code == 200
    assert len(get_all.json()) >= 1

    # Get job by id
    get_one = client.get(f"/api/v1/jobs/{job_id}")
    assert get_one.status_code == 200
    assert get_one.json()["id"] == job_id
