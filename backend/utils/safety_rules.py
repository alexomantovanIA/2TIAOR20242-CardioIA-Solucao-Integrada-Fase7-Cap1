import re

URGENCY_KEYWORDS = [
    "dor intensa no peito",
    "dor forte no peito",
    "aperto forte no peito",
    "pressao forte no peito",
    "falta de ar intensa",
    "falta de ar forte",
    "nao consigo respirar",
    "desmaio",
    "desmaiei",
    "perda de consciencia",
    "perdi a consciencia",
    "infarto",
    "avc",
    "parada cardiaca",
    "parada cardíaca",
    "suor frio",
    "dor irradiando para o braco",
    "dor no braco esquerdo",
    "formigamento no braco",
    "convulsao",
]

URGENCY_COMBINATIONS = [
    (["dor no peito", "dor toracica", "aperto no peito"], ["falta de ar", "suor", "nausea", "braco"]),
    (["tontura", "vertigem"], ["desmaio", "perda de consciencia"]),
]

URGENCY_RESPONSE = (
    "ATENCAO: Os sintomas que voce relatou podem indicar uma situacao de urgencia cardiovascular. "
    "Procure atendimento medico imediatamente ou ligue para o SAMU (192). "
    "Este assistente nao substitui avaliacao profissional e nao pode confirmar diagnosticos. "
    "Em caso de dor intensa no peito, falta de ar ou desmaio, nao aguarde: busque ajuda agora."
)


def _normalize(text):
    text = text.lower()
    replacements = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u", "ü": "u",
        "ç": "c",
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text


def check_urgency(message):
    normalized = _normalize(message)

    detected = []
    for keyword in URGENCY_KEYWORDS:
        if keyword in normalized:
            detected.append(keyword)

    if detected:
        return True, detected

    for group_a, group_b in URGENCY_COMBINATIONS:
        has_a = any(kw in normalized for kw in group_a)
        has_b = any(kw in normalized for kw in group_b)
        if has_a and has_b:
            combined = [kw for kw in group_a + group_b if kw in normalized]
            return True, combined

    return False, []
