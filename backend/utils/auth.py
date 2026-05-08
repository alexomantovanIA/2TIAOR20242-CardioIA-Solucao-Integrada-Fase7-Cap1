import base64
import json
import time


class AuthError(Exception):
    pass


def _b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def parse_jwt_without_signature(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise AuthError("Token JWT malformado.")
    try:
        payload = json.loads(_b64url_decode(parts[1]).decode("utf-8"))
    except Exception as exc:
        raise AuthError("Payload JWT inválido.") from exc
    if not isinstance(payload, dict):
        raise AuthError("Payload JWT inválido.")
    return payload


def validate_entra_claims(payload: dict, *, tenant_id: str, audience: str, issuer: str) -> dict:
    token_tid = str(payload.get("tid") or "")
    token_aud = str(payload.get("aud") or "")
    token_iss = str(payload.get("iss") or "")
    token_sub = str(payload.get("sub") or "")
    token_exp = payload.get("exp")

    if not token_sub:
        raise AuthError("Token sem subject (sub).")
    if token_tid != tenant_id:
        raise AuthError("Tenant inválido.")
    if token_aud != audience:
        raise AuthError("Audience inválida.")
    if issuer and token_iss != issuer:
        raise AuthError("Issuer inválido.")
    if token_exp is None:
        raise AuthError("Token sem expiração (exp).")
    try:
        if int(token_exp) <= int(time.time()):
            raise AuthError("Token expirado.")
    except ValueError as exc:
        raise AuthError("Campo exp inválido.") from exc

    return {
        "subject": token_sub,
        "tenant_id": token_tid,
        "name": payload.get("name"),
        "email": payload.get("preferred_username") or payload.get("email"),
        "roles": payload.get("roles") or [],
    }
