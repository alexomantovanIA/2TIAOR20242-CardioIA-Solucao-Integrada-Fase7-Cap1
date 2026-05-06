import pytest

from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_iot_ingest_accepts_valid_reading(client):
    response = client.post(
        "/api/iot/ingest",
        json={
            "device_id": "esp32-demo",
            "heart_rate": 82,
            "temperature": 36.7,
            "spo2": 98,
            "timestamp": "2026-05-03T15:00:00Z",
        },
    )

    assert response.status_code == 201, response.get_data(as_text=True)
    data = response.get_json()
    assert data["accepted"] is True
    assert data["reading"]["status"] == "normal"
    assert data["patient_payload"]["freq_cardiaca"] == 82
    assert data["disclaimer"]


def test_iot_ingest_rejects_missing_fields(client):
    response = client.post("/api/iot/ingest", json={"device_id": "esp32-demo"})
    assert response.status_code == 400
    assert "message" in response.get_json()


def test_dashboard_summary_uses_latest_iot_reading(client):
    client.post(
        "/api/iot/ingest",
        json={
            "device_id": "esp32-demo",
            "heart_rate": 118,
            "temperature": 37.9,
            "spo2": 94,
            "timestamp": "2026-05-03T15:01:00Z",
        },
    )

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200, response.get_data(as_text=True)
    data = response.get_json()
    assert data["latest_iot_reading"]["status"] == "atencao"
    assert data["patient_payload"]["freq_cardiaca"] == 118
    assert data["risk_current"] in ("baixo", "médio", "alto", "atencao")
    assert data["disclaimer"]


def test_patient_latest_returns_derived_patient(client):
    client.post(
        "/api/iot/ingest",
        json={
            "device_id": "esp32-demo",
            "heart_rate": 72,
            "temperature": 36.5,
            "spo2": 97,
            "timestamp": "2026-05-03T15:02:00Z",
        },
    )

    response = client.get("/api/patient/latest")

    assert response.status_code == 200
    data = response.get_json()
    assert data["patient"]["freq_cardiaca"] == 72
    assert data["latest_iot_reading"]["device_id"] == "esp32-demo"


def test_full_analysis_combines_chat_and_prediction(client):
    response = client.post(
        "/api/full-analysis",
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

    assert response.status_code == 200, response.get_data(as_text=True)
    data = response.get_json()
    assert data["mode"] == "ml_only"
    assert data["chat"]["source"] in ("fallback_local", "watson_assistant", "safety_override")
    assert data["recommendation"]["risk_classification"] in ("baixo", "médio", "alto")
    assert data["safe_response"]
    assert data["disclaimer"]


def test_cors_header_is_present(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"]
