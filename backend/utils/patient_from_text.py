"""
Heurísticas leves para extrair os 5 campos numéricos do modelo a partir de texto livre (pt-BR).
Usado para sugerir a análise preditiva após o chat, sem substituir validação formal no endpoint.
"""
from __future__ import annotations

import re
from typing import Any

# Alinhado a agents/main.PATIENT_FIELD_RANGES
_FIELD_RANGES: dict[str, tuple[float, float]] = {
    "idade": (18, 90),
    "freq_cardiaca": (40, 200),
    "spo2": (80.0, 100.0),
    "carga_sistema": (0.0, 1.0),
    "disponibilidade_recursos": (0.0, 1.0),
}

FIELD_ORDER = [
    "idade",
    "freq_cardiaca",
    "spo2",
    "carga_sistema",
    "disponibilidade_recursos",
]


def _in_range(field: str, value: float) -> bool:
    lo, hi = _FIELD_RANGES[field]
    return lo <= value <= hi


def _parse_decimal(s: str) -> float:
    return float(s.replace(",", ".").strip())


def extract_patient_fields_from_text(message: str) -> dict[str, Any]:
    """Extrai o que for reconhecível; valores fora do intervalo são ignorados."""
    if not message or not message.strip():
        return {}

    text = message.lower()
    found: dict[str, Any] = {}

    for pattern in (
        r"\b(\d{1,2})\s*anos?\b",
        r"\bidade\s*(?:de|:)?\s*(\d{1,2})\b",
    ):
        m = re.search(pattern, text)
        if m:
            v = int(m.group(1))
            if _in_range("idade", v):
                found["idade"] = v
            break

    for pattern in (
        r"\b(\d{2,3})\s*bpm\b",
        r"\bfrequ(?:ê|e)ncia\s*(?:card(?:í|i)aca)?\s*(?:de|:)?\s*(\d{2,3})\b",
        r"\bfc\s*(?:de|:|=)?\s*(\d{2,3})\b",
        r"\bpulso\s*(?:de|:|=)?\s*(\d{2,3})\b",
        r"\b(\d{2,3})\s*(?:batimentos|bat/min)\b",
    ):
        m = re.search(pattern, text)
        if m:
            v = int(m.group(1))
            if _in_range("freq_cardiaca", v):
                found["freq_cardiaca"] = v
            break

    for pattern in (
        r"\b(?:spo2|sat(?:ura(?:ç|c)ao)?(?:\s+de)?(?:\s+oxigenio)?)\s*(?:de|:|=)?\s*(\d{1,2}(?:[.,]\d+)?)\s*%?",
        r"\boximetria\s*(?:de|:|=)?\s*(\d{1,2}(?:[.,]\d+)?)\s*%?",
        r"\b(\d{2}(?:[.,]\d+)?)\s*%\s*(?:de\s*)?(?:spo2|sat|oxigenio)\b",
    ):
        m = re.search(pattern, text)
        if m:
            v = _parse_decimal(m.group(1))
            if _in_range("spo2", v):
                found["spo2"] = v
            break

    m = re.search(
        r"\bcarga\s*(?:do\s*)?sistema\s*(?:de|:)?\s*(0?\.\d+|1\.0|1|0)\b",
        text,
    )
    if m:
        v = _parse_decimal(m.group(1))
        if _in_range("carga_sistema", v):
            found["carga_sistema"] = v

    m = re.search(
        r"\bdisponibilidade\s*(?:de\s*)?recursos\s*(?:de|:|=)?\s*(0?\.\d+|1\.0|1|0)\b",
        text,
    )
    if not m:
        m = re.search(
            r"\brecursos\s*(?:de|:|=)?\s*(0?\.\d+|1\.0|1|0)\b",
            text,
        )
    if m:
        v = _parse_decimal(m.group(1))
        if _in_range("disponibilidade_recursos", v):
            found["disponibilidade_recursos"] = v

    return found


def build_predictive_suggestion(message: str) -> dict[str, Any] | None:
    """
    Se houver dados extraídos, devolve objeto para o frontend sugerir /api/predict-risk.
    None se nada foi reconhecido.
    """
    extracted = extract_patient_fields_from_text(message)
    if not extracted:
        return None

    missing = [f for f in FIELD_ORDER if f not in extracted]
    patient_payload: dict[str, Any] | None = None
    if not missing:
        patient_payload = {k: extracted[k] for k in FIELD_ORDER}

    return {
        "extracted_fields": extracted,
        "missing_fields": missing,
        "ready_for_predict": patient_payload is not None,
        "patient_payload": patient_payload,
    }
