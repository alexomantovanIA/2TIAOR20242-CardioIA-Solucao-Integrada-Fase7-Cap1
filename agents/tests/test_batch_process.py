"""Lote ml_only (IR ALÉM 2)."""

from pathlib import Path

import pytest

import agents.config as agent_config
from agents.batch_process import BATCH_DEMO, run_batch_ml_only


@pytest.mark.skipif(
    not Path(agent_config.MODEL_PATH).is_file(),
    reason="Artefato ml/modelo_risco_cardiaco.joblib ausente",
)
def test_run_batch_ml_only_all_succeed_with_coherence():
    out = run_batch_ml_only(BATCH_DEMO[:2])
    assert len(out) == 2
    assert all(r["ok"] for r in out)
    for r in out:
        rec = r["recommendation"]
        assert rec["governance"]["coherence_ok"] is True


def test_batch_demo_has_three_cases():
    assert len(BATCH_DEMO) == 3
