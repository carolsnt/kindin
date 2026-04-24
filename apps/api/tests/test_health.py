"""Test the health check endpoint."""
from fastapi.testclient import TestClient

from kindin_api.main import app

client = TestClient(app)


def test_health():
    """GET /health should return 200 and status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
