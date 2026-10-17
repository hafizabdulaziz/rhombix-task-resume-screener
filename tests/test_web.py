from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_web_silver_enterprise_portal():
    response = client.get("/")
    assert response.status_code == 200
    assert "Premium Silver Enterprise Portal" in response.text
