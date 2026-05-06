"""
T013 — Testes para agents/tools/risk_predictor.py
Escrever ANTES da implementação; verificar que falham primeiro.
"""
import pytest
from unittest.mock import patch, MagicMock
import numpy as np


class TestPredictRisk:

    def test_returns_required_keys(self, mock_model):
        from agents.tools.risk_predictor import predict_risk
        result = predict_risk({"idade": 50, "freq_cardiaca": 80, "spo2": 97.0,
                               "carga_sistema": 0.4, "disponibilidade_recursos": 0.6})
        assert "probability" in result
        assert "risk_classification" in result
        assert "source_model" in result

    def test_probability_in_range(self, mock_model):
        from agents.tools.risk_predictor import predict_risk
        result = predict_risk({"idade": 50, "freq_cardiaca": 80, "spo2": 97.0,
                               "carga_sistema": 0.4, "disponibilidade_recursos": 0.6})
        assert 0.0 <= result["probability"] <= 1.0

    # --- Boundary tests: [0.0, 0.3) → baixo, [0.3, 0.7) → médio, [0.7, 1.0] → alto ---

    def test_boundary_baixo(self):
        from agents.tools.risk_predictor import _classify
        assert _classify(0.0) == "baixo"
        assert _classify(0.29) == "baixo"

    def test_boundary_at_0_3_is_medio(self):
        from agents.tools.risk_predictor import _classify
        assert _classify(0.3) == "médio"

    def test_boundary_medio(self):
        from agents.tools.risk_predictor import _classify
        assert _classify(0.5) == "médio"
        assert _classify(0.69) == "médio"

    def test_boundary_at_0_7_is_alto(self):
        from agents.tools.risk_predictor import _classify
        assert _classify(0.7) == "alto"

    def test_boundary_alto(self):
        from agents.tools.risk_predictor import _classify
        assert _classify(0.9) == "alto"
        assert _classify(1.0) == "alto"

    def test_model_not_found_raises_gracefully(self):
        from agents.tools.risk_predictor import predict_risk
        import agents.config as config
        original = config.MODEL_PATH
        config.MODEL_PATH = "/path/que/nao/existe/modelo.joblib"
        try:
            with pytest.raises((FileNotFoundError, RuntimeError)):
                predict_risk({"idade": 50, "freq_cardiaca": 80, "spo2": 97.0,
                              "carga_sistema": 0.4, "disponibilidade_recursos": 0.6})
        finally:
            config.MODEL_PATH = original

    def test_source_model_is_string(self, mock_model):
        from agents.tools.risk_predictor import predict_risk
        result = predict_risk({"idade": 50, "freq_cardiaca": 80, "spo2": 97.0,
                               "carga_sistema": 0.4, "disponibilidade_recursos": 0.6})
        assert isinstance(result["source_model"], str)
        assert len(result["source_model"]) > 0


@pytest.fixture
def mock_model():
    mock = MagicMock()
    mock.predict_proba.return_value = np.array([[0.45, 0.55]])
    with patch("agents.tools.risk_predictor._load_model", return_value=mock):
        yield mock
