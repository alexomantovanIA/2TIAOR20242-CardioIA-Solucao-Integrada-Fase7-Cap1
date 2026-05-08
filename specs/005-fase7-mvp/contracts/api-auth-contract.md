# API Contract - Authentication and Access Control

## Scope

Este contrato define o comportamento de autenticacao/autorizacao para o MVP da Fase 7.

## Access Policy

- `GET /health`: publico (sem token).
- Todos os demais endpoints sob `/api/*`: autenticados com Bearer token Entra ID.

## Token Requirements

- Provider: Microsoft Entra ID.
- Tenant mode: single-tenant.
- Validation (backend):
  - assinatura valida;
  - token nao expirado;
  - `tid` igual ao tenant configurado;
  - audience compativel com API configurada.

## Unauthorized Responses

- Missing token: `401 Unauthorized`
- Invalid/expired token: `401 Unauthorized`
- Tenant mismatch: `401 Unauthorized`
- Authenticated sem permissao de escopo/papel (se aplicavel): `403 Forbidden`

## Endpoint Security Matrix

| Endpoint | Method | Auth Required | Notes |
|---|---|---|---|
| `/health` | GET | No | endpoint de monitoramento |
| `/api/chat` | POST | Yes | interacao conversacional |
| `/api/predict-risk` | POST | Yes | inferencia de risco |
| `/api/iot/ingest` | POST | Yes | ingestao de leitura IoT |
| `/api/dashboard/summary` | GET | Yes | resumo para UI |
| `/api/patient/latest` | GET | Yes | ultimo payload normalizado |
| `/api/full-analysis` | POST | Yes | fluxo integrado com meta p95 <= 3s |

## Acceptance Tests (Contract-level)

1. Request sem token para `/api/full-analysis` retorna `401`.
2. Request com token invalido para endpoint `/api/*` retorna `401`.
3. Request com token de tenant diferente retorna `401`.
4. Request com token valido para `/api/dashboard/summary` retorna `200`.
5. Request sem token para `/health` retorna `200`.
