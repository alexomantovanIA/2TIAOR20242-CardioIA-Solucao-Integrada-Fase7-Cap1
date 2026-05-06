from flask import Blueprint, request, jsonify

from backend.services.watson_service import WatsonService
from backend.utils.patient_from_text import build_predictive_suggestion
from backend.utils.prediction_readiness import get_prediction_readiness
from backend.utils.validators import validate_message, sanitize_message

chat_bp = Blueprint("chat", __name__)

watson_service = WatsonService()
GENERIC_FALLBACK_PREFIX = "Nao identifiquei com clareza"

_SYMPTOM_INTENTS = frozenset([
    "informar_dor_peito", "informar_palpitacao", "informar_falta_ar",
    "informar_tontura", "informar_pressao", "informar_inchaco", "informar_sintoma_geral",
])

_PREDICTIVE_FIELDS = [
    "idade", "freq_cardiaca", "spo2", "carga_sistema", "disponibilidade_recursos"
]


def _predictive_transition_reply(suggestion: dict) -> tuple[str, str, bool]:
    missing = suggestion.get("missing_fields") or []
    if not missing:
        return (
            "Perfeito, entendi seu contexto clinico e ja tenho todos os parametros. Vou iniciar a analise preditiva.",
            "Dados completos recebidos; iniciar analise preditiva.",
            True,
        )

    missing_labels = {
        "idade": "idade",
        "freq_cardiaca": "frequencia cardiaca",
        "spo2": "SpO2",
        "carga_sistema": "carga do sistema",
        "disponibilidade_recursos": "disponibilidade de recursos",
    }
    readable_missing = [missing_labels.get(field, field) for field in missing]
    return (
        "Obrigado, ja captei parte dos dados. Posso seguir e coletar so o que falta para a analise preditiva.",
        f"Dados pendentes para etapa preditiva: {', '.join(readable_missing)}.",
        False,
    )


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True)

    if not body or "message" not in body:
        return jsonify({"message": "Campo 'message' e obrigatorio no corpo da requisicao."}), 400

    raw_message = body.get("message", "")
    conversation_id = body.get("conversation_id")

    is_valid, error_msg = validate_message(raw_message)
    if not is_valid:
        return jsonify({"message": error_msg}), 400

    message = sanitize_message(raw_message)
    response = watson_service.send_message(message, conversation_id)

    payload = response.to_dict()
    if not response.urgency_detected:
        suggestion = build_predictive_suggestion(message)
        if not suggestion:
            detected = set(payload.get("detected_intents") or [])
            if detected & _SYMPTOM_INTENTS:
                suggestion = {
                    "extracted_fields": {},
                    "missing_fields": _PREDICTIVE_FIELDS[:],
                    "ready_for_predict": False,
                    "patient_payload": None,
                }
        if suggestion:
            payload["predictive_suggestion"] = suggestion
            # Evita quebra de fluidez: quando a mensagem já traz contexto para predição,
            # substitui fallback genérico por uma transição conversacional.
            reply_text = payload.get("reply", "")
            # Substitui quando a resposta é o texto genérico de fallback,
            # independente da fonte (Watson ou local): ambos podem retorná-lo.
            is_generic_fallback = reply_text.startswith(GENERIC_FALLBACK_PREFIX)
            if is_generic_fallback:
                new_reply, new_follow_up, auto_start = _predictive_transition_reply(suggestion)
                payload["reply"] = new_reply
                payload["follow_up"] = new_follow_up
                payload["predictive_auto_start"] = auto_start

    return jsonify(payload), 200


@chat_bp.route("/health", methods=["GET"])
def health():
    readiness = get_prediction_readiness()
    return jsonify(
        {
            "status": "ok",
            "watson_connected": watson_service.is_connected,
            "mode": "watson_assistant" if watson_service.is_connected else "fallback_local",
            "fase6_prediction": readiness,
        }
    ), 200
