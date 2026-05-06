"""Garante que os builders de agentes importam sem erro (SDK + tools disponíveis)."""


def test_persona_builders_are_callable():
    from agents.personas import (
        build_orchestrator_agent,
        build_protocol_specialist_agent,
        build_risk_analyst_agent,
    )

    spec = build_protocol_specialist_agent()
    analyst = build_risk_analyst_agent(spec)
    orch = build_orchestrator_agent(analyst)
    assert spec.name == "Especialista_em_Protocolos"
    assert analyst.name == "Analista_de_Risco"
    assert orch.name == "Orquestrador"
