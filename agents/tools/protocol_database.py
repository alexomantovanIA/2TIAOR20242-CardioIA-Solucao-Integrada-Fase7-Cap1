import json
import logging
from pathlib import Path

import agents.config as config

logger = logging.getLogger(__name__)

_cached_protocols: dict | None = None


def _load_protocols() -> dict:
    global _cached_protocols
    if _cached_protocols is None:
        path = Path(config.PROTOCOLS_PATH)
        if not path.exists():
            raise FileNotFoundError(f"Base de protocolos não encontrada em '{path}'.")
        with open(path, encoding="utf-8") as f:
            _cached_protocols = json.load(f)
        logger.info("Protocolos carregados: %d níveis", len(_cached_protocols))
    return _cached_protocols


def get_protocols(risk_classification: str) -> list:
    """
    Consulta a base de protocolos simulados pelo nível de risco.

    Args:
        risk_classification: 'baixo', 'médio' ou 'alto'.

    Returns:
        Lista de dicts de protocolo. Retorna [] se nível inválido (sem exceção).
    """
    protocols = _load_protocols()
    result = protocols.get(risk_classification, [])

    if not result:
        logger.warning(
            "Nenhum protocolo encontrado para classificação '%s'. "
            "Valores válidos: %s",
            risk_classification,
            list(protocols.keys()),
        )
    else:
        logger.info(
            "Protocolo(s) encontrado(s) para '%s': %s",
            risk_classification,
            [p["protocol_id"] for p in result],
        )
    return result


# Wrapper para uso como tool do OpenAI Agents SDK
try:
    from agents import function_tool  # openai-agents SDK

    @function_tool
    def get_protocols_tool(risk_classification: str) -> list:
        """
        Consulta a base de protocolos médicos simulados e retorna os protocolos
        indicados para o nível de risco informado (baixo, médio ou alto).
        """
        return get_protocols(risk_classification)

except ImportError:
    get_protocols_tool = None
    logger.warning("openai-agents não instalado; get_protocols_tool não disponível.")
