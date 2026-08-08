from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, lifespan="off")


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert body["status"] == "healthy"
