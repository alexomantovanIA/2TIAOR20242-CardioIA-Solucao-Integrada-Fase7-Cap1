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


def test_tenant_mismatch_returns_401(client):
    wrong_tenant_token = build_test_jwt(tid="outro-tenant")
    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {wrong_tenant_token}"},
    )
    assert response.status_code == 401
