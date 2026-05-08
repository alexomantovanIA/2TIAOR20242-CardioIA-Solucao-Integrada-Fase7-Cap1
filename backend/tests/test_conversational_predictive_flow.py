import pytest

from backend.app import create_app
from backend.tests.auth_token import build_test_jwt


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["AUTH_ENABLED"] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_auth():
    app = create_app()
    app.config["TESTING"] = True
    app.config["AUTH_ENABLED"] = True
    app.config["ENTRA_TENANT_ID"] = "fiap-tenant"
    app.config["ENTRA_AUDIENCE"] = "cardioia-api"
    app.config["ENTRA_ISSUER"] = "https://login.microsoftonline.com/fiap-tenant/v2.0"
    with app.test_client() as client:
        yield client


def test_conversational_flow_chat_to_predictive_pipeline(client):
    chat_response = client.post(
        "/api/chat",
        json={
            "message": (
                "Tenho 65 anos, FC 115 bpm, SpO2 91.5, "
                "carga do sistema 0.85 e disponibilidade de recursos 0.2."
            )
        },
    )
    assert chat_response.status_code == 200
    chat_data = chat_response.get_json()

    suggestion = chat_data.get("predictive_suggestion")
    assert suggestion is not None
    assert suggestion.get("ready_for_predict") is True
    payload = suggestion.get("patient_payload")
    assert isinstance(payload, dict)

    predictive_body = {
        **payload,
        "mode": "ml_only",
        "context_message": "Fluxo conversacional integrado para analise preditiva.",
    }
    predict_response = client.post("/api/predict-risk", json=predictive_body)
    assert predict_response.status_code == 200, predict_response.get_data(as_text=True)
    predict_data = predict_response.get_json()

    assert predict_data.get("urgency_detected") is False
    assert predict_data.get("mode") == "ml_only"
    recommendation = predict_data.get("recommendation") or {}
    assert "probability" in recommendation
    assert "risk_classification" in recommendation
    assert "suggested_protocols" in recommendation
    assert recommendation.get("governance", {}).get("coherence_ok") is True


def test_full_analysis_authenticated_returns_200(client_auth):
    token = build_test_jwt()
    response = client_auth.post(
        "/api/full-analysis",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "message": "Tenho palpitacoes leves ha dois dias.",
            "patient": {
                "idade": 50,
                "freq_cardiaca": 80,
                "spo2": 97.0,
                "carga_sistema": 0.3,
                "disponibilidade_recursos": 0.7,
            },
        },
    )
    assert response.status_code == 200
