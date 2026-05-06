"""
CardioIA Fase 6 — Sistema Preditivo Multiagente
Parte 2: pipeline modular (`agents/personas/`, `agents/pipeline/`).

Uso:
    python -m agents.main

A API pública do pipeline está em `agents.pipeline` (reexportada aqui para compatibilidade).
"""
import logging
import sys
from agents.pipeline import (
    PATIENT_FIELD_RANGES,
    run_pipeline,
    run_pipeline_ml_only,
    validate_patient_data,
)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

PACIENTE_DEMO = {
    "idade": 65,
    "freq_cardiaca": 115,
    "spo2": 91.5,
    "carga_sistema": 0.85,
    "disponibilidade_recursos": 0.20,
}

__all__ = [
    "PACIENTE_DEMO",
    "PATIENT_FIELD_RANGES",
    "validate_patient_data",
    "run_pipeline",
    "run_pipeline_ml_only",
]


def _print_banner(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def _print_result(patient_data: dict, recommendation: dict) -> None:
    _print_banner("RECOMENDAÇÃO FINAL — CardioIA Fase 6")

    prob = recommendation.get("probability")
    classif = recommendation.get("risk_classification", "—")
    protocols = recommendation.get("suggested_protocols", [])
    disclaimer = recommendation.get("disclaimer", "")

    if prob is not None:
        print(f"  Probabilidade de pico de risco : {prob:.1%}")
    print(f"  Classificação de risco         : {classif.upper()}")

    if protocols:
        print("\n  Protocolos sugeridos:")
        for p in protocols:
            nome = p.get("nome", p.get("protocol_id", ""))
            print(f"    [{p.get('protocol_id', '')}] {nome}")
            for acao in p.get("acoes", []):
                print(f"      • {acao}")

    print(f"\n  {disclaimer}")
    print("=" * 60)


def main() -> None:
    _print_banner("CARDIOIA FASE 6 — SISTEMA PREDITIVO MULTIAGENTE")
    print(f"\n  Paciente: {PACIENTE_DEMO}")
    print("\n  Iniciando pipeline de agentes...\n")

    try:
        recommendation = run_pipeline(PACIENTE_DEMO)
        _print_result(PACIENTE_DEMO, recommendation)
    except (ValueError, RuntimeError) as exc:
        print(f"\n[ERRO] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
