import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.matching import ResumeMatcher
from src.services.export import ReportExporter

client = TestClient(app)

def test_e2e_screening_flow():
    # 1. Test Matching & Scoring Logic directly
    score_data = ResumeMatcher.compute_composite_score(
        job_description="Seeking Python Developer with FastAPI and Postgres",
        resume_text="Senior Python Developer with 6 years experience in FastAPI, Postgres, and Docker.",
        required_skills=["Python", "FastAPI", "Postgres"],
        candidate_skills=["python", "fastapi", "postgresql", "docker"],
        required_experience_years=3.0,
        candidate_experience_years=6.0
    )
    assert score_data["composite_score"] > 80.0
    assert score_data["skill_match_score"] == 100.0

    # 2. Test Report Export Generation (Excel & CSV)
    mock_results = [{
        "candidate_name": "Alice Smith",
        "candidate_email": "alice@example.com",
        "composite_score": 92.5,
        "skill_match_score": 100.0,
        "experience_match_score": 100.0,
        "semantic_score": 85.0,
        "status": "shortlisted",
        "skill_scores": [{"skill_name": "python", "is_matched": True, "match_type": "exact"}]
    }]
    
    excel_bytes = ReportExporter.generate_excel_report("Python Dev", mock_results)
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 0

    csv_str = ReportExporter.generate_csv_report(mock_results)
    assert isinstance(csv_str, str)
    assert "Alice Smith" in csv_str

    # 3. Test Web Endpoints Health & Pages
    resp_dash = client.get("/", follow_redirects=False)
    assert resp_dash.status_code == 303
    assert resp_dash.headers["location"] == "/docs"

    resp_docs = client.get("/docs")
    assert resp_docs.status_code == 200
