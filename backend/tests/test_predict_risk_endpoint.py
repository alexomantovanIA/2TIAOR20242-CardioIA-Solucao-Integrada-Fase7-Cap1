import pytest

from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_predict_risk_missing_fields(client):
    response = client.post("/api/predict-risk", json={"idade": 50})
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data


def test_predict_risk_ml_only_ok(client):
    response = client.post(
        "/api/predict-risk",
        json={
            "idade": 50,
            "freq_cardiaca": 80,
            "spo2": 97.0,
            "carga_sistema": 0.3,
            "disponibilidade_recursos": 0.7,
            "mode": "ml_only",
        },
    )
    assert response.status_code == 200, response.get_data(as_text=True)
    data = response.get_json()
    assert data.get("urgency_detected") is False
    assert data.get("mode") == "ml_only"
    rec = data.get("recommendation") or {}
    assert "probability" in rec
    assert "risk_classification" in rec
    assert "suggested_protocols" in rec
    assert "disclaimer" in rec
    assert rec.get("governance", {}).get("coherence_ok") is True


def test_predict_risk_context_urgency_blocks_ml(client):
    response = client.post(
        "/api/predict-risk",
        json={
            "idade": 50,
            "freq_cardiaca": 80,
            "spo2": 97.0,
            "carga_sistema": 0.3,
            "disponibilidade_recursos": 0.7,
            "mode": "ml_only",
            "context_message": "Estou com dor intensa no peito e falta de ar intensa.",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("urgency_detected") is True
    assert data.get("recommendation") is None
    assert "urgency_message" in data
