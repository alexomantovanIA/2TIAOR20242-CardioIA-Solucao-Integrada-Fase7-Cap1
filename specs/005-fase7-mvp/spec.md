# Feature Specification: Fase 7 MVP Integrado (sem IR ALÉM)

**Feature Branch**: `005-fase7-mvp`  
**Created**: 2026-05-08  
**Status**: Draft  
**Input**: User description: "/speckit-implement preciso fazer a fase 7 para esse projeto. baseado nos requisitos no arquivo .fiap/fases_unificadas/fase07_enunciado_avaliacao.md, lembrando que quero a nota maxima, sem o ir alem."

## Clarifications

### Session 2026-05-08

- Q: Qual abordagem de login deve ser adotada para avaliação da Fase 7? → A: Login real com autenticação no backend usando Entra ID.
- Q: A aprovação técnica pode ocorrer sem URL pública/APK final? → A: Não; aprovação exige URL pública e APK final acessíveis.
- Q: Qual escopo de tenant será usado no Entra ID? → A: Single-tenant do projeto/turma.
- Q: Quais endpoints devem ser protegidos por autenticação? → A: Todos `/api/*` exceto `GET /health`.
- Q: Qual meta de latência para `full-analysis` em demo? → A: p95 <= 3s em ambiente de demonstração.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy profissional Web e Mobile (Priority: P1)

Como avaliador/tutor, quero acessar a aplicação Web publicada e validar o APK funcional
para confirmar que a solução foi distribuída de forma profissional.

**Why this priority**: este item vale a maior parcela da nota e é obrigatório para avaliação.

**Independent Test**: validar `vercel.json`, `app.json`, `eas.json`, executar build web local,
rodar `expo-doctor` e confirmar instruções de deploy/build no README.

**Acceptance Scenarios**:

1. **Given** o projeto web configurado, **When** o repositório recebe push, **Then** o deploy
   Web pode ser automatizado e suporta rotas SPA.
2. **Given** o projeto mobile configurado, **When** é executado build `preview`, **Then**
   um APK Android pode ser gerado e instalado para validação.
3. **Given** um usuário válido, **When** ele autentica via Entra ID, **Then** o acesso às
   funcionalidades protegidas é permitido no backend e nas interfaces.

---

### User Story 2 - Integração funcional de ponta a ponta (Priority: P1)

Como usuário acadêmico, quero que dados simulados de sensores alimentem o backend e cheguem
às interfaces com recomendação de risco para demonstrar o fluxo completo da Fase 7.

**Why this priority**: este é o núcleo técnico da fase e responde ao critério de unificação.

**Independent Test**: executar testes de integração do backend e verificar endpoints
`/api/iot/ingest`, `/api/dashboard/summary` e `/api/full-analysis`.

**Acceptance Scenarios**:

1. **Given** uma leitura IoT válida, **When** é enviada ao backend, **Then** o sistema
   persiste a leitura e retorna payload para análise preditiva.
2. **Given** leitura IoT e mensagem clínica simulada, **When** `full-analysis` é chamado,
   **Then** o backend retorna conversa, classificação de risco e disclaimer acadêmico.

---

### User Story 3 - Evidências e documentação de avaliação (Priority: P2)

Como equipe, queremos documentação clara (README + relatório + arquitetura) para comprovar
os entregáveis obrigatórios e facilitar a correção com nota máxima.

**Why this priority**: sem evidência clara, funcionalidades prontas podem não ser pontuadas.

**Independent Test**: revisar README e docs para checklist de entrega, execução local e
artefatos obrigatórios sem referência aos itens "IR ALÉM".

**Acceptance Scenarios**:

1. **Given** os artefatos de projeto, **When** o tutor acessa o repositório, **Then**
   encontra instruções claras, links e evidências de cada entregável obrigatório.

---

### Edge Cases

- API IoT indisponível durante simulação MicroPython.
- Build mobile falha por credenciais Expo ausentes.
- Backend sem modelo carregado para recomendação.
- Frontend sem variável de ambiente da API configurada.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Sistema MUST publicar front-end Web em ambiente de deploy com suporte SPA.
- **FR-002**: Sistema MUST permitir geração de APK Android via profile `preview` do EAS.
- **FR-003**: Sistema MUST expor backend Python integrador com endpoints de chat, risco e IoT.
- **FR-004**: Sistema MUST simular captura de sensores em MicroPython com status visual.
- **FR-005**: Sistema MUST documentar arquitetura Sensor -> MicroPython -> Backend -> IA -> UI.
- **FR-006**: Sistema MUST fornecer README com instruções de execução e validação da entrega.
- **FR-007**: Sistema MUST NOT incluir escopo de "IR ALÉM" como requisito para conclusão da fase.
- **FR-008**: Sistema MUST implementar autenticação real via Entra ID para fluxo de login Web/Mobile.
- **FR-009**: Sistema MUST proteger endpoints sensíveis com validação de token e controle de acesso.
- **FR-010**: Sistema MUST usar configuração Entra ID single-tenant para autenticação do MVP.
- **FR-011**: Sistema MUST exigir autenticação em todos os endpoints `/api/*`, exceto `GET /health`.

### Key Entities *(include if feature involves data)*

- **IoTReading**: leitura simulada contendo `heart_rate`, `temperature`, `spo2`, `timestamp`.
- **PatientPayload**: representação normalizada do paciente para entrada no pipeline preditivo.
- **RiskRecommendation**: saída de risco com classificação, probabilidade e protocolos sugeridos.
- **DeliveryEvidence**: conjunto de links/prints/provas de deploy, apk e simulação.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos endpoints essenciais da integração (`health`, `chat`, `predict`, `iot`)
  respondem conforme contratos esperados pelos testes.
- **SC-002**: Build Web (`npm run build`) conclui sem erro no ambiente de CI/local.
- **SC-003**: `npx expo-doctor` conclui sem erros críticos e `eas.json` possui profile `preview` APK.
- **SC-004**: README cobre todos os entregáveis obrigatórios da Fase 7 sem dependência dos
  itens opcionais "IR ALÉM".
- **SC-005**: 100% dos acessos a rotas protegidas sem token válido retornam status de não autorizado.
- **SC-006**: URL pública do Web e link/QR do APK final estão acessíveis no momento da avaliação.
- **SC-007**: 100% dos tokens aceitos no backend pertencem ao tenant configurado do projeto.
- **SC-008**: 100% das chamadas sem token válido para `/api/*` (exceto `/health`) retornam não autorizado.
- **SC-009**: Endpoint `POST /api/full-analysis` atende p95 <= 3s no ambiente de demonstração.

## Assumptions

- O deploy público (URL final e link do APK) MUST estar concluído antes da revisão final.
- Dados usados para demonstração são simulados e não representam prontuário real.
- O escopo desta entrega é Fase 7 obrigatória, excluindo IR ALÉM 1 e 2.
- A infraestrutura de nuvem (Vercel/Expo/Wokwi) está disponível para validação final manual.
