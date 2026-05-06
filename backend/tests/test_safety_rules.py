import pytest
from backend.utils.safety_rules import check_urgency, URGENCY_RESPONSE


def test_urgency_dor_intensa_peito():
    is_urgent, keywords = check_urgency("Estou com dor intensa no peito")
    assert is_urgent is True
    assert len(keywords) > 0


def test_urgency_infarto():
    is_urgent, keywords = check_urgency("Acho que estou tendo um infarto")
    assert is_urgent is True
    assert "infarto" in keywords


def test_urgency_desmaio():
    is_urgent, keywords = check_urgency("Desmaiei no trabalho hoje")
    assert is_urgent is True


def test_urgency_falta_ar_intensa():
    is_urgent, keywords = check_urgency("Estou com falta de ar intensa")
    assert is_urgent is True


def test_urgency_suor_frio():
    is_urgent, keywords = check_urgency("Estou com suor frio e muito mal")
    assert is_urgent is True


def test_no_urgency_palpitacao_leve():
    is_urgent, keywords = check_urgency("Tenho palpitacao leve ha 2 dias")
    assert is_urgent is False
    assert keywords == []


def test_no_urgency_saudacao():
    is_urgent, keywords = check_urgency("Ola, bom dia!")
    assert is_urgent is False


def test_no_urgency_pergunta_ecg():
    is_urgent, keywords = check_urgency("O que e um ECG?")
    assert is_urgent is False


def test_urgency_combination_dor_peito_falta_ar():
    is_urgent, keywords = check_urgency("Dor no peito com falta de ar")
    assert is_urgent is True


def test_urgency_handles_accents():
    is_urgent, keywords = check_urgency("Dor intensa no peito e parada cardíaca")
    assert is_urgent is True


def test_urgency_response_exists():
    assert URGENCY_RESPONSE != ""
    assert "atendimento" in URGENCY_RESPONSE.lower() or "SAMU" in URGENCY_RESPONSE


def test_no_urgency_exame():
    is_urgent, keywords = check_urgency("Quero saber sobre ecocardiograma")
    assert is_urgent is False
