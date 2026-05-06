# Relatorio Tecnico - Fase 5: Assistente Cardiologico Inteligente e Conversacional

**Projeto:** CardioIA
**Instituicao:** FIAP - Faculdade de Informatica e Administracao Paulista
**Curso:** 1TIAOR - Turma 2024/2
**Fase:** 5 - Experiencia do Paciente
**Disciplina de referencia:** Processamento de Linguagem Natural, Chatbots & Virtual Agents (PCV)

**Integrantes:**
- Alexandre Oliveira Mantovani
- Edmar Ferreira Souza
- Ricardo Lourenco Coube
- Jose Andre Filho

**Orientacao:**
- Tutor: Leonardo Ruiz Orabona
- Coordenador: Andre Godoi

**Repositorio:** [github.com/alexomantovanIA/1TIAOR20242-Cap1-CardioIA-experiencia-do-paciente](https://github.com/alexomantovanIA/1TIAOR20242-Cap1-CardioIA-experiencia-do-paciente)

---

## 1. Introducao e Contextualizacao

### 1.1 Contexto do Projeto

O CardioIA e um projeto academico desenvolvido ao longo de multiplas fases com foco em saude cardiovascular e tecnologia. Nas fases anteriores, foram explorados temas como monitoramento de dados clinicos, analise de imagens e prototipacao visual. Na Fase 5, o foco se desloca para a **comunicacao inteligente** por meio de Processamento de Linguagem Natural (NLP), consolidando a construcao de um **Assistente Cardiologico Conversacional**.

### 1.2 Objetivo

Construir um prototipo funcional de chatbot que:
- Interaja com o usuario por meio de linguagem natural, simulando um atendimento inicial em saude cardiovascular.
- Integre servicos de NLP (IBM Watson Assistant) e automacao de fluxos conversacionais.
- Organize e apresente informacoes clinicas de forma estruturada, segura e compreensivel.
- Implemente regras de seguranca que detectem cenarios de urgencia e orientem o usuario adequadamente.
- Respeite limites eticos, tecnicos e conceituais, sem realizar diagnosticos ou prescricoes.

### 1.3 Justificativa

Segundo a Organizacao Mundial da Saude (OMS), doencas cardiovasculares sao a principal causa de morte no mundo. A aplicacao de agentes conversacionais em saude digital pode contribuir para a educacao do paciente, triagem inicial e encaminhamento adequado, desde que respeitados os limites eticos e regulatorios. Este projeto explora essa possibilidade em contexto estritamente academico.

### 1.4 Relacao com as Disciplinas

O desenvolvimento integra conhecimentos de multiplas disciplinas do curso:

| Disciplina | Contribuicao no Projeto |
|-----------|------------------------|
| Processamento de Linguagem Natural (PCV) | Modelagem de intents, entities e dialog nodes no Watson Assistant; motor de NLP local por palavras-chave |
| Automacao e Integracao | Fluxo automatizado de atendimento; integracao backend-Watson via API REST |
| APIs e Servicos | Comunicacao Flask-Watson via IBM Cloud SDK; endpoints RESTful |
| IA Generativa e Governanca | Regras de seguranca; limites eticos do assistente; transparencia nas respostas; aderencia conceitual a LGPD |
| Bancos de Dados | Estruturacao de dados em modelos (dataclasses); formato JSON para troca de mensagens |

---

## 2. Metodologia de Desenvolvimento

O projeto seguiu uma abordagem incremental organizada em 8 fases internas:

**Fase A - Planejamento e Arquitetura:** definicao de objetivo, escopo, restricoes tecnicas e eticas, estrutura de diretorios e arquivos de configuracao. Decisao por Flask como framework backend e Watson Assistant como motor de NLP.

**Fase B - Modelagem do Assistente:** construcao de 16 intencoes (intents), 4 entidades (entities) com sinonimos, e 18 nos de dialogo (dialog nodes) no padrao IBM Watson Assistant. Documentacao completa em `assistant/intents_entities_documentation.md`.

**Fase C - Backend Flask:** implementacao dos endpoints `/api/chat` (POST) e `/health` (GET), validacao de entrada, sanitizacao de mensagens, normalizacao de caracteres e organizacao modular por camadas (routes, services, models, utils).

**Fase D - Integracao Watson:** criacao da classe `WatsonService` com autenticacao IAM, gerenciamento de sessoes via API v2, e fallback automatico para motor local quando o Watson nao esta configurado ou falha.

**Fase E - Regras de Seguranca e Etica:** implementacao do modulo `safety_rules.py` com 20 palavras-chave de urgencia e 2 regras combinatorias. Verificacao de urgencia executada **antes** do envio ao Watson, garantindo resposta imediata em cenarios criticos. Inclusao de disclaimer em todas as respostas.

**Fase F - Frontend:** desenvolvimento da interface de chat responsiva em HTML, CSS e JavaScript puro, com: painel de boas-vindas, exemplos interativos, indicadores visuais de tipo de resposta (educacional, urgencia, limite), badge de fonte (Watson/Fallback/Regra de seguranca), acessibilidade (skip links, aria labels, reduced motion).

**Fase G - Testes:** criacao de **30** testes automatizados na entrega original da Fase 5 (healthcheck, chat, seguranca). **Atualizacao:** apos integracao Fase 6, ver **Apendice C** e `README.md` para a contagem atual da suite `backend/tests`.

**Fase H/I - Documentacao:** elaboracao de relatorio tecnico, documentacao de arquitetura, fluxo conversacional, instrucoes de configuracao e exemplos de conversas anotados.

**Video de demonstracao:** https://youtu.be/dn5lhY7gvAY

---

## 3. Arquitetura da Solucao

### 3.1 Visao Geral

A arquitetura segue o padrao de tres camadas com separacao clara de responsabilidades. Cada mensagem recebida percorre um pipeline sequencial: **(1) camada de seguranca**, que intercepta urgencias antes de qualquer processamento de NLP; **(2) camada de NLP**, que classifica intencoes e extrai entidades via IBM Watson Assistant ou motor de fallback local; e **(3) camada de respostas educacionais**, que seleciona e formata a orientacao adequada.

```
+-------------------+       HTTP POST /api/chat      +-------------------+
|                   |  -----------------------------> |                   |
|     Frontend      |                                 |   Backend Flask   |
|   (HTML/CSS/JS)   |  <---- JSON response ---------- |                   |
|                   |                                 +--------+----------+
+-------------------+                                          |
                                                               v
                                              +----------------+----------------+
                                              |         Watson Service          |
                                              |                                 |
                                              |  1. Verificacao de urgencia     |
                                              |     (safety_rules.py)           |
                                              |         |                       |
                                              |    [Urgente?]                   |
                                              |     Sim -> Alerta SAMU          |
                                              |     Nao -> continua             |
                                              |         |                       |
                                              |  2. Watson Assistant API v2     |
                                              |     (se configurado)            |
                                              |         |                       |
                                              |    [Falhou?]                    |
                                              |     Sim -> Fallback local       |
                                              |     Nao -> Resposta Watson      |
                                              +---------------------------------+
```

### 3.2 Componentes

**Frontend (`frontend/`):** Interface responsiva sem dependencias externas. Tres paineis: hero (apresentacao), contexto (escopo e exemplos) e chat (interacao). Comunicacao assincrona via `fetch` API.

**Backend (`backend/`):** Aplicacao Flask organizada em camadas:
- `routes/` - Endpoints HTTP (Blueprint)
- `services/` - Logica de integracao Watson + fallback
- `models/` - Dataclasses para request e response
- `utils/` - Validacao de entrada e regras de seguranca
- `tests/` - Suite de testes automatizados

**Servico de NLP:** Dupla implementacao:
- **Watson Assistant (API v2):** Autenticacao IAM, sessoes persistentes, classificacao por modelo de machine learning treinado com ~160 exemplos de treino.
- **Fallback Local:** Motor baseado em correspondencia de palavras-chave com normalizacao de acentos, 16 intencoes mapeadas e 4 tipos de entidades com reconhecimento por padrao regex.

### 3.3 Especificacao da API

**POST /api/chat**

Request:
```json
{
  "message": "Estou com palpitacoes leves ha 2 dias",
  "conversation_id": "opcional-uuid"
}
```

Response (200):
```json
{
  "reply": "Palpitacoes podem ser percebidas como...",
  "source": "watson_assistant",
  "urgency_detected": false,
  "disclaimer": "Aviso: este assistente tem finalidade educacional...",
  "conversation_id": "uuid-gerado",
  "detected_intents": ["informar_palpitacao"],
  "detected_entities": ["duracao", "intensidade"],
  "follow_up": "Orientacao educacional entregue."
}
```

Response (400 - erro de validacao):
```json
{
  "message": "A mensagem deve conter pelo menos 2 caracteres."
}
```

**GET /health**

Response (200):
```json
{
  "status": "ok",
  "watson_connected": true,
  "mode": "watson_assistant"
}
```

---

## 4. Modelagem do Assistente (NLP)

### 4.1 Intencoes (Intents)

Foram modeladas 16 intencoes com 10 exemplos de treino cada (total: ~160 exemplos):

| Categoria | Intent | Descricao | Exemplos |
|-----------|--------|-----------|----------|
| Navegacao | `saudacao` | Cumprimento inicial | "Oi", "Bom dia" |
| Navegacao | `despedida` | Encerramento | "Tchau", "Obrigado" |
| Sintomas | `informar_dor_peito` | Dor toracica | "Dor no peito", "Aperto no peito" |
| Sintomas | `informar_palpitacao` | Batimentos irregulares | "Palpitacao", "Coracao acelerado" |
| Sintomas | `informar_falta_ar` | Dispneia | "Falta de ar", "Cansaco" |
| Sintomas | `informar_tontura` | Vertigem/sincope | "Tontura", "Desmaio" |
| Sintomas | `informar_pressao` | Pressao arterial | "Pressao alta", "Hipertensao" |
| Sintomas | `informar_inchaco` | Edema/inchaco | "Pernas inchadas", "Pes inchados" |
| Sintomas | `informar_sintoma_geral` | Sintoma generico | "Nao me sinto bem" |
| Exames | `perguntar_ecg` | Eletrocardiograma | "O que e ECG?" |
| Exames | `perguntar_ecocardiograma` | Ecocardiograma | "Me explica o eco" |
| Exames | `perguntar_holter` | Monitoramento Holter | "O que e Holter?" |
| Exames | `perguntar_teste_ergometrico` | Teste de esforco | "Teste na esteira" |
| Exames | `perguntar_cateterismo` | Cateterismo cardiaco | "Cateterismo e perigoso?" |
| Exames | `perguntar_exame` | Exames em geral | "Quais exames do coracao?" |
| Limite | `solicitar_diagnostico` | Pedido de diagnostico | "O que eu tenho?" |

### 4.2 Entidades (Entities)

| Entidade | Valores | Exemplos de Sinonimos |
|----------|---------|----------------------|
| `@sintoma` | 8 valores | dor no peito, palpitacao, falta de ar, tontura, pressao alta, inchaco, nausea, suor frio |
| `@duracao` | 5 valores | minutos, horas, dias, semanas, meses |
| `@intensidade` | 3 valores | leve/fraco, moderada/medio, intensa/forte |
| `@exame` | 5 valores | ECG, ecocardiograma, holter, teste ergometrico, cateterismo |

### 4.3 Regras de Seguranca

O modulo `backend/utils/safety_rules.py` implementa verificacao de urgencia com **prioridade sobre o Watson**. A funcao `check_urgency()` (linha 54) normaliza o texto via `_normalize()` — removendo acentos e convertendo para minusculas — e busca correspondencias em duas estruturas:

**Palavras-chave individuais (20)** (lista `URGENCY_KEYWORDS`, linha 3): "dor intensa no peito", "infarto", "desmaio", "perda de consciencia", "parada cardiaca", "AVC", "falta de ar intensa", "suor frio", entre outras.

**Combinacoes (2 regras)** (lista `URGENCY_COMBINATIONS`, linha 26):
- Dor toracica + (falta de ar | suor | nausea | dor no braco)
- Tontura + (desmaio | perda de consciencia)

**Normalizacao:** acentos sao removidos antes da verificacao para garantir deteccao independente de formatacao.

**Comportamento:** quando urgencia e detectada, o pipeline e **interrompido** — o Watson nao e acionado. A resposta padronizada (`URGENCY_RESPONSE`, linha 31) orienta o usuario a procurar atendimento medico imediato ou ligar para o SAMU (192). O campo `source` retorna `"safety_override"` e `urgency_detected` retorna `true`.

**Validacao:** 11 testes unitarios em `backend/tests/test_safety_rules.py` cobrem palavras-chave individuais, combinacoes, normalizacao de acentos e ausencia de falsos positivos.

### 4.4 Motor de Fallback Local

Quando o Watson esta indisponivel, o fallback local (funcao `_classify_intent()` em `backend/services/watson_service.py`) utiliza correspondencia por palavras-chave com normalizacao de acentos. O dicionario `INTENT_KEYWORDS` (linha 15) mapeia cada uma das 16 intencoes a uma lista de termos. A classificacao percorre as intencoes em ordem de prioridade definida na funcao `_choose_response()`, priorizando sintomas especificos sobre o generico (`informar_sintoma_geral`) e garantindo que `solicitar_diagnostico` seja corretamente identificado antes do fallback final. O sistema utiliza **18 nos de dialogo** encadeados via campo `previous_sibling` no JSON exportado para definir a ordem de avaliacao no Watson.

---

## 5. Resultados

### 5.1 Testes Automatizados

Foram implementados 30 testes automatizados na entrega Fase 5, organizados em 3 suites (ver Apendice C para evolucao):

| Suite | Testes | Cobertura |
|-------|--------|-----------|
| `test_healthcheck.py` | 4 | Disponibilidade, status, modo de operacao, flag Watson |
| `test_chat_endpoint.py` | 14 | Mensagem valida, payload invalido, mensagem vazia, muito curta, preservacao de conversation_id, geracao de ID, reconhecimento de intents (saudacao, despedida, palpitacao, ECG, diagnostico), disclaimer, fallback |
| `test_safety_rules.py` | 12 | Dor intensa, infarto, desmaio, falta de ar intensa, suor frio, combinacoes, acentos, nao-urgencia (palpitacao leve, saudacao, pergunta exame) |
| **Total** | **30** | **100% passando** |

### 5.2 Integracao Watson Assistant

O Watson Assistant foi configurado e treinado com sucesso:
- **16 intencoes** reconhecidas com confianca media superior a 85%
- **4 entidades** com extracao por sinonimos
- **18 nos de dialogo** com fluxo estruturado
- **Fallback automatico** ativa modo local quando Watson indisponivel
- **Tempo medio de resposta:** inferior a 2 segundos via Watson API

### 5.3 Cenarios Validados

| Cenario | Entrada | Resposta Esperada | Resultado |
|---------|---------|-------------------|-----------|
| Saudacao | "Oi, bom dia" | Apresentacao educacional | OK - Watson |
| Sintoma com detalhes | "Palpitacoes leves ha 2 dias" | Orientacao sobre palpitacoes | OK - Watson |
| Pergunta sobre exame | "O que e um ECG?" | Explicacao do ECG | OK - Watson |
| Urgencia | "Dor intensa no peito e falta de ar" | Alerta SAMU 192 | OK - Safety Override |
| Limite do assistente | "O que eu tenho? Me diagnostica" | Recusa educada + encaminhamento | OK - Watson |
| Despedida | "Obrigado, tchau" | Encerramento + lembrete | OK - Watson |
| Mensagem invalida | "" (vazio) | Erro 400 | OK - Validacao |
| Intent desconhecido | "xyzabc123" | Resposta de fallback | OK - Fallback |

---

## 6. Consideracoes Eticas e de Governanca

### 6.1 Limites do Assistente

O CardioIA foi projetado com restricoes explicitas:
- **Nao realiza diagnostico:** quando o usuario solicita, o assistente recusa e orienta busca por profissional.
- **Nao prescreve medicamentos:** nenhuma resposta contem indicacao farmacologica.
- **Nao substitui avaliacao medica:** disclaimer presente em todas as respostas.
- **Nao processa dados reais:** nenhum dado clinico real e armazenado ou processado.

### 6.2 Transparencia

- Todas as respostas incluem nota de rodape indicando carater educacional.
- A interface exibe banner etico permanente.
- O badge de fonte indica se a resposta veio do Watson, do fallback local ou da regra de seguranca.

### 6.3 Seguranca do Paciente

- Verificacao de urgencia tem **prioridade absoluta** sobre qualquer outro fluxo.
- Cenarios de urgencia nunca sao minimizados.
- Orientacao para SAMU (192) e sempre incluida em alertas.

### 6.4 Aderencia Conceitual a LGPD

- Nenhum dado pessoal e coletado ou armazenado.
- Nao ha persistencia de conversas em banco de dados.
- Credenciais de API sao gerenciadas via variaveis de ambiente (`.env`), excluidas do versionamento (`.gitignore`).
- O projeto nao transmite dados a terceiros alem do IBM Watson Assistant para processamento de NLP.

---

## 7. Limitacoes

- O fallback local utiliza correspondencia por palavras-chave, sem modelo estatistico ou embeddings.
- Nao ha persistencia de historico entre sessoes do navegador.
- Nao existe autenticacao ou controle de acesso de usuarios.
- O assistente nao processa prontuarios, exames ou dados clinicos reais.
- O reconhecimento de intencoes depende da qualidade e quantidade dos exemplos de treino.
- O prototipo nao foi validado com usuarios reais ou profissionais de saude.

---

## 8. Conclusao

O CardioIA demonstra a aplicabilidade de agentes conversacionais em contextos de saude digital educacional, integrando Processamento de Linguagem Natural, automacao de fluxos e boas praticas de governanca em IA.

A arquitetura modular desenvolvida - com separacao clara entre frontend, backend e servico de NLP - permite expansao futura para modelos mais sofisticados de processamento de linguagem, integracao com bases de dados clinicos e implementacao de mecanismos adicionais de personalizacao e acompanhamento.

O projeto reforca que a tecnologia pode ser aliada na educacao em saude, desde que aplicada com responsabilidade, transparencia e respeito aos limites eticos e profissionais da area medica.

---

## Apendice A - Estrutura de Arquivos

```
backend/
  app.py, config.py, __init__.py
  models/message_models.py
  routes/chat_routes.py, prediction_routes.py
  services/watson_service.py
  utils/safety_rules.py, validators.py, patient_from_text.py, prediction_readiness.py
  prompts/response_guidelines.md
  tests/ (5+ ficheiros de teste; ver nota pos-Fase-6 no Apendice C)
assistant/
  cardioia_assistant_export.json
  fluxo_conversacional.md
  intents_entities_documentation.md
docs/
  relatorio_fase5.md (este documento)
  relatorio_fluxo_conversacional.pdf
  arquitetura_solucao.md
  instrucoes_configuracao_watson.md
frontend/
  index.html, script.js, style.css
samples/
  conversas_exemplo.md
  json_examples/request_exemplo.json
  json_examples/response_exemplo.json
```

## Apendice B - Comandos de Execucao

```bash
# Instalar dependencias
pip install -r requirements.txt

# Executar o backend
python -m backend.app

# Executar testes (Fase 5 + integracao Fase 6 no mesmo backend)
pytest backend/tests -v
pytest backend/tests agents/tests -q

# Acessar a interface
http://localhost:5000

# Verificar saude do servico
http://localhost:5000/health
```

## Apendice C — Atualizacao pos-Fase 6 (integracao no mesmo backend)

Apos a unificacao do CardioIA com a Fase 6, o backend descrito neste relatorio **ganhou** rotas e utilitarios adicionais (mantendo o chat e as regras de urgencia):

- `POST /api/predict-risk` — mesmo pipeline de predicao que o pacote `agents/` (modos `ml_only` e `agents`).
- `GET /health` — resposta inclui `fase6_prediction` (prontidao do modelo e dependencias).
- `POST /api/chat` — pode incluir `predictive_suggestion` quando o texto do utilizador contem valores extraiveis para as cinco features.

A suite `backend/tests` **deixou de ter apenas 30 testes**; na ultima consolidacao do repositorio ha **41** testes em `backend/tests` e **65** no total com `agents/tests`. O relatorio historico da Fase 5 acima refere-se ao estado entregue na disciplina da Fase 5; a numeracao atual encontra-se no `README.md` e em `docs/passo_a_passo_execucao_local_fase6.md`.
