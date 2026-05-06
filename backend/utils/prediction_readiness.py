"""
Indicadores de prontidão do endpoint de predição (Fase 6) para o /health.
Evita carregar o modelo completo no healthcheck — apenas ficheiros e import leve.
"""
from __future__ import annotations

import os
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_prediction_readiness() -> dict:
    root = _repo_root()
    model_path = root / "ml" / "modelo_risco_cardiaco.joblib"
    protocols_path = root / "agents" / "data" / "protocols.json"

    model_file_present = model_path.is_file()
    protocols_file_present = protocols_path.is_file()
    predict_risk_ready = model_file_present and protocols_file_present

    openai_api_configured = bool(os.getenv("OPENAI_API_KEY", "").strip())

    openai_agents_sdk_importable = False
    try:
        from importlib.metadata import version

        version("openai-agents")
        openai_agents_sdk_importable = True
    except Exception:
        openai_agents_sdk_importable = False

    multiagent_full_pipeline_ready = (
        predict_risk_ready and openai_api_configured and openai_agents_sdk_importable
    )

    return {
        "model_file_present": model_file_present,
        "protocols_file_present": protocols_file_present,
        "predict_risk_ready": predict_risk_ready,
        "openai_api_configured": openai_api_configured,
        "openai_agents_sdk_importable": openai_agents_sdk_importable,
        "multiagent_full_pipeline_ready": multiagent_full_pipeline_ready,
    }
