"""Definições dos agentes CardioIA (um módulo por agente — separação de responsabilidades)."""

from agents.personas.protocol_specialist_agent import build_protocol_specialist_agent
from agents.personas.risk_analyst_agent import build_risk_analyst_agent
from agents.personas.orchestrator_agent import build_orchestrator_agent

__all__ = [
    "build_protocol_specialist_agent",
    "build_risk_analyst_agent",
    "build_orchestrator_agent",
]
