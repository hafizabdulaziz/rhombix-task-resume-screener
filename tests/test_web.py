from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_web_master_portal():
    response = client.get("/")
    assert response.status_code == 200
    assert "Master Recruitment Intelligence Portal" in response.text

def test_web_jobs_redirect():
    response = client.get("/jobs", follow_redirects=False)
    assert response.status_code == 303
    assert "/?tab=jobs" in response.headers["location"]

def test_web_upload_redirect():
    response = client.get("/upload", follow_redirects=False)
    assert response.status_code == 303
    assert "/?tab=upload" in response.headers["location"]
