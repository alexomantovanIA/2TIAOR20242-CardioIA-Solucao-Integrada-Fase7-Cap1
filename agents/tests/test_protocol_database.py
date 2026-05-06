"""
T014 — Testes para agents/tools/protocol_database.py
Escrever ANTES da implementação; verificar que falham primeiro.
"""
import pytest


class TestGetProtocols:

    def test_baixo_returns_list(self):
        from agents.tools.protocol_database import get_protocols
        result = get_protocols("baixo")
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_medio_returns_list(self):
        from agents.tools.protocol_database import get_protocols
        result = get_protocols("médio")
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_alto_returns_list(self):
        from agents.tools.protocol_database import get_protocols
        result = get_protocols("alto")
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_protocol_has_required_keys(self):
        from agents.tools.protocol_database import get_protocols
        for nivel in ["baixo", "médio", "alto"]:
            protocols = get_protocols(nivel)
            for p in protocols:
                assert "protocol_id" in p, f"protocol_id ausente em nível {nivel}"
                assert "nome" in p, f"nome ausente em nível {nivel}"
                assert "acoes" in p, f"acoes ausente em nível {nivel}"

    def test_acoes_is_nonempty_list(self):
        from agents.tools.protocol_database import get_protocols
        for nivel in ["baixo", "médio", "alto"]:
            for p in get_protocols(nivel):
                assert isinstance(p["acoes"], list)
                assert len(p["acoes"]) >= 1

    def test_invalid_classification_returns_empty_list(self):
        from agents.tools.protocol_database import get_protocols
        result = get_protocols("invalido")
        assert result == []

    def test_invalid_classification_does_not_raise(self):
        from agents.tools.protocol_database import get_protocols
        try:
            get_protocols("nao_existe")
        except Exception as e:
            pytest.fail(f"get_protocols levantou exceção inesperada: {e}")

    def test_protocol_id_format(self):
        from agents.tools.protocol_database import get_protocols
        for nivel in ["baixo", "médio", "alto"]:
            for p in get_protocols(nivel):
                assert p["protocol_id"].startswith("PROT-"), \
                    f"protocol_id deve iniciar com PROT-, obtido: {p['protocol_id']}"
