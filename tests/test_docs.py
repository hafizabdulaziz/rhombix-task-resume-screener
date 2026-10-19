from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text.lower()

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (302, 303, 307)
    assert response.headers["location"] == "/docs"
