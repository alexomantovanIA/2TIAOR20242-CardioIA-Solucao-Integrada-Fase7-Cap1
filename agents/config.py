import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

_ROOT = Path(__file__).parent.parent
MODEL_PATH: str = str(_ROOT / "ml" / "modelo_risco_cardiaco.joblib")

# Limites superiores exclusivos: [0.0, 0.3) → baixo, [0.3, 0.7) → médio, [0.7, 1.0] → alto
RISK_THRESHOLDS: dict = {"baixo_max": 0.3, "medio_max": 0.7}

PROTOCOLS_PATH: str = str(Path(__file__).parent / "data" / "protocols.json")

# Aviso único da saída preditiva Fase 6 (modelo + multiagentes). O chat Fase 5 usa
# backend.models.message_models.DISCLAIMER (âmbito conversacional distinto).
DISCLAIMER: str = (
    "AVISO: Esta análise é gerada por um sistema acadêmico simulado (CardioIA — FIAP). "
    "Não substitui avaliação médica profissional. "
    "Em situações de emergência, ligue para o SAMU (192)."
)
