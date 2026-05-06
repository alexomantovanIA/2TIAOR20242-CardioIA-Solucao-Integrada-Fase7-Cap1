import logging

from flask import Blueprint, jsonify, request

from backend.utils.safety_rules import URGENCY_RESPONSE, check_urgency

logger = logging.getLogger(__name__)

prediction_bp = Blueprint("prediction", __name__)

PATIENT_KEYS = [
    "idade",
    "freq_cardiaca",
    "spo2",
    "carga_sistema",
    "disponibilidade_recursos",
]


def _missing_value(v) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and not v.strip():
        return True
    return False


def _coerce_patient(body: dict) -> dict:
    raw = {k: body.get(k) for k in PATIENT_KEYS}
    missing = [k for k in PATIENT_KEYS if _missing_value(raw[k])]
    if missing:
        raise ValueError(f"Campos obrigatorios ausentes: {', '.join(missing)}")

    out: dict = {}
    out["idade"] = int(raw["idade"])
    out["freq_cardiaca"] = int(raw["freq_cardiaca"])
    out["spo2"] = float(str(raw["spo2"]).replace(",", "."))
    out["carga_sistema"] = float(str(raw["carga_sistema"]).replace(",", "."))
    out["disponibilidade_recursos"] = float(
        str(raw["disponibilidade_recursos"]).replace(",", ".")
    )
    return out


@prediction_bp.route("/api/predict-risk", methods=["POST"])
def predict_risk_http():
    """
    Nível 1: expõe o pipeline Fase 6 via HTTP.
    - context_message: texto opcional; se indicar urgência (mesmas regras do chat), não corre ML.
    - mode: 'agents' (default) ou 'ml_only'. Sem OPENAI_API_KEY, usa ml_only automaticamente.
    """
    body = request.get_json(silent=True) or {}

    context_message = body.get("context_message") or ""
    if isinstance(context_message, str) and context_message.strip():
        is_urgent, _keywords = check_urgency(context_message)
        if is_urgent:
            return (
                jsonify(
                    {
                        "urgency_detected": True,
                        "urgency_message": URGENCY_RESPONSE,
                        "recommendation": None,
                        "mode": None,
                    }
                ),
                200,
            )

    try:
        import agents.config as agent_config
        from agents.pipeline import run_pipeline, run_pipeline_ml_only, validate_patient_data
    except ImportError as exc:
        logger.exception("Dependencia agents nao disponivel")
        return jsonify({"message": f"Modulo de predicao indisponivel: {exc}"}), 500

    try:
        patient = _coerce_patient(body)
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400

    mode = body.get("mode") or "agents"
    if mode not in ("agents", "ml_only"):
        return jsonify({"message": "Campo 'mode' deve ser 'agents' ou 'ml_only'."}), 400

    try:
        validate_patient_data(patient)
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400

    note = None
    try:
        if mode == "ml_only":
            recommendation = run_pipeline_ml_only(patient)
            return (
                jsonify(
                    {
                        "urgency_detected": False,
                        "mode": "ml_only",
                        "recommendation": recommendation,
                        "note": note,
                    }
                ),
                200,
            )

        if not agent_config.OPENAI_API_KEY:
            recommendation = run_pipeline_ml_only(patient)
            note = (
                "OPENAI_API_KEY nao configurada; retorno apenas com modelo supervisionado "
                "(equivalente a mode=ml_only)."
            )
            return (
                jsonify(
                    {
                        "urgency_detected": False,
                        "mode": "ml_only",
                        "recommendation": recommendation,
                        "note": note,
                    }
                ),
                200,
            )

        recommendation = run_pipeline(patient)
        return (
            jsonify(
                {
                    "urgency_detected": False,
                    "mode": "agents",
                    "recommendation": recommendation,
                    "note": note,
                }
            ),
            200,
        )
    except RuntimeError as exc:
        logger.warning("Pipeline Fase 6: %s", exc)
        return jsonify({"message": str(exc)}), 503
    except Exception as exc:
        logger.exception("Erro inesperado no pipeline de predicao")
        return jsonify({"message": str(exc)}), 500
