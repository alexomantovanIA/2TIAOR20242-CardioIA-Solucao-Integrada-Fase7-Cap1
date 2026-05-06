"""
Processamento em lote de casos clínicos simulados (IR ALÉM 2 — enunciado FIAP).

Executa o mesmo pipeline determinístico que ``run_pipeline_ml_only`` para cada
paciente em sequência, grava um resumo JSON em ``agents/logs/`` e imprime uma
linha por caso no terminal.

Uso::

    python -m agents.batch_process
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Casos de demonstração (valores sintéticos, âmbito académico)
BATCH_DEMO: list[dict[str, Any]] = [
    {
        "idade": 45,
        "freq_cardiaca": 72,
        "spo2": 98.0,
        "carga_sistema": 0.2,
        "disponibilidade_recursos": 0.9,
    },
    {
        "idade": 65,
        "freq_cardiaca": 115,
        "spo2": 91.5,
        "carga_sistema": 0.85,
        "disponibilidade_recursos": 0.2,
    },
    {
        "idade": 78,
        "freq_cardiaca": 140,
        "spo2": 88.0,
        "carga_sistema": 0.95,
        "disponibilidade_recursos": 0.15,
    },
]


def run_batch_ml_only(patients: list[dict]) -> list[dict]:
    """
    Processa cada paciente com ``run_pipeline_ml_only`` (ML + protocolos + governança).

    Returns:
        Lista de dicts com chaves: index, patient, ok, e recommendation ou error.
    """
    from agents.pipeline import run_pipeline_ml_only, validate_patient_data

    results: list[dict] = []
    for i, patient in enumerate(patients):
        row: dict[str, Any] = {"index": i, "patient": patient, "ok": False}
        try:
            validate_patient_data(patient)
            recommendation = run_pipeline_ml_only(patient)
            row["ok"] = True
            row["recommendation"] = recommendation
        except Exception as exc:
            row["error"] = str(exc)
        results.append(row)
    return results


def main() -> None:
    print("CardioIA — lote ml_only (IR ALÉM 2),", len(BATCH_DEMO), "casos\n")
    results = run_batch_ml_only(BATCH_DEMO)
    for row in results:
        idx = row["index"]
        if row["ok"]:
            rec = row["recommendation"]
            gov = rec.get("governance", {})
            print(
                f"  [{idx}] OK — classificação={rec.get('risk_classification')} "
                f"coerência={gov.get('coherence_ok')}"
            )
        else:
            print(f"  [{idx}] ERRO — {row.get('error')}", file=sys.stderr)

    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    summary_path = logs_dir / "batch_last_summary.json"
    summary_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"\n  Resumo gravado em: {summary_path}")


if __name__ == "__main__":
    main()
