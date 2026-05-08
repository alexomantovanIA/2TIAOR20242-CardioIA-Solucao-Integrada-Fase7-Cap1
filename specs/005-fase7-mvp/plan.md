# Implementation Plan: Fase 7 MVP Integrado (Nota Maxima sem IR ALEM)

**Branch**: `005-fase7-mvp` | **Date**: 2026-05-08 | **Spec**: `specs/005-fase7-mvp/spec.md`  
**Input**: Feature specification from `/specs/005-fase7-mvp/spec.md`

## Summary

Concluir a entrega obrigatoria da Fase 7 com foco em nota maxima: deploy web com CI/CD,
APK via Expo EAS, backend integrador com autenticacao Entra ID single-tenant, fluxo IoT
MicroPython -> backend -> IA -> interfaces, e evidencia objetiva para avaliacao.

## Technical Context

**Language/Version**: Python 3.11, TypeScript, React 19, React Native 0.81, MicroPython  
**Primary Dependencies**: Flask, pytest, Vite, Expo/EAS, Entra ID (OIDC/JWT), OpenAI Agents (pipeline)  
**Storage**: JSON/local para ultima leitura IoT + artefatos de build/documentacao  
**Testing**: `pytest backend/tests agents/tests -q`, `npm run build` (web), `npx expo-doctor` (mobile)  
**Target Platform**: Web deploy publico + Android APK + backend Python + Wokwi  
**Project Type**: Solucao integrada (backend/web/mobile/iot)  
**Performance Goals**: `POST /api/full-analysis` com p95 <= 3s em ambiente de demonstracao  
**Constraints**: Escopo sem IR ALEM; API protegida (`/api/*` exceto `/health`); single-tenant Entra ID  
**Scale/Scope**: Avaliacao academica Fase 7 com evidencia fim-a-fim obrigatoria

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Integracao fim-a-fim coberta pelo fluxo Sensor -> MicroPython -> Backend -> IA -> UI.
- ✅ Deploy profissional coberto por `apps/web/vercel.json`, `apps/mobile/app.json`, `apps/mobile/eas.json`.
- ✅ Seguranca de uso academico mantida com disclaimers e autenticacao real via Entra ID.
- ✅ Evidencias de qualidade previstas em testes e checklist de entrega.
- ✅ Documentacao/rastreabilidade cobertas por spec, plan, tasks, README e docs fase 7.

## Project Structure

### Documentation (this feature)

```text
specs/005-fase7-mvp/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── api-auth-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── app.py
├── routes/
├── services/
└── tests/

agents/
├── pipeline/
└── tests/

apps/
├── web/
│  ├── src/
│  └── vercel.json
└── mobile/
   ├── app.json
   └── eas.json

iot/
└── main.py
```

**Structure Decision**: manter arquitetura existente, adicionar contrato claro de autenticacao
e reforcar validacoes/documentacao para fechamento da rubrica obrigatoria da Fase 7.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Nenhuma | N/A | N/A |
