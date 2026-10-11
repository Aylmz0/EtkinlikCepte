"""H1.2 skeleton contract tests: /health and /openapi.json stay 200."""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_ok() -> None:
    """GET /health returns ok plus the app version."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_openapi_v1_served() -> None:
    """GET /openapi.json returns an OpenAPI 3.1 document (H1.2 exit gate)."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["openapi"].startswith("3.1.")
