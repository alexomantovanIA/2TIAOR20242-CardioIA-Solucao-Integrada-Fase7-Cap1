import json
import math
import os
from datetime import datetime, timezone
from threading import Lock

from backend.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LATEST_READING_PATH = os.path.join(DATA_DIR, "latest_iot_reading.json")

ACADEMIC_DISCLAIMER = "Sistema acadêmico. Não substitui avaliação médica."

_lock = Lock()
_latest_reading = None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _coerce_float(value, field: str) -> float:
    if value is None or value == "":
        raise ValueError(f"Campo obrigatorio ausente: {field}")
    try:
        coerced = float(str(value).replace(",", "."))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Campo invalido: {field}") from exc
    if not math.isfinite(coerced):
        raise ValueError(f"Campo invalido: {field}")
    return coerced


def classify_iot_status(heart_rate: float, temperature: float, spo2: float) -> str:
    if heart_rate < 45 or heart_rate > 130 or spo2 < 90 or temperature >= 38.5:
        return "critico"
    if heart_rate < 55 or heart_rate > 100 or spo2 < 95 or temperature >= 37.8:
        return "atencao"
    return "normal"


def normalize_iot_reading(body: dict) -> dict:
    if not isinstance(body, dict):
        raise ValueError("Corpo JSON invalido.")

    device_id = str(body.get("device_id") or "").strip()
    if not device_id:
        raise ValueError("Campo obrigatorio ausente: device_id")

    heart_rate = _coerce_float(body.get("heart_rate"), "heart_rate")
    temperature = _coerce_float(body.get("temperature"), "temperature")
    spo2 = _coerce_float(body.get("spo2"), "spo2")

    if not 30 <= heart_rate <= 220:
        raise ValueError("heart_rate fora do intervalo aceito [30, 220].")
    if not 30 <= temperature <= 45:
        raise ValueError("temperature fora do intervalo aceito [30, 45].")
    if not 70 <= spo2 <= 100:
        raise ValueError("spo2 fora do intervalo aceito [70, 100].")

    timestamp = str(body.get("timestamp") or _utc_now_iso()).strip()
    status = classify_iot_status(heart_rate, temperature, spo2)
    return {
        "device_id": device_id,
        "heart_rate": round(heart_rate, 1),
        "temperature": round(temperature, 1),
        "spo2": round(spo2, 1),
        "timestamp": timestamp,
        "status": status,
    }


def save_latest_iot_reading(reading: dict) -> dict:
    global _latest_reading
    os.makedirs(DATA_DIR, exist_ok=True)
    with _lock:
        _latest_reading = dict(reading)
        with open(LATEST_READING_PATH, "w", encoding="utf-8") as fp:
            json.dump(_latest_reading, fp, ensure_ascii=False, indent=2)
    return dict(reading)


def get_latest_iot_reading() -> dict | None:
    global _latest_reading
    with _lock:
        if _latest_reading:
            return dict(_latest_reading)

    if not os.path.exists(LATEST_READING_PATH):
        return None

    try:
        with open(LATEST_READING_PATH, "r", encoding="utf-8") as fp:
            loaded = json.load(fp)
    except (OSError, json.JSONDecodeError):
        return None

    with _lock:
        _latest_reading = loaded
    return dict(loaded)


def patient_from_iot(reading: dict, overrides: dict | None = None) -> dict:
    overrides = overrides or {}
    status = reading.get("status") or classify_iot_status(
        reading["heart_rate"],
        reading["temperature"],
        reading["spo2"],
    )
    defaults_by_status = {
        "normal": {"carga_sistema": 0.25, "disponibilidade_recursos": 0.85},
        "atencao": {"carga_sistema": 0.55, "disponibilidade_recursos": 0.55},
        "critico": {"carga_sistema": 0.85, "disponibilidade_recursos": 0.25},
    }
    defaults = defaults_by_status.get(status, defaults_by_status["atencao"])
    return {
        "idade": int(overrides.get("idade") or Config.DEFAULT_PATIENT_AGE),
        "freq_cardiaca": int(round(float(reading["heart_rate"]))),
        "spo2": float(reading["spo2"]),
        "carga_sistema": float(overrides.get("carga_sistema", defaults["carga_sistema"])),
        "disponibilidade_recursos": float(
            overrides.get(
                "disponibilidade_recursos",
                defaults["disponibilidade_recursos"],
            )
        ),
    }
