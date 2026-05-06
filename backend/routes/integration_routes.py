import logging

from flask import Blueprint, jsonify, request

from backend.routes.prediction_routes import _coerce_patient
from backend.routes.chat_routes import watson_service
from backend.services.iot_store import (
    ACADEMIC_DISCLAIMER,
    get_latest_iot_reading,
    normalize_iot_reading,
    patient_from_iot,
    save_latest_iot_reading,
)

logger = logging.getLogger(__name__)

integration_bp = Blueprint("integration", __name__)


def _ml_recommendation(patient: dict) -> dict:
    from agents.pipeline import run_pipeline_ml_only, validate_patient_data

    validate_patient_data(patient)
    return run_pipeline_ml_only(patient)


def _summarize_protocols(recommendation: dict | None) -> str:
    if not recommendation:
        return "Envie uma leitura IoT para gerar uma recomendacao academica."
    protocols = recommendation.get("suggested_protocols") or []
    if not protocols:
        return "Monitorar sinais e procurar avaliacao profissional em caso de piora."
    first = protocols[0]
    if isinstance(first, dict):
        return first.get("nome") or first.get("title") or first.get("name") or str(first)
    return str(first)


def _patient_from_body_or_latest(body: dict) -> tuple[dict | None, dict | None]:
    patient_body = body.get("patient") if isinstance(body.get("patient"), dict) else body
    try:
        return _coerce_patient(patient_body), None
    except (TypeError, ValueError):
        latest = get_latest_iot_reading()
        if latest:
            overrides = body.get("patient_overrides") if isinstance(body.get("patient_overrides"), dict) else {}
            return patient_from_iot(latest, overrides), latest
    return None, None


@integration_bp.route("/api/iot/ingest", methods=["POST"])
def ingest_iot():
    body = request.get_json(silent=True) or {}
    try:
        reading = normalize_iot_reading(body)
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400

    save_latest_iot_reading(reading)
    patient_payload = patient_from_iot(reading, body.get("patient_overrides") or {})
    payload = {
        "accepted": True,
        "reading": reading,
        "patient_payload": patient_payload,
        "disclaimer": ACADEMIC_DISCLAIMER,
    }

    if body.get("include_recommendation") is True:
        try:
            payload["recommendation"] = _ml_recommendation(patient_payload)
        except Exception as exc:
            logger.warning("Falha ao gerar recomendacao no ingest IoT: %s", exc)
            payload["recommendation_error"] = str(exc)

    return jsonify(payload), 201


@integration_bp.route("/api/dashboard/summary", methods=["GET"])
def dashboard_summary():
    latest = get_latest_iot_reading()
    if not latest:
        return jsonify(
            {
                "latest_iot_reading": None,
                "risk_current": None,
                "recommendation": "Aguardando leitura IoT.",
                "disclaimer": ACADEMIC_DISCLAIMER,
            }
        ), 200

    patient = patient_from_iot(latest)
    try:
        recommendation = _ml_recommendation(patient)
        risk_current = recommendation.get("risk_classification")
        recommendation_text = _summarize_protocols(recommendation)
    except Exception as exc:
        logger.warning("Dashboard sem recomendacao ML: %s", exc)
        recommendation = None
        risk_current = latest.get("status")
        recommendation_text = "Monitorar sinais e validar o backend preditivo."

    return jsonify(
        {
            "latest_iot_reading": latest,
            "patient_payload": patient,
            "risk_current": risk_current,
            "recommendation": recommendation_text,
            "recommendation_detail": recommendation,
            "disclaimer": ACADEMIC_DISCLAIMER,
        }
    ), 200


@integration_bp.route("/api/patient/latest", methods=["GET"])
def patient_latest():
    latest = get_latest_iot_reading()
    if not latest:
        return jsonify(
            {
                "patient": None,
                "latest_iot_reading": None,
                "disclaimer": ACADEMIC_DISCLAIMER,
            }
        ), 200

    return jsonify(
        {
            "patient": patient_from_iot(latest),
            "latest_iot_reading": latest,
            "disclaimer": ACADEMIC_DISCLAIMER,
        }
    ), 200


@integration_bp.route("/api/full-analysis", methods=["POST"])
def full_analysis():
    body = request.get_json(silent=True) or {}
    message = str(body.get("message") or "Analise integrada CardioIA.").strip()
    if len(message) < 2:
        message = "Analise integrada CardioIA."

    patient, latest = _patient_from_body_or_latest(body)
    if not patient:
        return jsonify(
            {
                "message": (
                    "Informe os campos do paciente ou envie antes uma leitura em /api/iot/ingest."
                )
            }
        ), 400

    chat_response = watson_service.send_message(message, body.get("conversation_id"))
    chat_payload = chat_response.to_dict()
    recommendation = None
    if not chat_response.urgency_detected:
        try:
            recommendation = _ml_recommendation(patient)
        except ValueError as exc:
            return jsonify({"message": str(exc)}), 400
        except Exception as exc:
            logger.exception("Falha na analise completa")
            return jsonify({"message": str(exc)}), 500

    return jsonify(
        {
            "mode": "ml_only",
            "patient": patient,
            "latest_iot_reading": latest,
            "chat": chat_payload,
            "recommendation": recommendation,
            "urgency_detected": chat_response.urgency_detected,
            "safe_response": chat_payload.get("reply"),
            "disclaimer": ACADEMIC_DISCLAIMER,
        }
    ), 200
