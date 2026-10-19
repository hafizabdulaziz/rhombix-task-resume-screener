from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_root_redirects_to_swagger():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/docs"

def test_silver_swagger_docs_accessible():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Silver Enterprise UI" in response.text or "swagger" in response.text.lower()

def test_dashboard_ui_endpoint():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "html" in response.headers.get("content-type", "").lower()

def test_jobs_ui_endpoint():
    response = client.get("/jobs-ui")
    assert response.status_code == 200
    assert "html" in response.headers.get("content-type", "").lower()

def test_upload_ui_endpoint():
    response = client.get("/upload-ui")
    assert response.status_code == 200
    assert "html" in response.headers.get("content-type", "").lower()

