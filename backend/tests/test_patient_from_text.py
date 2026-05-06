from backend.utils.patient_from_text import build_predictive_suggestion, extract_patient_fields_from_text


def test_extract_partial():
    text = "Tenho 62 anos e minha frequência cardíaca está em 88 bpm."
    found = extract_patient_fields_from_text(text)
    assert found.get("idade") == 62
    assert found.get("freq_cardiaca") == 88


def test_extract_pulso_and_oximetria():
    text = "Paciente com pulso 92 e oximetria 96%."
    found = extract_patient_fields_from_text(text)
    assert found.get("freq_cardiaca") == 92
    assert found.get("spo2") == 96.0


def test_build_suggestion_ready():
    text = (
        "Paciente com 50 anos, FC 80 bpm, SpO2 97%, "
        "carga do sistema 0.3 e disponibilidade de recursos 0.7"
    )
    s = build_predictive_suggestion(text)
    assert s is not None
    assert s["ready_for_predict"] is True
    assert s["patient_payload"]["idade"] == 50
    assert s["missing_fields"] == []
