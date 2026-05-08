# Tasks: Fase 7 MVP Integrado (Sem IR ALEM)

**Input**: Design documents from `/specs/005-fase7-mvp/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Incluidos para validar segurança (Entra ID), integração fim-a-fim e meta de desempenho (p95 <= 3s).

**Organization**: Tasks agrupadas por user story para implementação e validação independente.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: tarefa paralelizável (arquivos diferentes, sem dependência direta)
- **[Story]**: mapeamento para user story (`[US1]`, `[US2]`, `[US3]`)
- Todas as descrições incluem caminho de arquivo alvo

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: preparar baseline de ambiente e configuração de qualidade.

- [X] T001 Validar branch e artefatos de design em `specs/005-fase7-mvp/`
- [X] T002 [P] Revisar padrões de ignore em `.gitignore` e `.dockerignore`
- [X] T003 [P] Atualizar checklist de validação operacional em `docs/fase7_checklist_entrega.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: infraestrutura obrigatória de autenticação e observabilidade mínima.

**CRITICAL**: nenhuma user story deve avançar sem esta fase.

- [X] T004 Implementar configuração Entra ID single-tenant em `backend/config.py`
- [X] T005 [P] Criar utilitário de validação JWT (issuer/audience/tid) em `backend/utils/auth.py`
- [X] T006 Aplicar middleware/guard para `/api/*` (exceto `/health`) em `backend/app.py`
- [X] T007 [P] Documentar variáveis de ambiente de autenticação em `README.md`
- [X] T008 [P] Criar testes de acesso sem token e com token inválido em `backend/tests/test_auth_guards.py`
- [X] T009 [P] Criar teste de tenant mismatch em `backend/tests/test_auth_tenant_validation.py`

**Checkpoint**: autenticação base pronta e cobertura de segurança inicial validada.

---

## Phase 3: User Story 1 - Deploy profissional Web e Mobile (Priority: P1) 🎯 MVP

**Goal**: garantir distribuição profissional com Web pública e APK funcional.

**Independent Test**: build web + expo-doctor + validação de configs + checklist de links finais.

### Tests for User Story 1

- [X] T010 [P] [US1] Validar build web em CI/local com script em `apps/web/package.json`
- [X] T011 [P] [US1] Validar saúde mobile com `expo-doctor` em `apps/mobile/package.json`

### Implementation for User Story 1

- [X] T012 [US1] Revisar rewrite SPA em `apps/web/vercel.json`
- [X] T013 [US1] Revisar `android.package` em `apps/mobile/app.json`
- [X] T014 [US1] Revisar profile `preview` APK em `apps/mobile/eas.json`
- [X] T015 [US1] Atualizar instruções de deploy Web e APK em `README.md`
- [X] T016 [US1] Criar gate de evidência obrigatória (URL web + link/QR APK) em `docs/fase7_checklist_entrega.md`

**Checkpoint**: User Story 1 pronta para validação de entrega externa (deploy + APK).

---

## Phase 4: User Story 2 - Integração funcional de ponta a ponta (Priority: P1)

**Goal**: validar fluxo IoT -> Backend -> IA -> UI com segurança aplicada.

**Independent Test**: testes de integração autenticados em endpoints críticos e simulação IoT funcional.

### Tests for User Story 2

- [X] T017 [P] [US2] Cobrir `/api/iot/ingest` autenticado em `backend/tests/test_integration_endpoints.py`
- [X] T018 [P] [US2] Cobrir `/api/dashboard/summary` autenticado em `backend/tests/test_integration_endpoints.py`
- [X] T019 [P] [US2] Cobrir `/api/full-analysis` autenticado em `backend/tests/test_conversational_predictive_flow.py`
- [X] T020 [P] [US2] Validar `/health` público em `backend/tests/test_healthcheck.py`

### Implementation for User Story 2

