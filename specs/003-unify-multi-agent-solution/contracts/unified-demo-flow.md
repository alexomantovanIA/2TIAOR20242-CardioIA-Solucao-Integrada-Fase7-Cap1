# Contract: Roteiro de demonstração unificado (CardioIA fases 1–6)

**Version**: 1.1  
**Owner**: Equipe CardioIA / FIAP  
**Consumers**: avaliadoras, integrantes

---

## Objetivo

Definir a **ordem canônica** e o **estado final válido** da demonstração que prova coesão entre a solução das fases 1–5 e a extensão da fase 6 (spec FR-003, FR-006).

---

## Pré-condições globais

1. Repositório clonado; ambiente virtual ativado; dependências instaladas conforme `README.md`.
2. Arquivo `.env` (ou equivalente) disponível quando o roteiro exigir credenciais — o roteiro deve declarar quais passos são **opcionais** se credenciais estiverem ausentes (constituição IV).

---

## Passos obrigatórios (ordem fixa)

| ID | Título | Resultado observável |
|----|--------|-------------------------|
| 1 | Sanidade do backend | Resposta HTTP OK do endpoint de saúde documentado |
| 2 | Fluxo conversacional mínimo | Pelo menos uma interação de chat retorna resposta com aviso educacional visível (texto ou JSON conforme cliente de teste) |
| 3 | Verificação de segurança documentada | Palavra-chave de urgência de teste (definida no roteiro) produz resposta com encaminhamento SAMU 192, sem depender do Watson para o texto final da urgência |
| 4 | Presença do modelo treinado | Ficheiro `.joblib` referenciado existe em `ml/` |
| 5 | Predição determinística (sem LLM) | Execução documentada de `predict_risk` ou célula equivalente produz `probability` e `risk_classification` coerentes com o glossário |
| 6 | Pipeline multiagente | Com `OPENAI_API_KEY` válida: execução de `python -m agents.main` termina com código 0 e imprime recomendação com `disclaimer` |
| 7 | Artefato de auditoria | Existe ficheiro JSON recente em `agents/logs/` com entrada e recomendação final (conteúdo mínimo definido no roteiro) |

---

## Extensões de produto (integração Fase 5 + 6) — v1.1

Recomendadas na demonstração completa do **mesmo** CardioIA (não substituem os passos 1–7); documentadas em `README.md` e `docs/passo_a_passo_execucao_local_fase6.md`.

| ID ext. | Título | Resultado observável |
|---------|--------|------------------------|
| EX-A | Health com prontidão Fase 6 | `GET /health` devolve JSON com `fase6_prediction.predict_risk_ready` e campos associados (`backend/utils/prediction_readiness.py`) |
| EX-B | Predição via HTTP | Com Flask em execução: `POST /api/predict-risk` com `mode=ml_only` e cinco campos devolve `recommendation` com `governance` |
| EX-C | Lote simulado (IR ALÉM 2) | `python -m agents.batch_process` gera `agents/logs/batch_last_summary.json` |

---

## Estados finais válidos

- **Completo (laboratório ideal)**: passos 1–7 cumpridos na mesma sessão.
- **Completo com LLM indisponível**: passos 1–5 + documentação de que 6 falhou com mensagem esperada; avaliadoras marcam exceção no checklist conforme spec (edge case modelo/LLM).

---

## Regras de alteração

- Novos passos **DEVEM** receber ID novo; não reordenar IDs após publicação sem bump de versão do contrato.
- O roteiro de apresentação, quando utilizado, deve listar os mesmos IDs na mesma ordem.
