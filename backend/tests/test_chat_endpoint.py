import pytest
from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["AUTH_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_chat_valid_message(client):
    response = client.post("/api/chat", json={
        "message": "Estou com palpitacoes leves ha 2 dias.",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
    assert "source" in data
    assert "conversation_id" in data
    assert "urgency_detected" in data
    assert "detected_intents" in data
    assert "detected_entities" in data


def test_chat_missing_message(client):
    response = client.post("/api/chat", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data


def test_chat_empty_message(client):
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400


def test_chat_too_short_message(client):
    response = client.post("/api/chat", json={"message": "a"})
    assert response.status_code == 400


def test_chat_preserves_conversation_id(client):
    response = client.post("/api/chat", json={
        "message": "Oi, bom dia!",
        "conversation_id": "test-session-001",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["conversation_id"] == "test-session-001"


def test_chat_generates_conversation_id(client):
    response = client.post("/api/chat", json={
        "message": "Oi, bom dia!",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["conversation_id"] != ""


def test_chat_saudacao_intent(client):
    response = client.post("/api/chat", json={"message": "Ola, bom dia!"})
    assert response.status_code == 200
    data = response.get_json()
    assert "saudacao" in data["detected_intents"]


def test_chat_despedida_intent(client):
    response = client.post("/api/chat", json={"message": "Tchau, obrigado!"})
    assert response.status_code == 200
    data = response.get_json()
    assert "despedida" in data["detected_intents"]


def test_chat_palpitacao_intent(client):
    response = client.post("/api/chat", json={"message": "Estou com palpitacao"})
    assert response.status_code == 200
    data = response.get_json()
    assert "informar_palpitacao" in data["detected_intents"]


def test_chat_ecg_intent(client):
    response = client.post("/api/chat", json={"message": "O que e um ECG?"})
    assert response.status_code == 200
    data = response.get_json()
    assert "perguntar_ecg" in data["detected_intents"]


def test_chat_diagnostico_limit(client):
    response = client.post("/api/chat", json={"message": "O que eu tenho? Me da um diagnostico."})
    assert response.status_code == 200
    data = response.get_json()
    assert "solicitar_diagnostico" in data["detected_intents"]
    assert "Reforcar limite" in data["follow_up"]


def test_chat_has_disclaimer(client):
    response = client.post("/api/chat", json={"message": "Oi"})
    assert response.status_code == 200
    data = response.get_json()
    assert "disclaimer" in data
    assert "educacional" in data["disclaimer"]


def test_chat_no_body(client):
    response = client.post("/api/chat")
    assert response.status_code == 400


def test_chat_fallback_response(client):
    response = client.post("/api/chat", json={"message": "xyzabc123 mensagem aleatoria"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["reply"] != ""


def test_chat_predictive_suggestion_when_vitals_in_text(client):
    response = client.post(
        "/api/chat",
        json={
            "message": (
                "Tenho 50 anos, FC 80 bpm, SpO2 97%, "
                "carga do sistema 0.3 e disponibilidade de recursos 0.7."
            ),
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("predictive_suggestion", {}).get("ready_for_predict") is True
    assert "patient_payload" in data["predictive_suggestion"]
    assert "Nao identifiquei com clareza" not in data.get("reply", "")


def test_chat_replaces_generic_fallback_when_predictive_ready(client):
    response = client.post(
        "/api/chat",
        json={
            "message": (
                "Tenho 65 anos, FC 115 bpm, SpO2 91.5, "
                "carga do sistema 0.85 e disponibilidade de recursos 0.2."
            )
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("predictive_suggestion", {}).get("ready_for_predict") is True
    assert data.get("follow_up") == "Dados completos recebidos; iniciar analise preditiva."
    assert data.get("predictive_auto_start") is True
    assert "Nao identifiquei com clareza" not in data.get("reply", "")


def test_chat_no_predictive_suggestion_on_safety_override(client):
    response = client.post(
        "/api/chat",
        json={"message": "Estou com dor intensa no peito e falta de ar intensa."},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("urgency_detected") is True
    assert "predictive_suggestion" not in data
