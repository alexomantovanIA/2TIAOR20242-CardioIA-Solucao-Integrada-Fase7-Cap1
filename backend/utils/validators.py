import re

MIN_MESSAGE_LENGTH = 2
MAX_MESSAGE_LENGTH = 1000


def validate_message(message):
    if not isinstance(message, str):
        return False, "A mensagem deve ser uma string."

    stripped = message.strip()

    if len(stripped) < MIN_MESSAGE_LENGTH:
        return False, "A mensagem deve conter pelo menos 2 caracteres."

    if len(stripped) > MAX_MESSAGE_LENGTH:
        return False, f"A mensagem deve conter no maximo {MAX_MESSAGE_LENGTH} caracteres."

    return True, ""


def sanitize_message(message):
    text = message.strip()
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text
