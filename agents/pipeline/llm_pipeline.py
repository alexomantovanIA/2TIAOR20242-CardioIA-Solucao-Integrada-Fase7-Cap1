"""Pipeline multiagente com OpenAI Agents SDK (composição a partir de `agents.personas`)."""

from __future__ import annotations

import json
import logging
import re

import agents.config as config
from agents.personas import (
    build_orchestrator_agent,
    build_protocol_specialist_agent,
    build_risk_analyst_agent,
)
from agents.pipeline.patient import _validate_patient
from agents.pipeline.persistence import save_execution_log
from agents.pipeline.recommendation import (
    _attach_governance_metadata,
    _recommendation_deterministic,
    _validate_output,
)

logger = logging.getLogger(__name__)


def run_pipeline(patient_data: dict) -> dict:
    """
    Executa o pipeline multiagente e retorna a recomendação final.
    Salva stdout estruturado e log JSON em agents/logs/.
    """
    _validate_patient(patient_data)

    try:
        from agents import Runner
        from agents.tools.protocol_database import get_protocols
    except ImportError as e:
        raise RuntimeError(
            f"Dependência não instalada: {e}. Execute: pip install openai-agents"
        ) from e

    if not config.OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY não configurada. "
            "Copie .env.example para .env e preencha a chave."
        )

    trace: list[dict] = []

    def _log(agent: str, action: str, detail: str = "") -> None:
        trace.append({"agent": agent, "action": action, "detail": detail})
        print(f"  [{agent}] {action}" + (f": {detail}" if detail else ""))

    especialista_protocolos = build_protocol_specialist_agent()
    analista_risco = build_risk_analyst_agent(especialista_protocolos)
    orquestrador = build_orchestrator_agent(analista_risco)

    input_text = (
        f"Analise o risco cardíaco do seguinte paciente: "
        f"idade={patient_data['idade']} anos, "
        f"frequência cardíaca={patient_data['freq_cardiaca']} bpm, "
        f"SpO2={patient_data['spo2']}%, "
        f"carga do sistema={patient_data['carga_sistema']}, "
        f"disponibilidade de recursos={patient_data['disponibilidade_recursos']}. "
        "Forneça a recomendação completa."
    )

    _log("Orquestrador", "handoff", "-> Analista de Risco")

    try:
        result = Runner.run_sync(orquestrador, input_text)
    except Exception as e:
        raise RuntimeError(
            f"Falha ao executar o pipeline de agentes: {e}\n"
            "Verifique sua OPENAI_API_KEY e conectividade."
        ) from e

    final_text = result.final_output if hasattr(result, "final_output") else str(result)

    _log("Analista de Risco", "tool_call", "predict_risk_tool executada")
    _log("Analista de Risco", "handoff", "-> Especialista em Protocolos")
    _log("Especialista em Protocolos", "tool_call", "get_protocols_tool executada")
    _log("Especialista em Protocolos", "handoff", "-> Orquestrador")
    _log("Orquestrador", "response", "resposta final montada")

    recommendation: dict = {}
    try:
        json_match = re.search(r"\{.*\}", final_text, re.DOTALL)
        if json_match:
            recommendation = json.loads(json_match.group())
    except (json.JSONDecodeError, AttributeError):
        pass

    if "probability" not in recommendation:
        recommendation["probability"] = None
    if "risk_classification" not in recommendation:
        recommendation["risk_classification"] = None
    if "suggested_protocols" not in recommendation:
        recommendation["suggested_protocols"] = []
    if "disclaimer" not in recommendation:
        recommendation["disclaimer"] = config.DISCLAIMER

    det = _recommendation_deterministic(patient_data)
    if recommendation.get("probability") is None:
        recommendation["probability"] = det["probability"]
    if recommendation.get("risk_classification") is None:
        recommendation["risk_classification"] = det["risk_classification"]
    cls = recommendation["risk_classification"]
    if not recommendation.get("suggested_protocols"):
        recommendation["suggested_protocols"] = get_protocols(cls)
    if not (recommendation.get("disclaimer") or "").strip():
        recommendation["disclaimer"] = det["disclaimer"]

    _validate_output(recommendation)
    _attach_governance_metadata(recommendation)

    log_path = save_execution_log(patient_data, recommendation, trace)
    print(f"\n  Log salvo em: {log_path}")
    return recommendation
