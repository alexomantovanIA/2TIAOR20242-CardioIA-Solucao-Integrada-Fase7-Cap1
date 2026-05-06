import pytest
from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_has_status_ok(client):
    response = client.get("/health")
    data = response.get_json()
    assert data["status"] == "ok"


def test_health_has_mode_field(client):
    response = client.get("/health")
    data = response.get_json()
    assert "mode" in data
    assert data["mode"] in ("watson_assistant", "fallback_local")


def test_health_has_watson_connected_field(client):
    response = client.get("/health")
    data = response.get_json()
    assert "watson_connected" in data
    assert isinstance(data["watson_connected"], bool)


def test_health_includes_fase6_prediction_readiness(client):
    response = client.get("/health")
    data = response.get_json()
    assert "fase6_prediction" in data
    f6 = data["fase6_prediction"]
    assert "predict_risk_ready" in f6
    assert "model_file_present" in f6
    assert "protocols_file_present" in f6
    assert "openai_api_configured" in f6
    assert "openai_agents_sdk_importable" in f6
    assert "multiagent_full_pipeline_ready" in f6
    assert isinstance(f6["predict_risk_ready"], bool)
