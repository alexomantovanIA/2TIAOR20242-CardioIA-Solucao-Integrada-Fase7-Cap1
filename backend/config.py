import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    DEFAULT_PATIENT_AGE = int(os.getenv("DEFAULT_PATIENT_AGE", 55))
    AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"
    ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID", "fiap-tenant")
    ENTRA_AUDIENCE = os.getenv("ENTRA_AUDIENCE", "cardioia-api")
    ENTRA_ISSUER = os.getenv(
        "ENTRA_ISSUER",
        f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}/v2.0",
    )

    WATSON_API_KEY = os.getenv("WATSON_API_KEY", "")
    WATSON_URL = os.getenv("WATSON_URL", "")
    WATSON_ASSISTANT_ID = os.getenv("WATSON_ASSISTANT_ID", "")
    WATSON_ASSISTANT_VERSION = os.getenv("WATSON_ASSISTANT_VERSION", "2021-11-27")

    @classmethod
    def watson_configured(cls):
        return bool(cls.WATSON_API_KEY and cls.WATSON_URL and cls.WATSON_ASSISTANT_ID)
