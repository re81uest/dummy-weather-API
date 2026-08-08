from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    with patch("app.main.init_db", new_callable=AsyncMock):
        client = TestClient(app)
        response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert body["status"] == "healthy"
