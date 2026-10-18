import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_security_headers():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("Strict-Transport-Security") is not None
    assert response.headers.get("Content-Security-Policy") is not None
