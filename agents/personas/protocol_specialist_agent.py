"""
Agente Especialista em Protocolos — consulta a base simulada (tools apenas).

Responsabilidade única: mapear classificação de risco → protocolos em `protocols.json`.
"""

from __future__ import annotations

from agents.tools.protocol_database import get_protocols_tool


def build_protocol_specialist_agent():
    """Instancia o agente SDK com instruções e tools do especialista em protocolos."""
    from agents import Agent

    return Agent(
        name="Especialista_em_Protocolos",
        instructions=(
            "Você é o Agente Especialista em Protocolos do sistema CardioIA. "
            "Sua única responsabilidade é receber uma classificação de risco "
            "('baixo', 'médio' ou 'alto') e retornar os protocolos médicos simulados "
            "correspondentes usando a tool get_protocols_tool. "
            "Retorne SOMENTE o resultado da tool, sem texto adicional."
        ),
        tools=[get_protocols_tool],
    )
