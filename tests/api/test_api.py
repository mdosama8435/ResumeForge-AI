from fastapi.testclient import TestClient
from src.api.setup import create_app

client = TestClient(create_app())

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "request_id" in data
