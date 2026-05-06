import logging
from pathlib import Path

import joblib
import pandas as pd

import agents.config as config

logger = logging.getLogger(__name__)

_FEATURES = ["idade", "freq_cardiaca", "spo2", "carga_sistema", "disponibilidade_recursos"]

_cached_model = None
_cached_model_path: str | None = None


def _load_model():
    global _cached_model, _cached_model_path
    path = config.MODEL_PATH
    if _cached_model is not None and _cached_model_path == path:
        return _cached_model
    _cached_model = None
    _cached_model_path = None
    if not Path(path).exists():
        raise FileNotFoundError(
            f"Modelo não encontrado em '{path}'. "
            "Execute o notebook em notebooks/ (local ou Colab) e grave o .joblib em ml/."
        )
    _cached_model = joblib.load(path)
    _cached_model_path = path
    logger.info("Modelo carregado: %s", path)
    return _cached_model


def _classify(probability: float) -> str:
    """Converte probabilidade em rótulo de risco (boundary: [0.3, 0.7) → médio)."""
    if probability < config.RISK_THRESHOLDS["baixo_max"]:
        return "baixo"
    if probability < config.RISK_THRESHOLDS["medio_max"]:
        return "médio"
    return "alto"


def predict_risk(patient_data: dict) -> dict:
    """
    Carrega o modelo treinado e prevê o risco de pico cardíaco.

    Args:
        patient_data: dict com chaves idade, freq_cardiaca, spo2,
                      carga_sistema, disponibilidade_recursos.

    Returns:
        dict com probability (float), risk_classification (str), source_model (str).
    """
    model = _load_model()

    try:
        X = pd.DataFrame([{f: patient_data[f] for f in _FEATURES}])
    except KeyError as e:
        raise ValueError(f"Campo obrigatório ausente nos dados do paciente: {e}") from e

    probability = float(model.predict_proba(X)[0][1])
    classification = _classify(probability)
    source = Path(config.MODEL_PATH).name

    logger.info(
        "Predição: prob=%.3f classificação=%s modelo=%s",
        probability, classification, source
    )
    return {
        "probability": round(probability, 4),
        "risk_classification": classification,
        "source_model": source,
    }


# Wrapper para uso como tool do OpenAI Agents SDK
try:
    from agents import function_tool  # openai-agents SDK

    @function_tool
    def predict_risk_tool(
        idade: int,
        freq_cardiaca: int,
        spo2: float,
        carga_sistema: float,
        disponibilidade_recursos: float,
    ) -> dict:
        """
        Consulta o modelo de ML treinado e retorna a probabilidade de pico de risco
        cardíaco e a classificação de risco (baixo/médio/alto) para o paciente.
        """
        patient_data = {
            "idade": idade,
            "freq_cardiaca": freq_cardiaca,
            "spo2": spo2,
            "carga_sistema": carga_sistema,
            "disponibilidade_recursos": disponibilidade_recursos,
        }
        return predict_risk(patient_data)

except ImportError:
    predict_risk_tool = None
    logger.warning("openai-agents não instalado; predict_risk_tool não disponível.")
