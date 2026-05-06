"""Governança / coerência protocolo × classificação (enunciado Fase 6, IR ALÉM 1)."""

from agents.governance.coherence import evaluate_recommendation_coherence


def test_coherence_ok_when_protocols_match_classification():
    rec = {
        "risk_classification": "baixo",
        "suggested_protocols": [
            {"protocol_id": "PROT-001", "risk_level": "baixo", "nome": "Monitoramento"},
        ],
    }
    out = evaluate_recommendation_coherence(rec)
    assert out["coherence_ok"] is True
    assert out["coherence_notes"] == []


def test_coherence_fails_on_mismatched_risk_level():
    rec = {
        "risk_classification": "baixo",
        "suggested_protocols": [
            {"protocol_id": "PROT-003", "risk_level": "alto", "nome": "Emergência"},
        ],
    }
    out = evaluate_recommendation_coherence(rec)
    assert out["coherence_ok"] is False
    assert any("Incoerência" in n for n in out["coherence_notes"])


def test_coherence_accepts_medio_unicode():
    rec = {
        "risk_classification": "médio",
        "suggested_protocols": [
            {"protocol_id": "PROT-002", "risk_level": "médio"},
        ],
    }
    out = evaluate_recommendation_coherence(rec)
    assert out["coherence_ok"] is True
