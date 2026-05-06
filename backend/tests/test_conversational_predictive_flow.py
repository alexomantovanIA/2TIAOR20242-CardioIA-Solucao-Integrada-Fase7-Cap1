import pytest

from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
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
