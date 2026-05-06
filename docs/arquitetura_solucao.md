# Arquitetura da Solucao - CardioIA (Fase 5 + extensao Fase 6)

**Repositorio:** [github.com/alexomantovanIA/1TIAOR20242-Cap1-CardioIA-experiencia-do-paciente](https://github.com/alexomantovanIA/1TIAOR20242-Cap1-CardioIA-experiencia-do-paciente)

## 1. Visao Geral da Arquitetura

O CardioIA adota uma arquitetura em tres camadas com separacao de responsabilidades, projetada para simplicidade, testabilidade e extensibilidade. A **Fase 6** acrescenta predicao estruturada via **`POST /api/predict-risk`** e o modulo **`agents/`** (executavel tambem em CLI e em lote), mantendo o chat da Fase 5 como nucleo conversacional.

```
                          +-----------------------------------------------+
                          |              USUARIO (Navegador)               |
                          +----------------------+------------------------+
                                                 |
                                   HTTP (GET /, POST /api/chat, POST /api/predict-risk, GET /health)
                                                 |
                          +----------------------v------------------------+
                          |              BACKEND (Flask)                   |
                          |                                               |
                          |  +----------+  +-----------+  +------------+  |
                          |  |  Routes  |  | Validators|  |   Models   |  |
                          |  | (chat_   |  | (entrada) |  | (dataclass)|  |
                          |  |  routes) |  +-----------+  +------------+  |
                          |  +----+-----+                                 |
                          |       |                                       |
                          |  +----v-----------+   +--------------------+  |
                          |  | Safety Rules   |   |  Static Files      |  |
                          |  | (urgencia)     |   |  (frontend/,       |  |
                          |  +----+-----------+   |   assets/)         |  |
                          |       |               +--------------------+  |
                          |  +----v-----------+                           |
                          |  | Watson Service |                           |
                          |  |  +-- Watson API v2 (IBM Cloud)             |
                          |  |  +-- Fallback Local (keywords)             |
                          |  +----------------+                           |
                          +-----------------------------------------------+
```

---

## 2. Diagrama de Sequencia - Fluxo Principal

```
Usuario          Frontend (JS)       Backend (Flask)      Safety Rules      Watson Service
  |                   |                    |                    |                  |
  |-- digita msg ---->|                    |                    |                  |
  |                   |-- POST /api/chat ->|                    |                  |
  |                   |                    |-- validate() ----->|                  |
  |                   |                    |<-- ok/erro --------|                  |
  |                   |                    |                    |                  |
  |                   |                    |-- check_urgency() ------>|            |
  |                   |                    |<-- (urgent, keywords) ---|            |
  |                   |                    |                    |                  |
  |                   |                    | [Se urgencia detectada]               |
  |                   |                    |-- retorna alerta SAMU --------------->|
  |                   |                    |                    |                  |
  |                   |                    | [Se nao urgente]   |                  |
  |                   |                    |-- send_message() ------------------>|
  |                   |                    |                    |     [Watson ok?] |
  |                   |                    |                    |     Sim: API v2  |
  |                   |                    |                    |     Nao: fallback|
  |                   |                    |<-- ChatResponse -------------------|
  |                   |                    |                    |                  |
  |                   |<-- JSON response --|                    |                  |
  |<-- renderiza msg--|                    |                    |                  |
```

---

## 3. Componentes Detalhados

### 3.1 Frontend (`frontend/`)

| Arquivo | Responsabilidade | Linhas |
|---------|-----------------|--------|
| `index.html` | Estrutura semantica HTML5: hero panel, context panel, chat panel, formulario, banner etico | ~137 |
| `style.css` | Sistema de design com CSS variables, layout responsivo (desktop/tablet/mobile), animacoes, acessibilidade (prefers-reduced-motion) | ~650 |
| `script.js` | Logica de interacao: fetch a `/api/chat` e `/api/predict-risk`, etapa de analise preditiva integrada ao fluxo conversacional (Fase 6), mensagens, `conversation_id` no localStorage, campo de governanca na predicao | ~480 |

**Decisao de projeto:** nenhum framework ou biblioteca externa. JavaScript puro (ES6+) para minimizar complexidade e dependencias, conforme escopo academico.

**Acessibilidade implementada:**
- Skip link para navegacao por teclado
- Atributos `aria-live`, `aria-label`, `aria-describedby`
- Suporte a `prefers-reduced-motion`
- Estados de foco visiveis (`focus-visible`)

### 3.2 Backend (`backend/`)

```
backend/
  __init__.py
  app.py              # Flask app factory, rotas de arquivos estaticos
  config.py           # Carrega variaveis de ambiente via python-dotenv
  models/
    message_models.py # ChatRequest, ChatResponse (dataclasses)
  routes/
    chat_routes.py    # Blueprint: POST /api/chat, GET /health (+ fase6_prediction)
    prediction_routes.py  # Blueprint: POST /api/predict-risk
  services/
    watson_service.py # WatsonService: integracao Watson + fallback local
  utils/
    validators.py     # validate_message(), sanitize_message()
    safety_rules.py   # check_urgency(), URGENCY_KEYWORDS, URGENCY_RESPONSE
    patient_from_text.py  # extracao heuristica -> predictive_suggestion no chat
    prediction_readiness.py  # indicadores Fase 6 para GET /health
  prompts/
    response_guidelines.md  # Diretrizes de resposta do assistente
  tests/
    test_healthcheck.py     # health + fase6_prediction
    test_chat_endpoint.py   # chat + predictive_suggestion
    test_safety_rules.py    # urgencia
    test_predict_risk_endpoint.py  # POST /api/predict-risk
    test_patient_from_text.py    # extracao de texto
```

### 3.3 Servico de NLP (watson_service.py)

O `WatsonService` implementa o padrao Strategy com fallback automatico:

**Modo Watson Assistant (primario):**
- Autenticacao: IAM (API Key)
- Versao da API: 2024-08-25
- SDK: `ibm-watson` v11.2.0
- Sessoes: criadas via `create_session()` com `assistant_id` e `environment_id`
- Mensagens: enviadas via `message()` com `user_id`
- Dados retornados: `intents[]` (com confianca), `entities[]` (com localizacao), `generic[]` (texto da resposta)

**Modo Fallback Local (secundario):**
- Ativacao: automatica quando Watson nao esta configurado ou falha
- Reconhecimento de intents: correspondencia por palavras-chave normalizadas (sem acentos)
- Reconhecimento de entities: correspondencia por padroes regex
- Selecao de resposta: lista de prioridade predefinida (urgencia > sintoma especifico > exame > geral)
- 16 intencoes mapeadas, 4 tipos de entidades, respostas predefinidas por intent

---

## 4. Fluxo de Dados Detalhado

### 4.1 Entrada (Request)

```
1. Usuario digita mensagem no textarea
2. JavaScript captura submit do formulario
3. Envia POST /api/chat com JSON: { message, conversation_id }
4. Flask recebe via request.get_json()
```

### 4.2 Processamento

```
5. Validacao (validators.py):
   - Tipo: deve ser string
   - Minimo: 2 caracteres
   - Maximo: 1000 caracteres
   - Sanitizacao: remove tags HTML, normaliza espacos

6. Verificacao de urgencia (safety_rules.py):
   - Normaliza acentos
   - Busca palavras-chave individuais (20 termos)
   - Verifica combinacoes (2 regras)
   - Se urgencia: retorna alerta imediato (nao envia ao Watson)

7. Processamento NLP (watson_service.py):
   a. Watson conectado: cria/reutiliza sessao, envia mensagem, recebe intents+entities+resposta
   b. Watson falhou: processa com motor local de palavras-chave

8. Construcao da resposta (ChatResponse):
   - reply: texto da resposta
   - source: "watson_assistant" | "fallback_local" | "safety_override"
   - urgency_detected: boolean
   - disclaimer: texto padrao de aviso
   - conversation_id: UUID da sessao
   - detected_intents: lista de intencoes reconhecidas
   - detected_entities: lista de entidades extraidas
   - follow_up: orientacao de proximo passo
```

### 4.3 Saida (Response)

```
9. Flask retorna JSON com status 200 (sucesso) ou 400 (erro de validacao)
10. JavaScript recebe resposta
11. Renderiza mensagem com:
    - Texto da resposta
    - Tag visual (Orientacao educacional | Atencao imediata | Limite do assistente)
    - Badge de fonte (Watson Assistant | Fallback local | Regra de seguranca)
    - Nota de rodape (lembrete educacional ou alerta de urgencia)
12. Atualiza status bar com modo e resultado
13. Armazena conversation_id no localStorage
```

---

## 5. Decisoes Arquiteturais

| Decisao | Alternativas Consideradas | Justificativa da Escolha |
|---------|--------------------------|-------------------------|
| Flask como framework backend | Django, FastAPI | Simplicidade para prototipo academico; curva de aprendizado minima; adequado para MVP |
| Watson Assistant como NLP | Dialogflow, Rasa, LUIS | Plataforma de referencia na disciplina PCV; plano Lite gratuito; API v2 bem documentada |
| Fallback local por keywords | Sem fallback; modelo local (spaCy) | Garante funcionamento offline; demonstra conceitos de NLP sem dependencia externa |
| Verificacao de urgencia pre-Watson | Verificacao pos-Watson; sem verificacao | Seguranca do paciente e prioridade absoluta; nao depender de modelo ML para cenarios criticos |
| Frontend sem frameworks | React, Vue, Angular | Menor complexidade; sem build step; alinhado ao escopo academico; mais facil de avaliar |
| Testes com pytest | unittest, nose | Padrao Python moderno; sintaxe simples; boa integracao com Flask test client |
| JSON como formato de resposta | XML, texto plano | Padrao da industria para APIs REST; parsing nativo no JavaScript; estruturado e legivel |
| localStorage para sessao | Cookies, sessionStorage | Persiste entre abas; API simples; sem necessidade de backend para sessao |
| Dataclasses para modelos | Dicionarios, Pydantic | Nativas do Python 3.10+; type hints; metodo to_dict() para serializacao |

---

## 6. Seguranca

### 6.1 Seguranca do Paciente
- Verificacao de urgencia com prioridade sobre NLP
- 20 palavras-chave + 2 combinacoes de alerta
- Resposta imediata com orientacao SAMU (192)

### 6.2 Seguranca da Aplicacao
- Sanitizacao de entrada: remocao de tags HTML (prevencao XSS)
- Validacao de tamanho de mensagem (2-1000 caracteres)
- Credenciais em variaveis de ambiente (`.env` no `.gitignore`)
- Sem execucao de codigo dinamico a partir da entrada do usuario

### 6.3 Privacidade
- Nenhum dado pessoal coletado ou armazenado
- Sem banco de dados ou logs persistentes de conversas
- Comunicacao com Watson via HTTPS (criptografado em transito)
