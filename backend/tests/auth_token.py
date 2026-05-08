import base64
import json
import time


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def build_test_jwt(*, tid="fiap-tenant", aud="cardioia-api", iss=None, exp_offset_sec=3600, sub="user-1"):
    if iss is None:
        iss = f"https://login.microsoftonline.com/{tid}/v2.0"
    header = {"alg": "none", "typ": "JWT"}
    payload = {
        "sub": sub,
        "tid": tid,
        "aud": aud,
        "iss": iss,
        "exp": int(time.time()) + exp_offset_sec,
        "name": "Aluno FIAP",
        "preferred_username": "aluno@fiap.local",
    }
    return f"{_b64url(json.dumps(header).encode())}.{_b64url(json.dumps(payload).encode())}.sig"
