"""
Verificação simples de coerência entre classificação de risco e protocolos sugeridos.

Atende ao critério de governança do enunciado (protocolos alinhados ao nível de risco)
e facilita auditoria das decisões do sistema.
"""
from __future__ import annotations

import unicodedata
from typing import Any


def _normalize_label(value: str) -> str:
    s = unicodedata.normalize("NFKD", value.strip())
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def evaluate_recommendation_coherence(recommendation: dict[str, Any]) -> dict[str, Any]:
    """
    Confere se cada protocolo retornado declara o mesmo nível de risco que a classificação final.

    Returns:
        dict com coherence_ok (bool) e coherence_notes (lista de strings, vazia se ok).
    """
    cls = recommendation.get("risk_classification")
    notes: list[str] = []

    if not cls:
        return {"coherence_ok": False, "coherence_notes": ["Classificação de risco ausente."]}

    cls_n = _normalize_label(str(cls))
    protocols = recommendation.get("suggested_protocols") or []

    if not protocols:
        notes.append("Nenhum protocolo sugerido para validar coerência.")
        return {"coherence_ok": False, "coherence_notes": notes}

    for p in protocols:
        if not isinstance(p, dict):
            notes.append("Item de protocolo inválido (não é objeto).")
            continue
        rl = p.get("risk_level")
        pid = p.get("protocol_id", "?")
        if rl is None:
            continue
        if _normalize_label(str(rl)) != cls_n:
            notes.append(
                f"Incoerência: protocolo {pid} com risk_level='{rl}' "
                f"não corresponde à classificação '{cls}'."
            )

    return {"coherence_ok": len(notes) == 0, "coherence_notes": notes}
