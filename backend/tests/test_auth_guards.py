import pytest

from backend.app import create_app
from backend.tests.auth_token import build_test_jwt


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["AUTH_ENABLED"] = True
    app.config["ENTRA_TENANT_ID"] = "fiap-tenant"
    app.config["ENTRA_AUDIENCE"] = "cardioia-api"
    app.config["ENTRA_ISSUER"] = "https://login.microsoftonline.com/fiap-tenant/v2.0"
    with app.test_client() as client:
        yield client


def test_api_without_token_returns_401(client):
    response = client.post("/api/full-analysis", json={"message": "teste"})
    assert response.status_code == 401


def test_api_with_invalid_token_returns_401(client):
    response = client.post(
        "/api/full-analysis",
        headers={"Authorization": "Bearer token-invalido"},
        json={"message": "teste"},
    )
    assert response.status_code == 401


def test_health_without_token_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_dashboard_with_valid_token_returns_200(client):
    token = build_test_jwt()
    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
