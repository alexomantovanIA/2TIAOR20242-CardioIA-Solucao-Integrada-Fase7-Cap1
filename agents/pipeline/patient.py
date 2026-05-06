"""Validação de entrada do paciente (contrato numérico do modelo)."""

_FIELD_RANGES = {
    "idade": (18, 90),
    "freq_cardiaca": (40, 200),
    "spo2": (80.0, 100.0),
    "carga_sistema": (0.0, 1.0),
    "disponibilidade_recursos": (0.0, 1.0),
}

PATIENT_FIELD_RANGES = dict(_FIELD_RANGES)


def _validate_patient(data: dict) -> None:
    for field, (low, high) in _FIELD_RANGES.items():
        if field not in data:
            raise ValueError(f"Campo obrigatório ausente: '{field}'")
        val = data[field]
        if not (low <= val <= high):
            raise ValueError(
                f"Campo '{field}' fora do intervalo válido [{low}, {high}]: {val}"
            )


def validate_patient_data(data: dict) -> None:
    """Valida o dict do paciente (mesmas regras do pipeline). Levanta ValueError se inválido."""
    _validate_patient(data)
