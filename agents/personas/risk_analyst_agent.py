"""
Agente Analista de Risco — invoca o modelo supervisionado (.joblib).

Responsabilidade: receber dados clínicos estruturados, chamar `predict_risk_tool`
e encaminhar ao Especialista em Protocolos via handoff.
"""

from __future__ import annotations


def build_risk_analyst_agent(especialista_protocolos):
    """Recebe a instância do agente especialista para registrar o handoff."""
    from agents import Agent, handoff
    from agents.tools.risk_predictor import predict_risk_tool

    return Agent(
        name="Analista_de_Risco",
        instructions=(
            "Você é o Agente Analista de Risco do sistema CardioIA. "
            "Sua responsabilidade é receber os dados clínicos do paciente, "
            "invocar a tool predict_risk_tool com os valores numéricos e "
            "retornar o resultado da predição. "
            "Após obter o resultado, faça handoff para o Especialista em Protocolos "
            "passando a classificação de risco obtida."
        ),
        tools=[predict_risk_tool],
        handoffs=[handoff(especialista_protocolos)],
    )
