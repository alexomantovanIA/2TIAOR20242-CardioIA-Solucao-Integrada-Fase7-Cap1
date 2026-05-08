# Data Model - Fase 7 MVP Integrado

## Entity: UserIdentity

- Description: identidade autenticada via Entra ID para acesso ao ecossistema.
- Fields:
  - `subject` (string, required): identificador unico do usuario no token.
  - `tenant_id` (string, required): tenant do Entra ID (single-tenant esperado).
  - `name` (string, optional): nome de exibicao.
  - `email` (string, optional): email institucional.
  - `roles` (array[string], optional): papeis para autorizacao.
- Validation rules:
  - token MUST ser valido e nao expirado.
  - `tenant_id` MUST corresponder ao tenant configurado do projeto.

## Entity: IoTReading

- Description: leitura de sinais vitais recebida do simulador MicroPython/Wokwi.
- Fields:
  - `device_id` (string, required)
  - `heart_rate` (integer, required)
  - `temperature` (number, required)
  - `spo2` (integer, required)
  - `timestamp` (string, required, ISO8601 ou epoch string)
  - `status` (enum: `normal|atencao|critico`, derived)
- Validation rules:
  - `heart_rate` MUST estar em faixa fisiologica simulada.
  - `spo2` MUST estar entre 0 e 100.

## Entity: PatientPayload

- Description: payload normalizado para inferencia de risco cardiaco.
- Fields:
  - `idade` (integer, required)
  - `freq_cardiaca` (integer, required)
  - `spo2` (number, required)
  - `carga_sistema` (number, required)
  - `disponibilidade_recursos` (number, required)
- Relationships:
  - derivado de `IoTReading` + overrides opcionais.
- Validation rules:
  - todos os campos MUST existir antes de chamar pipeline de predição.

## Entity: RiskRecommendation

- Description: resultado da analise preditiva com suporte conversacional.
- Fields:
  - `risk_classification` (enum: `baixo|medio|alto`, required)
  - `probability` (number, optional)
  - `suggested_protocols` (array, optional)
  - `governance` (object, optional)
  - `disclaimer` (string, required)
- State transitions:
  - `generated` -> `exposed_to_ui` -> `logged_for_evidence`.

## Entity: DeliveryEvidence

- Description: artefatos exigidos para avaliacao final da Fase 7.
- Fields:
  - `web_url` (string, required before final review)
  - `apk_link_or_qr` (string, required before final review)
  - `wokwi_url` (string, required)
  - `video_url` (string, required)
  - `report_pdf_ref` (string, required)
- Validation rules:
  - campos MUST estar preenchidos para aprovacao final.
