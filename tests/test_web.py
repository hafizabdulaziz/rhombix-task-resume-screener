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