- [X] T021 [US2] Integrar validação de identidade do usuário em `backend/routes/integration_routes.py`
- [X] T022 [US2] Integrar validação de token em `backend/routes/chat_routes.py`
- [X] T023 [US2] Integrar validação de token em `backend/routes/prediction_routes.py`
- [X] T024 [US2] Ajustar payload IoT para compatibilidade com fluxo autenticado em `iot/main.py`
- [X] T025 [US2] Atualizar documentação do fluxo fim-a-fim em `docs/arquitetura_final.mmd`

**Checkpoint**: integração fim-a-fim autenticada e funcional.

---

## Phase 5: User Story 3 - Evidências e documentação de avaliação (Priority: P2)

**Goal**: consolidar evidências formais para maximizar nota na rubrica.

**Independent Test**: revisão de README/docs com todos os artefatos obrigatórios preenchíveis.

### Tests for User Story 3

- [X] T026 [P] [US3] Criar checklist de conformidade de documentação em `docs/fase7_checklist_entrega.md`

### Implementation for User Story 3

- [X] T027 [US3] Consolidar matriz de entregáveis no `README.md`
- [X] T028 [US3] Garantir escopo “sem IR ALEM” explícito no `README.md`
- [X] T029 [US3] Validar consistência com contrato de autenticação em `specs/005-fase7-mvp/contracts/api-auth-contract.md`
- [X] T030 [US3] Atualizar roteiro de demonstração com etapa de login Entra ID em `docs/roteiro_video.md`

**Checkpoint**: documentação pronta para banca com rastreabilidade completa.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: fechar qualidade não funcional e validação final.

- [X] T031 [P] Medir p95 de `/api/full-analysis` e registrar evidência em `docs/relatorio_fase7.md`
- [X] T032 [P] Executar suíte final `pytest backend/tests agents/tests -q` e registrar resultado em `docs/relatorio_fase7.md`
- [X] T033 [P] Executar `npm run build` em `apps/web` e registrar evidência em `docs/relatorio_fase7.md`
- [X] T034 [P] Executar `npx expo-doctor` em `apps/mobile` e registrar evidência em `docs/relatorio_fase7.md`
- [X] T035 Revisar conformidade final com constituição em `.specify/memory/constitution.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup): inicia imediatamente
- Phase 2 (Foundational): depende da Phase 1 e bloqueia US1/US2/US3
- Phase 3 (US1), Phase 4 (US2), Phase 5 (US3): dependem da conclusão da Phase 2
- Phase 6 (Polish): depende da conclusão das fases de user story

### User Story Dependencies

- **US1 (P1)**: depende apenas de Foundational
- **US2 (P1)**: depende de Foundational; pode rodar em paralelo com US1 após gates de auth
- **US3 (P2)**: depende parcialmente de US1/US2 para consolidar evidências finais

### Within Each User Story

- Testes primeiro (T010-T011, T017-T020, T026)
- Depois implementação
- Fechar com checkpoint de história

### Parallel Opportunities

- T002, T003 paralelizáveis
- T005, T007, T008, T009 paralelizáveis
- T010 e T011 paralelizáveis
- T017-T020 paralelizáveis
- T031-T034 paralelizáveis

---

## Parallel Example: User Story 2

```bash
Task: "T017 [US2] Cobrir /api/iot/ingest autenticado em backend/tests/test_integration_endpoints.py"
Task: "T018 [US2] Cobrir /api/dashboard/summary autenticado em backend/tests/test_integration_endpoints.py"
Task: "T019 [US2] Cobrir /api/full-analysis autenticado em backend/tests/test_conversational_predictive_flow.py"
```

---

## Implementation Strategy

### MVP First (US1 + segurança mínima)

1. Concluir Setup + Foundational (auth Entra ID)
2. Concluir US1 (deploy e APK)
3. Validar entrega mínima de nota máxima

### Incremental Delivery

1. Add US2 para fluxo integrado autenticado
2. Add US3 para documentação/evidências
3. Executar Polish com meta p95 e validações finais


