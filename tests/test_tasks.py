from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_get_task_status():
    response = client.get("/api/v1/tasks/test-task-123")
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "test-task-123"
    assert data["status"] == "completed"
    assert data["progress"] == 100

def test_get_task_status_not_found():
    response = client.get("/api/v1/tasks/invalid")
    assert response.status_code == 404

def test_get_task_progress_widget():
    response = client.get("/api/v1/tasks/test-task-123/widget")
    assert response.status_code == 200
    assert "Async Task ID" in response.text
    assert "hx-get" in response.text
