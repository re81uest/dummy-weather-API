from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with (
        patch("app.main.init_db", new_callable=AsyncMock),
        TestClient(app) as client,
    ):
        yield client


def test_health_does_not_touch_database(client: TestClient) -> None:
    session_local = MagicMock()

    with patch("app.middleware.SessionLocal", session_local):
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    session_local.assert_not_called()
