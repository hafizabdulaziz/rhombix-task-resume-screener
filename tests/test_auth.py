import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from src.main import app
from src.core.security import require_role, create_access_token

client = TestClient(app)

# Add a test protected route for RBAC verification
@app.get("/api/v1/test-rbac-admin", dependencies=[Depends(require_role(["Admin"]))])
async def admin_only_route():
    return {"message": "Welcome Admin"}

def test_rbac_authorization():
    # Create token with Viewer role
    viewer_token = create_access_token({"sub": "viewer@rhombix.com", "role": "Viewer"})
    
    # Try accessing admin route with Viewer token -> should get 403 Forbidden
    response = client.get(
        "/api/v1/test-rbac-admin",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403

    # Create token with Admin role
    admin_token = create_access_token({"sub": "admin@rhombix.com", "role": "Admin"})
    
    # Try accessing admin route with Admin token -> should get 200 OK
    response = client.get(
        "/api/v1/test-rbac-admin",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Admin"
