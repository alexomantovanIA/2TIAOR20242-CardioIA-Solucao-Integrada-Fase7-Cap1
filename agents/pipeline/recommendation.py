"""Recomendação determinística (ML + protocolos) e pipeline ml_only."""

import agents.config as config
from agents.governance.coherence import evaluate_recommendation_coherence
from agents.pipeline.patient import _validate_patient
from agents.pipeline.persistence import save_execution_log


def _recommendation_deterministic(patient_data: dict) -> dict:
    """Monta recomendação só com modelo supervisionado + protocolos (sem LLM)."""
    from agents.tools.risk_predictor import predict_risk
    from agents.tools.protocol_database import get_protocols

    ml_out = predict_risk(patient_data)
    cls = ml_out["risk_classification"]
    return {
        "probability": ml_out["probability"],
        "risk_classification": cls,
        "suggested_protocols": get_protocols(cls),
        "disclaimer": config.DISCLAIMER,
    }


def _validate_output(recommendation: dict) -> None:
    required = ["probability", "risk_classification", "suggested_protocols", "disclaimer"]
    missing = [k for k in required if k not in recommendation or recommendation[k] is None]
    if missing:
        raise RuntimeError(
            f"Validação de saída falhou — campos ausentes ou nulos: {missing}"
        )


def _attach_governance_metadata(recommendation: dict) -> None:
    recommendation["governance"] = evaluate_recommendation_coherence(recommendation)


def run_pipeline_ml_only(patient_data: dict) -> dict:
    """
    Executa apenas predição ML + protocolos determinísticos (sem OpenAI Agents SDK).
    """
    _validate_patient(patient_data)
    recommendation = _recommendation_deterministic(patient_data)
    _validate_output(recommendation)
    _attach_governance_metadata(recommendation)
    trace = [
        {
            "agent": "Sistema",
            "action": "ml_only",
            "detail": "Predição supervisionada sem orquestração LLM.",
        }
    ]
    log_path = save_execution_log(patient_data, recommendation, trace)
    print(f"\n  Log salvo em: {log_path}")
    return recommendation
