# Glossário unificado — CardioIA (fases 1 a 6)

**Objetivo:** Uma única referência de termos para o trabalho FIAP **2TIAOR20242**, alinhando a solução conversacional (Fases 1–5) com a extensão preditiva e multiagente (Fase 6).  
**Contrato de referência da demo unificada:** [`../specs/003-unify-multi-agent-solution/contracts/unified-demo-flow.md`](../specs/003-unify-multi-agent-solution/contracts/unified-demo-flow.md)

> **Âmbito educacional:** definições descrevem o **protótipo académico** no repositório. Não constituem orientação clínica nem substituem profissionais de saúde.

---

## Tabela de termos

| termo_canonico | definicao (resumo) | sinonimos / notas | fases_onde_aparece |
|----------------|-------------------|-------------------|---------------------|
| **idade** | Idade do paciente simulado em anos, usada como entrada do classificador e do pipeline. | "anos", "idade do utente" | 6 (ML, agents) |
| **freq_cardiaca** | Frequência cardíaca em bpm no cenário sintético. | "pulsação", "batimentos" | 6 |
| **spo2** | Saturação periférica de oxigénio simulada (%). | "saturação", "oximetria" | 6 |
| **carga_sistema** | Indicador normalizado \[0,1\] de stress/carga fisiológica simulada no dataset. | "stress", "carga fisiológica" | 6 |
| **disponibilidade_recursos** | Indicador normalizado \[0,1\] de recursos disponíveis no cenário simulado. | "recursos", "disponibilidade" | 6 |
| **pico_risco** | Variável alvo binária do modelo supervisionado (1 = pico de risco cardíaco simulado, 0 = sem pico). | "risco de pico", label do notebook | 6 (Parte 1) |
| **probability** | Probabilidade estimada \(P(\text{pico\_risco}=1)\) entre 0 e 1. | "prob. de pico", score do modelo | 6 |
| **risk_classification** | Faixa **baixo** / **médio** / **alto** derivada de limiares no código (`agents/config.py`). | "nível de risco", "classe de risco" | 6 |
| **protocolo simulado** | Entrada em `agents/data/protocols.json` com ações educativas **não prescritivas**. | "protocolo de emergência simulado" | 6 |
| **SAMU 192** | Número nacional de urgência referenciado na resposta fixa de **urgência médica** do backend. | "192", "urgência" | 1–6 (segurança) |
| **Watson Assistant** | Serviço IBM opcional que responde no modo conversacional quando credenciais estão configuradas. | "Watson", "assistente cloud" | 5–6 (contexto produto) |
| **camada de segurança** | Interceptação **antes** de Watson/ML/agentes que deteta palavras-chave de urgência e devolve resposta fixa com SAMU 192. | `safety_rules`, urgência | 5–6 |
| **LGPD / dado sensível** | Tratamento mínimo de dados; logs de agente em `agents/logs/` não devem conter dados reais de doentes. | "privacidade", "dados simulados" | 5–6 |
| **CardioIA (produto)** | Nome do trabalho académico: chat educativo (Flask + frontend) + extensão Fase 6 (modelo + multiagentes). | "projeto", "solução" | 1–6 |
| **POST /api/predict-risk** | Endpoint Flask que executa o mesmo pipeline que `agents/main.py` (`mode=agents` ou `ml_only`), com `context_message` opcional para urgência. | predição HTTP, API Fase 6 | 6 |
| **predictive_suggestion** | Objeto JSON opcional na resposta do chat quando o texto contém números reconhecíveis como features; sugere avançar para a etapa preditiva integrada na própria conversa. | ponte chat → ML | 6 |
| **fase6_prediction** | Objeto no `GET /health` com prontidão do modelo, protocolos e SDK (`prediction_readiness`). | readiness, sanidade Fase 6 | 6 |
| **governance (coerência)** | Verificação de alinhamento entre `risk_classification` e `risk_level` dos protocolos simulados; incluída na recomendação e nos logs. | IR ALÉM 1, auditoria | 6 |
| **batch_last_summary.json** | Resumo JSON após `python -m agents.batch_process` (vários pacientes em sequência). | IR ALÉM 2, lote | 6 |

---

## De intenções conversacionais a campos clínicos (Fase 5 → Fase 6)

O assistente da **Fase 5** (`backend/routes/chat_routes.py`, `backend/services/watson_service.py`) opera em **linguagem natural** com intents definidos no IBM Watson Assistant e limites em `backend/prompts/response_guidelines.md`. **Não** exige que o utilizador digite os cinco números do modelo.

A **Fase 6** (`agents/main.py` e `POST /api/predict-risk`) usa um **dicionário estruturado** com as cinco features para `predict_risk` em `agents/tools/risk_predictor.py`. O **chat** pode sugerir a predição quando `build_predictive_suggestion` encontra números no texto (`backend/utils/patient_from_text.py`).

| Papel | Onde | Função |
|-------|------|--------|
| Intents + respostas seguras | Watson + `response_guidelines.md` | Educação, redirecionamento, sem diagnóstico |
| Urgência | `backend/utils/safety_rules.py` | Resposta imutável com SAMU 192 **antes** de Watson/LLM; também aplicada a `context_message` em `/api/predict-risk` |
| Risco numérico | `agents/tools/risk_predictor.py` + HTTP | Dados estruturados — laboratório / rubrica FIAP; mesmo código via Flask |

**Conclusão para avaliadoras:** o chat e o pipeline são **complementares** na mesma linha de produto: o primeiro apoia conversa educativa (e pode **sugerir** a predição); o segundo demonstra orquestração + ML com dados explícitos ou via API, ambos sujeitos aos limites educacionais.

---

## Exemplo sintético canónico (PACIENTE_DEMO)

O repositório define em `agents/main.py` o dicionário `PACIENTE_DEMO`:

```python
PACIENTE_DEMO = {
    "idade": 65,
    "freq_cardiaca": 115,
    "spo2": 91.5,
    "carga_sistema": 0.85,
    "disponibilidade_recursos": 0.20,
}
```

Use **estes valores** no roteiro de demonstração e nos vídeos para manter rastreabilidade entre código, relatório e documentação (spec FR-004).

---

## Referências rápidas

- Limiares de classificação: `agents/config.py` (`RISK_THRESHOLDS`)
- Protocolos: `agents/data/protocols.json`
- Saída esperada do pipeline: `docs/arquitetura_multiagente_fiap_pdf.md`
