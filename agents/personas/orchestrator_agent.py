"""
Agente Orquestrador — coordena handoffs e consolida a resposta final (JSON + disclaimer).

Responsabilidade: ponto de entrada do Runner; delega ao Analista de Risco e sintetiza saída.
"""

from __future__ import annotations

import agents.config as config


def build_orchestrator_agent(analista_risco):
    """Recebe a instância do analista de risco para o handoff inicial."""
    from agents import Agent, handoff

    return Agent(
        name="Orquestrador",
        instructions=(
            "Você é o Agente Orquestrador do sistema CardioIA. "
            "Receba os dados do paciente, delegue a análise de risco ao "
            "Analista de Risco via handoff, e depois monte a resposta final "
            "estruturada com: probabilidade prevista, classificação de risco, "
            "protocolos sugeridos e o seguinte aviso obrigatório:\n"
            f"{config.DISCLAIMER}\n"
            "Apresente a resposta final em formato JSON com as chaves: "
            "probability, risk_classification, suggested_protocols, disclaimer."
        ),
        handoffs=[handoff(analista_risco)],
    )
