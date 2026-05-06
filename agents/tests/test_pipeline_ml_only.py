"""Integração mínima: pipeline só ML + governança (sem OpenAI)."""

from pathlib import Path

import pytest

import agents.config as agent_config
from agents.pipeline import run_pipeline_ml_only


@pytest.mark.skipif(
    not Path(agent_config.MODEL_PATH).is_file(),
    reason="Artefato ml/modelo_risco_cardiaco.joblib ausente",
)
def test_run_pipeline_ml_only_returns_governance_and_coherent_protocols():
    patient = {
        "idade": 55,
        "freq_cardiaca": 90,
        "spo2": 96.0,
        "carga_sistema": 0.4,
        "disponibilidade_recursos": 0.6,
    }
    rec = run_pipeline_ml_only(patient)
    assert "probability" in rec
    assert "risk_classification" in rec
    assert "governance" in rec
    assert rec["governance"]["coherence_ok"] is True
    assert rec["governance"]["coherence_notes"] == []
