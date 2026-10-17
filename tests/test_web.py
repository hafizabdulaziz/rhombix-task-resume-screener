from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_web_dashboard():
    response = client.get("/")
    assert response.status_code == 200
    assert "Recruitment Intelligence Dashboard" in response.text

def test_web_jobs_page():
    response = client.get("/jobs")
    assert response.status_code == 200
    assert "Job Descriptions & Vacancies" in response.text

def test_web_upload_page():
    response = client.get("/upload")
    assert response.status_code == 200
    assert "Batch Resume Upload & Parsing" in response.text

def test_web_upload_invalid_file():
    # Test uploading an invalid file format (e.g. invalid signature)
    bad_bytes = b"NOTAPDFCONTENT"
    files = [("files", ("test_resume.pdf", bad_bytes, "application/pdf"))]
    response = client.post("/upload", files=files, follow_redirects=False)
    assert response.status_code == 400
