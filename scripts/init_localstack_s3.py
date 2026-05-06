#!/usr/bin/env python3
"""
Cria o bucket S3 no LocalStack (Docker) antes de subir o Flask.

Variáveis: AWS_ENDPOINT_URL, CARDIOIA_S3_LOG_BUCKET (default: cardioia-logs).
Se AWS_ENDPOINT_URL não estiver definido, termina sem efeito (desenvolvimento local sem Docker).
"""
from __future__ import annotations

import os
import sys
import time
import urllib.error
import urllib.request


def _wait_localstack(url: str, max_wait: int = 60) -> bool:
    deadline = time.time() + max_wait
    health = url.rstrip("/") + "/_localstack/health"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health, timeout=3) as r:
                if r.status == 200:
                    return True
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(2)
    return False


def main() -> int:
    endpoint = os.getenv("AWS_ENDPOINT_URL", "").strip()
    if not endpoint:
        return 0

    base = endpoint.rstrip("/")
    if not _wait_localstack(base):
        print("LocalStack não respondeu a tempo; continua mesmo assim.", file=sys.stderr)

    try:
        import boto3
        from botocore.exceptions import ClientError
    except ImportError:
        print("boto3 ausente; não é possível criar bucket.", file=sys.stderr)
        return 0

    bucket = os.getenv("CARDIOIA_S3_LOG_BUCKET", "cardioia-logs").strip()
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=region,
    )
    try:
        if region == "us-east-1":
            client.create_bucket(Bucket=bucket)
        else:
            client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"Bucket criado: {bucket}")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            print(f"Bucket já existe: {bucket}")
        else:
            print(f"Aviso ao criar bucket: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
