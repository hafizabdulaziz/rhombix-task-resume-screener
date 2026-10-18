import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_auth_register_and_login():
    # Register user
    reg_response = client.post(
        "/api/v1/auth/register",
        json={"email": "testhr@rhombix.com", "password": "SecurePassword123!", "role": "Admin"}
    )
    assert reg_response.status_code == 201
    assert reg_response.json()["email"] == "testhr@rhombix.com"

    # Login user
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "testhr@rhombix.com", "password": "SecurePassword123!"}
    )
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

    # Test refresh token
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": data["refresh_token"]}
    )
    assert refresh_response.status_code == 200
    refresh_data = refresh_response.json()
    assert "access_token" in refresh_data
