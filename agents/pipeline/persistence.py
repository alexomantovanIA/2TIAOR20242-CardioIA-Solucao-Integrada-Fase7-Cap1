"""Persistência de logs de execução (disco local + opcional S3 / LocalStack)."""

from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def save_execution_log(patient_data: dict, recommendation: dict, trace: list) -> Path:
    """
    Grava JSON em agents/logs/ e, se configurado, envia cópia para S3 (AWS ou LocalStack).

    Variáveis de ambiente opcionais:
        CARDIOIA_S3_LOG_BUCKET — nome do bucket
        AWS_ENDPOINT_URL — ex.: http://localstack:4566 (LocalStack)
        AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION — credenciais padrão boto3
    """
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(exist_ok=True)
    stem = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    log_path = logs_dir / f"{stem}_execution.json"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "source": "orchestrator",
        "source_ml_inference": "ml_agent",
        "patient_input": patient_data,
        "final_recommendation": recommendation,
        "agents_trace": trace,
        "governance": recommendation.get("governance"),
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, ensure_ascii=False, indent=2)

    _maybe_upload_log_to_s3(log_path)
    return log_path


def _maybe_upload_log_to_s3(local_path: Path) -> None:
    bucket = os.getenv("CARDIOIA_S3_LOG_BUCKET", "").strip()
    if not bucket:
        return
    try:
        import boto3
    except ImportError:
        logger.warning("boto3 não instalado; upload S3 ignorado.")
        return

    endpoint_url = os.getenv("AWS_ENDPOINT_URL", "").strip() or None
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    try:
        client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
            region_name=region,
        )
        key = f"cardioia-logs/{local_path.name}"
        client.upload_file(str(local_path), bucket, key)
        logger.info("Log enviado para s3://%s/%s", bucket, key)
    except Exception as exc:
        logger.warning("Falha ao enviar log para S3 (continua apenas em disco): %s", exc)
