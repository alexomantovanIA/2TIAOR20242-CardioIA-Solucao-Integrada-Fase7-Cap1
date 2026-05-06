"""
Orquestração do pipeline Fase 6 — validação, predição ML-only e pipeline multiagente.

Mantém a API pública usada por `agents.main`, `backend/routes/prediction_routes` e testes.
"""

from agents.pipeline.patient import PATIENT_FIELD_RANGES, validate_patient_data
from agents.pipeline.recommendation import run_pipeline_ml_only
from agents.pipeline.llm_pipeline import run_pipeline

__all__ = [
    "PATIENT_FIELD_RANGES",
    "validate_patient_data",
    "run_pipeline_ml_only",
    "run_pipeline",
]
