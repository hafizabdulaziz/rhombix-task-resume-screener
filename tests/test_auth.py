import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from src.main import app
from src.core.security import require_role, create_access_token

client = TestClient(app)

@app.get("/api/v1/test-rbac-admin", dependencies=[Depends(require_role(["Admin"]))])
async def admin_only_route():
    return {"message": "Welcome Admin"}

def test_auth_register_login_profile_logout():
    # Register user
    reg_response = client.post(
        "/api/v1/auth/register",
        json={"email": "profiletest@rhombix.com", "password": "SecurePassword123!", "role": "Recruiter"}
    )
    assert reg_response.status_code == 201

    # Login user
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "profiletest@rhombix.com", "password": "SecurePassword123!"}
    )
    assert login_response.status_code == 200
    data = login_response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    # Test get profile
    profile_response = client.get(
        "/api/v1/auth/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "profiletest@rhombix.com"
    assert profile_response.json()["role"] == "Recruiter"

    # Test logout
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert logout_response.status_code == 200

    # Test refresh token
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

def test_rbac_authorization():
    viewer_token = create_access_token({"sub": "viewer@rhombix.com", "role": "Viewer"})
    response = client.get(
        "/api/v1/test-rbac-admin",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403

    admin_token = create_access_token({"sub": "admin@rhombix.com", "role": "Admin"})
    response = client.get(
        "/api/v1/test-rbac-admin",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Admin"
