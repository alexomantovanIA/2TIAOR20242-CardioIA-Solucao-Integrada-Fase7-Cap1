# Research - Fase 7 MVP Integrado

## Decisao 1: Autenticacao real com Entra ID single-tenant

- Decision: usar Entra ID com configuracao single-tenant para Web e Mobile, com validacao
  de JWT no backend para todos os endpoints `/api/*` exceto `GET /health`.
- Rationale: atende o requisito de login real com baixo risco operacional e controle de
  seguranca previsivel para ambiente academico.
- Alternatives considered:
  - Login fake de demonstracao (rejeitado por nao atender decisao de clarificacao).
  - Multi-tenant Entra ID (rejeitado por ampliar superficie de risco e configuracao).

## Decisao 2: Regra de protecao de endpoints

- Decision: proteger todo endpoint de API (`/api/*`) e manter `GET /health` publico para
  observabilidade e monitoramento.
- Rationale: equilibrio entre seguranca e operabilidade (healthcheck sem credencial).
- Alternatives considered:
  - Proteger apenas endpoints de escrita (insuficiente para requisito de seguranca definido).
  - Proteger apenas `/api/full-analysis` (cobertura fraca para avaliacao).

## Decisao 3: Meta de desempenho em demonstracao

- Decision: estabelecer p95 <= 3s para `POST /api/full-analysis` em ambiente de demo.
- Rationale: meta objetiva, testavel e compatível com escopo MVP sem exigir otimizacoes
  avancadas fora da rubrica.
- Alternatives considered:
  - p95 <= 1s (alto risco de nao conformidade em ambiente academico).
  - Sem meta formal (reduz testabilidade da qualidade nao funcional).

## Decisao 4: Entrega de nota maxima sem IR ALEM

- Decision: excluir IR ALEM 1 e 2 do escopo e concentrar esforco nos 10 pontos obrigatorios.
- Rationale: alinhamento direto ao objetivo do usuario e reducao de risco de dispersao.
- Alternatives considered:
  - Implementar IR ALEM parcial (maior custo com baixo impacto na nota base).

## Decisao 5: Evidencia obrigatoria de aprovacao

- Decision: aprovacao exige URL publica da Web e link/QR do APK final acessiveis no momento
  da avaliacao.
- Rationale: decisao explicitamente definida nas clarificacoes e aderente ao enunciado.
- Alternatives considered:
  - Aprovar somente com evidencias locais (rejeitado pela decisao de clarificacao).
