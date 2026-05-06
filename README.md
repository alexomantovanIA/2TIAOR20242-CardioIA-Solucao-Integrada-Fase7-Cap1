# CardioIA Fase 7 - MVP Final Integrado

Projeto academico FIAP com integracao final:

Sensor simulado -> MicroPython/Wokwi -> Backend Flask -> IA/ML Fase 6 -> Web React/Vite e Mobile Expo.

> Sistema acadêmico. Não substitui avaliação médica. Não usar para diagnóstico definitivo, prescrição ou decisão clínica real.

## Links de entrega

- Vercel Web: `PREENCHER_APOS_DEPLOY`
- APK/Expo Dashboard ou QR Code: `PREENCHER_APOS_EAS_BUILD`
- Wokwi publico: `PREENCHER_APOS_PUBLICAR_WOKWI`
- Video demonstrativo: `PREENCHER_APOS_GRAVACAO`

## Estrutura Fase 7

```text
cardioia-fase7/
├─ backend/          # Flask integrador, chat, predição e IoT
├─ agents/           # Pipeline Fase 6 ml_only/agentes opcionais
├─ ml/               # modelo_risco_cardiaco.joblib reutilizado
├─ apps/
│  ├─ web/           # React + Vite + TypeScript + Vercel
│  └─ mobile/        # React Native + Expo + EAS APK
├─ iot/              # MicroPython + Wokwi
├─ docs/             # relatório, roteiro e arquitetura
├─ notebooks/        # notebooks opcionais/historicos
├─ README.md
├─ .env.example
└─ docker-compose.yml
```

## Backend

Modo padrao: `ml_only` com fallback local. OpenAI Agents, Watson, Docker e LocalStack sao opcionais via variaveis de ambiente.

Endpoints principais:

- `GET /health`
- `POST /api/chat`
- `POST /api/predict-risk`
- `POST /api/iot/ingest`
- `GET /api/dashboard/summary`
- `GET /api/patient/latest`
- `POST /api/full-analysis`

Rodar:

```bash
python3 -m venv .venv311
.venv311/bin/pip install -r requirements.txt
PORT=5001 .venv311/bin/python -m backend.app
```

Testes:

```bash
.venv311/bin/pytest backend/tests agents/tests -q
```

Exemplo IoT:

```bash
curl -s -X POST http://127.0.0.1:5000/api/iot/ingest \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"wokwi-esp32-cardioia","heart_rate":118,"temperature":37.9,"spo2":94,"timestamp":"2026-05-03T16:11:00Z"}'
```

Exemplo analise completa:

```bash
curl -s -X POST http://127.0.0.1:5000/api/full-analysis \
  -H 'Content-Type: application/json' \
  -d '{"message":"Tenho palpitacoes leves ha dois dias.","patient":{"idade":55,"freq_cardiaca":118,"spo2":94,"carga_sistema":0.55,"disponibilidade_recursos":0.55}}'
```

## Web React + Vite

Local: `apps/web`.

```bash
cd apps/web
npm install
npm run lint
npm run build
npm run preview
```

Variavel:

```bash
VITE_API_BASE_URL=http://localhost:5000
```

Deploy Vercel:

- Conectar o repositorio GitHub na Vercel.
- Definir o root directory como `apps/web`.
- Usar o `vercel.json` ja incluido para SPA rewrite em `/index.html`.
- Configurar `VITE_API_BASE_URL` para a URL publica do backend.

## Mobile Expo

Local: `apps/mobile`.

```bash
cd apps/mobile
npm install
npx expo-doctor
npx expo start
```

Variavel:

```bash
EXPO_PUBLIC_API_BASE_URL=http://localhost:5000
```

APK preview:

```bash
npx eas build --platform android --profile preview
```

O `app.json` usa `android.package = br.com.fiap.cardioiafase7`, e o `eas.json` usa `android.buildType = apk` no profile `preview`.

## IoT MicroPython/Wokwi

Local: `iot/`.

- `main.py`: simula `heart_rate`, `temperature` e `spo2`, calcula `normal`, `atencao` ou `critico`, controla LED RGB e pode enviar POST para `/api/iot/ingest`.
- `diagram.json`: ESP32 + LED RGB.
- `iot/README.md`: instrucoes Wokwi e prints esperados.

## Documentacao Fase 7

- Relatorio tecnico: [`docs/relatorio_fase7.md`](docs/relatorio_fase7.md)
- Roteiro do video: [`docs/roteiro_video.md`](docs/roteiro_video.md)
- Diagrama Mermaid: [`docs/arquitetura_final.mmd`](docs/arquitetura_final.mmd)

## Prints esperados

- Backend: `/health` com `mode=fallback_local` e `fase6_prediction.predict_risk_ready=true`.
- Web: login demo, dashboard com sinais vitais, card de risco, chat e historico.
- Mobile: login demo, home com risco atual, sinais vitais, chat, recomendacoes e sobre.
- Wokwi: console com leituras e LED RGB mudando por status.
- Terminal: `71 passed` nos testes, build Vite concluido e `expo-doctor` com `17/17 checks passed`.

## LGPD e limitacoes

- O MVP usa armazenamento local simples/JSON apenas para a ultima leitura IoT.
- Nao ha banco de dados obrigatorio, autenticacao real, prontuario clinico ou consentimento formal.
- Dados usados na demonstracao devem ser simulados.
- O modelo `.joblib` classifica risco academico em `baixo`, `médio` ou `alto`; nao realiza diagnostico.
- Watson/OpenAI/TensorFlow/LocalStack/Docker permanecem opcionais para reduzir custo e risco de demonstracao.

---

# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

---

# CardioIA — Coração Sob Controle: Previsão de Crises com IA

### Fase 6 — Sistema Preditivo Multiagente

**Repositório:** [github.com/joseandrefilho/2TIAOR20242-CardioIA-Fase6-Cap1](https://github.com/joseandrefilho/2TIAOR20242-CardioIA-Fase6-Cap1)

---

## 👨‍🎓 Integrantes

- [Alexandre Oliveira Mantovani](https://www.linkedin.com/in/alexomantovani)
- [Edmar Ferreira Souza](https://www.linkedin.com/in/)
- [Ricardo Lourenço Coube](https://www.linkedin.com/in/ricardolcoube/)
- [Jose Andre Filho](https://www.linkedin.com/in/joseandrefilho)

## 👩‍🏫 Professores

- Tutor: [Leonardo Ruiz Orabona](https://www.linkedin.com/in/leonardoorabona)
- Coordenador: [André Godoi](https://www.linkedin.com/in/profandregodoi)

---

## 📌 Descrição do Projeto

A **Fase 6** do projeto **CardioIA** evolui do assistente conversacional (Fase 5) para uma **plataforma preditiva multiagente** capaz de antecipar picos de risco cardíaco e recomendar protocolos de emergência com base em dados clínicos.

O sistema integra:
- **Modelo de Machine Learning supervisionado** (`RandomForestClassifier`) treinado para classificar o risco cardíaco como `baixo`, `médio` ou `alto` a partir de 5 variáveis clínicas.
- **Sistema Multiagente com OpenAI Agents SDK** composto por três agentes especializados que colaboram via handoffs para gerar uma recomendação estruturada.

> **Aviso Acadêmico e Médico**: projeto com **uso estritamente acadêmico (FIAP)**. Não realiza diagnóstico, não prescreve medicamentos e não substitui avaliação médica profissional. Em emergências, ligue **SAMU 192**.

### Linha do tempo — CardioIA (fases 1 a 6)

| Fase | Foco no repositório |
|------|---------------------|
| 1–4 | Fundamentos e IoT (histórico do trabalho consolidado nos enunciados em `.fiap/fases_unificadas/`) |
| 5 | **Assistente conversacional** em `backend/` (Flask), `frontend/`, IBM Watson Assistant em `assistant/` — triagem educativa com **camada de segurança** antes do processamento NLP |
| 6 (Parte 1) | Modelo supervisionado treinado no notebook → artefato `ml/modelo_risco_cardiaco.joblib` |
| 6 (Parte 2) | **Pipeline multiagente** em `agents/` (OpenAI Agents SDK + tools determinísticas) |

**Coesão (documentação canónica):**

- [Glossário unificado](docs/glossario_unificado_cardioia.md) — termos partilhados entre conversação e predição  

A Fase 6 **não substitui** o trabalho da Fase 5: o **mesmo produto CardioIA** ganha uma extensão preditiva demonstrável em laboratório. O servidor Flask em `backend/app.py` expõe **`POST /api/chat`** (conversação + sugestão preditiva opcional no JSON), **`POST /api/predict-risk`** (ML e/ou pipeline multiagente, com verificação de urgência opcional em `context_message`) e **`GET /health`** (inclui bloco `fase6_prediction` com prontidão do modelo, protocolos e SDK). O ficheiro `ml/modelo_risco_cardiaco.joblib` e o pacote `agents/` cumprem a rubrica de ML e orquestração de agentes.

**Enunciado formal da disciplina (avaliação):** [`.fiap/fases_unificadas/fase06_enunciado_avaliacao.md`](.fiap/fases_unificadas/fase06_enunciado_avaliacao.md)

#### Da conversa à predição (quatro passos)

1. **Conversar (Fase 5):** o utilizador interage com o HTML em `frontend/` → `POST /api/chat` → `backend/routes/chat_routes.py` aplica validação e delega em `WatsonService` ou fallback local, **sempre** após a verificação de urgência em `backend/utils/safety_rules.py`.  
2. **Treinar e persistir o modelo (Fase 6 — Parte 1):** o notebook em `notebooks/` gera dados sintéticos, treina o classificador e grava `ml/modelo_risco_cardiaco.joblib`.  
3. **Orquestrar predição + protocolos (Fase 6 — Parte 2):** `python -m agents.main` executa o pipeline multiagente (`predict_risk_tool` + `get_protocols_tool` + handoffs). Em alternativa sem browser: `POST /api/predict-risk` com `mode=ml_only` ou `agents`; na interface `frontend/`, a análise preditiva aparece como **etapa integrada da conversa** e chama esse endpoint. Cada recomendação inclui **`governance`** (coerência protocolo × classificação) e **log JSON** em `agents/logs/`.
4. **IR ALÉM 2 (lote simulado):** `python -m agents.batch_process` processa vários pacientes em sequência e grava `agents/logs/batch_last_summary.json`.

---

## 📦 Entregáveis — Fase 6

### Parte 1 — Modelo Preditivo de Pico de Risco

| Entregável | Localização |
|------------|-------------|
| Notebook Jupyter — geração de dados, treino, avaliação, simulação (**execução local**) | `notebooks/fase6_modelo_preditivo.ipynb` + `requirements-notebook.txt` |
| Modelo treinado persistido | `ml/modelo_risco_cardiaco.joblib` |
| Relatório técnico (máx. 2 páginas) | `docs/relatorio_parte1.md` |

### Parte 2 — Sistema Multiagente com OpenAI Agents SDK

| Entregável | Localização |
|------------|-------------|
| Código completo do sistema multiagente | `agents/` |
| Documento de arquitetura (**Markdown completo**, rubrica + rastreabilidade código ↔ enunciado) | [`docs/arquitetura_multiagente.md`](docs/arquitetura_multiagente.md) |
| Testes automatizados (`agents/tests/` + `backend/tests/`; ver secção *Testes*) | `agents/tests/`, `backend/tests/` |

### 🎬 Vídeo de Demonstração — Fase 6

> [YouTube](https://youtu.be/L_ryHoJJKnY) 

---

## 🎯 Critérios de Avaliação (10 pontos)

| Critério | Pontos | Como atendido |
|----------|--------|---------------|
| Treinamento correto do modelo preditivo | 3 | `notebooks/fase6_modelo_preditivo.ipynb` — RF com avaliação registrada no notebook executado |
| Avaliação com métricas adequadas | 2 | Acurácia, classification report, matriz de confusão no notebook e relatório |
| Implementação da arquitetura multiagente | 3 | `agents/main.py` — 3 agentes, handoffs, tools, histórico de mensagens |
| Integração correta entre agentes e modelo | 1 | `predict_risk_tool` invoca o `.joblib` e passa resultado via handoff; **HTTP** `POST /api/predict-risk` reutiliza o mesmo pipeline |
| Organização e clareza do código/documentação | 1 | Estrutura modular (`agents/personas/`, `agents/pipeline/`, `agents/governance/`, `backend/`), **65** testes automatizados (`pytest backend/tests agents/tests`), docs e README |
| Trabalho em equipe (4 integrantes) | +1 extra | Equipe de 4 integrantes — ver seção Integrantes |

---

## 🏗️ Arquitetura do Sistema Multiagente

```
Entrada: dados do paciente (idade, freq_cardiaca, spo2, carga_sistema, disponibilidade_recursos)
          │
          ▼
    [ORQUESTRADOR]  ──handoff──►  [ANALISTA DE RISCO]
                                         │  tool: predict_risk_tool
                                         │  (invoca RandomForestClassifier)
                                         │
                              handoff──► [ESPECIALISTA EM PROTOCOLOS]
                                                │  tool: get_protocols_tool
                                                │  (consulta protocols.json)
                                                │
                              handoff──► [ORQUESTRADOR]
                                                │
                                                ▼
                              Saída: { probability, risk_classification,
                                       suggested_protocols, disclaimer }
```

Documentação da arquitetura: [**versão completa (Markdown)**](docs/arquitetura_multiagente.md)

---

## 🗂️ Estrutura do Projeto

```text
2TIAOR20242-CardioIA-Fase6-Cap1/
│
├─ notebooks/
│  └─ fase6_modelo_preditivo.ipynb   ← FASE 6 Parte 1: dataset, treino, avaliação
│
├─ ml/
│  └─ modelo_risco_cardiaco.joblib   ← Modelo treinado e persistido (métricas no notebook executado)
│
├─ agents/                           ← FASE 6 Parte 2: sistema multiagente
│  ├─ __init__.py                    ← Proxy para openai-agents SDK
│  ├─ main.py                        ← CLI: python -m agents.main
│  ├─ personas/                      ← Um módulo por agente (builders OpenAI Agents SDK)
│  ├─ pipeline/                      ← run_pipeline, validação, governança, persistência (S3 opcional)
│  ├─ batch_process.py               ← IR ALÉM 2: lote ml_only (python -m agents.batch_process)
│  ├─ config.py                      ← OPENAI_API_KEY, MODEL_PATH, limiares, disclaimer
│  ├─ governance/                    ← IR ALÉM 1: coerência protocolo × classificação
│  ├─ tools/
│  │  ├─ risk_predictor.py           ← Tool: carrega modelo e faz predição
│  │  └─ protocol_database.py        ← Tool: consulta base de protocolos
│  ├─ data/
│  │  └─ protocols.json              ← Protocolos simulados para baixo/médio/alto
│  ├─ logs/                          ← Logs JSON de execução (no .gitignore — LGPD)
│  └─ tests/                         ← governança, lote, ML, protocolos (ver secção Testes)
│
├─ docs/
│  ├─ relatorio_parte1.md            ← Relatório Fase 6 Parte 1 (máx. 2 págs.)
│  ├─ arquitetura_multiagente.md          ← Parte 2: arquitetura (Markdown completo)
│  ├─ passo_a_passo_execucao_local_fase6.md ← Execução local Parte 1 + 2 (Windows)
│  ├─ docker_localstack.md         ← Docker Compose + LocalStack (S3 de logs)
│  ├─ glossario_unificado_cardioia.md     ← Coesão fases 1–6: termos e mapeamentos
│  ├─ relatorio_fase5.md             ← Relatório Fase 5
│  └─ arquitetura_solucao.md         ← Arquitetura da solução Fase 5
│
├─ backend/                          ← Fase 5: assistente conversacional Flask
├─ assistant/                        ← Fase 5: modelagem IBM Watson Assistant
├─ frontend/                         ← Fase 5: interface web
│
├─ .env.example                      ← Template de variáveis de ambiente
├─ Dockerfile                      ← Imagem da API + frontend estático
├─ docker-compose.yml              ← `web` + LocalStack (S3) para desenvolvimento local
├─ docker-compose.pull.yml         ← Mesmo stack com imagem já publicada (`CARDIOIA_IMAGE`)
├─ scripts/init_localstack_s3.py   ← Cria bucket no LocalStack antes do Flask
├─ scripts/docker-build-test-push.ps1 ← Build + pytest no container + push (Docker Hub / GHCR)
├─ requirements.txt                  ← Dependências Python (Fase 5 + Fase 6)
├─ requirements-notebook.txt         ← Jupyter / nbconvert (Parte 1 local)
└─ README.md
```

---

## ✅ Requisitos para Execução

- Python **3.10+**
- `pip` disponível no ambiente
- **Chave OpenAI** com API Key válida (`OPENAI_API_KEY`) — obrigatório para a Fase 6 Parte 2
- Jupyter local (VS Code ou `jupyter notebook`) para a Fase 6 Parte 1 — ver `requirements-notebook.txt`

---

## 🚀 Como Executar — Fase 6

**Passo a passo detalhado (local, Windows):** [`docs/passo_a_passo_execucao_local_fase6.md`](docs/passo_a_passo_execucao_local_fase6.md) — inclui `PATH` para `nbconvert`, `pytest` e `agents.main`.

### 1. Clonar o repositório e instalar dependências

```bash
git clone https://github.com/joseandrefilho/2TIAOR20242-CardioIA-Fase6-Cap1.git
cd 2TIAOR20242-CardioIA-Fase6-Cap1

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-notebook.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Abra .env e preencha OPENAI_API_KEY com sua chave
```

Conteúdo do `.env`:
```env
OPENAI_API_KEY=sk-...sua_chave_openai_aqui
OPENAI_MODEL=gpt-4o-mini
```

### 3. Parte 1 — Executar o Notebook **localmente** (Jupyter)

1. Com o `venv` ativo, instale também as ferramentas de notebook:  
   `pip install -r requirements-notebook.txt`
2. **VS Code / Cursor:** abra `notebooks/fase6_modelo_preditivo.ipynb`, escolha o interpretador Python do `venv` como kernel e use **Executar tudo** (Run All).
3. **Linha de comando (interface clássica):**
   ```bash
   cd notebooks
   jupyter notebook fase6_modelo_preditivo.ipynb
   ```
   No menu do notebook: **Kernel → Restart & Run All** (ou execute célula a célula).
4. **Linha de comando (executar tudo sem abrir o browser):** com o **`venv` ativado** e, no **Windows**, o `PATH` a começar por `venv\Scripts` (para o kernel não usar o Python global), na **raiz** do repositório:
   ```powershell
   $venvScripts = (Resolve-Path ".\venv\Scripts").Path
   $env:PATH = "$venvScripts;$env:PATH"
   jupyter nbconvert --to notebook --execute notebooks/fase6_modelo_preditivo.ipynb --output notebooks/fase6_modelo_preditivo_executed.ipynb --ExecutePreprocessor.timeout=600
   ```
   Isto corre todas as células e gera um `.ipynb` com saídas; o modelo é gravado em `ml/modelo_risco_cardiaco.joblib` (caminho `../ml/` relativamente à pasta `notebooks/` onde o kernel executa o código).

   > **Importante no Windows:** se aparecer `ModuleNotFoundError` para `matplotlib` ou `pandas`, prefira o bloco PowerShell acima ou o guia [`docs/passo_a_passo_execucao_local_fase6.md`](docs/passo_a_passo_execucao_local_fase6.md).

O notebook irá:

- Gerar dataset sintético (1000 registros)
- Treinar `RandomForestClassifier(n_estimators=100, random_state=42)`
- Exibir acurácia, classification report e matriz de confusão
- Simular previsão para um novo paciente
- Gravar `ml/modelo_risco_cardiaco.joblib` (sobrescreve o ficheiro existente se voltar a treinar)

> **Nota:** o repositório já inclui um `ml/modelo_risco_cardiaco.joblib` gerado com os mesmos parâmetros; voltar a executar o notebook **atualiza** esse ficheiro.

### 4. Parte 2 — Executar o Sistema Multiagente

Certifique-se de que `ml/modelo_risco_cardiaco.joblib` existe e `.env` está preenchido, então execute:

```bash
python -m agents.main
```

**Saída esperada no terminal:**

```
============================================================
  CARDIOIA FASE 6 — SISTEMA PREDITIVO MULTIAGENTE
============================================================

  Paciente: {'idade': 65, 'freq_cardiaca': 115, 'spo2': 91.5, ...}

  [Orquestrador] handoff: → Analista de Risco
  [Analista de Risco] tool_call: predict_risk_tool executada
  [Analista de Risco] handoff: → Especialista em Protocolos
  [Especialista em Protocolos] tool_call: get_protocols_tool executada
  [Especialista em Protocolos] handoff: → Orquestrador
  [Orquestrador] response: resposta final montada

  Log salvo em: agents/logs/<timestamp>_execution.json

============================================================
  RECOMENDAÇÃO FINAL — CardioIA Fase 6
============================================================
  Probabilidade de pico de risco : XX.X%
  Classificação de risco         : ALTO/MÉDIO/BAIXO
  Protocolos sugeridos: [...]
  AVISO: Esta análise é gerada por um sistema acadêmico simulado...
============================================================
```

O log completo é salvo automaticamente em `agents/logs/<timestamp>_execution.json`.

### 4b. Lote — vários pacientes (IR ALÉM 2)

Simulação de fila sequencial (sem infraestrutura distribuída real):

```bash
python -m agents.batch_process
```

Gera `agents/logs/batch_last_summary.json` com um objeto por caso (`ok`, `recommendation` ou `error`).

### 4c. Docker + LocalStack (opcional)

Na raiz do repositório, com Docker Desktop:

```powershell
docker compose up --build
```

Sobe **LocalStack** (S3 na porta **4566**) e o serviço **web** (API em **http://localhost:5000**). Os logs de predição podem ser copiados para o bucket configurado por `CARDIOIA_S3_LOG_BUCKET` quando `AWS_ENDPOINT_URL` aponta para o LocalStack. Guia detalhado: [`docs/docker_localstack.md`](docs/docker_localstack.md).

**CI (GHCR):** o workflow [`.github/workflows/docker-publish-and-test.yml`](.github/workflows/docker-publish-and-test.yml) faz build, **pytest na imagem** e push para `ghcr.io/<dono>/<repo>` (nomes em minúsculas). Ative com *Actions → Docker — testes na imagem e publicação (GHCR) → Run workflow* ou com push para `main`/`master`.

**Só imagem publicada + LocalStack:** `docker-compose.pull.yml` + variável `CARDIOIA_IMAGE` (ver `docs/docker_localstack.md`).

---

## 🧪 Testes Automatizados

### Fase 6 (`agents/tests/`)

```bash
pytest agents/tests/ -v
```

| Suite | O que valida |
|-------|--------------|
| `test_risk_predictor.py` | Limiares, chaves de saída, modelo ausente, cache por caminho |
| `test_protocol_database.py` | Protocolos por nível, chaves, nível inválido |
| `test_governance_coherence.py` | Coerência `risk_level` × classificação |
| `test_pipeline_ml_only.py` | Pipeline só ML + `governance` |
| `test_batch_process.py` | Lote `run_batch_ml_only` |
| `test_personas_smoke.py` | Import e nomes dos três builders de agente |

### Fase 5 + integração (`backend/tests/`)

```bash
pytest backend/tests/ -q
```

Inclui `/api/chat`, **`POST /api/predict-risk`**, **`GET /health`** (`fase6_prediction`), extração de parâmetros a partir do texto.

### Suíte completa (recomendado antes de entregar)

```bash
pytest backend/tests agents/tests -q
```

**Resultado esperado:** todos os testes passam (**65** casos: `backend/tests` + `agents/tests`).

---

## 📊 Resultados do Modelo (Parte 1)

| Métrica | Valor | Referência |
|---------|-------|-----------|
| Acurácia | **87,5%** | conjunto de teste (200 amostras) |
| Precisão classe 1 (Pico) | **95,0%** | 19 TP / (19 TP + 1 FP) |
| Recall classe 1 (Pico) | **44,2%** | 19 TP / (19 TP + 24 FN) |
| F1-Score classe 1 | **60,3%** | média harmônica entre precisão e recall |

**Matriz de Confusão:**

```
                 Predito: Sem Pico   Predito: Pico
Real: Sem Pico       TN = 156           FP = 1
Real: Pico           FN = 24            TP = 19
```

Os resultados indicam **boa especificidade para casos sem pico** e, ao mesmo tempo, **sensibilidade baixa para detectar picos reais** (24 falsos negativos), ponto central de melhoria para o contexto de triagem.

---

## 📚 Documentação Detalhada

### Fase 6

| Documento | Caminho | Conteúdo |
|-----------|---------|----------|
| Relatório Técnico Parte 1 | [`docs/relatorio_parte1.md`](docs/relatorio_parte1.md) | Justificativa do algoritmo, métricas reais, análise da matriz de confusão, limitações |
| Arquitetura Multiagente (completa) | [`docs/arquitetura_multiagente.md`](docs/arquitetura_multiagente.md) | Conformidade com enunciado, diagramas ASCII + Mermaid, handoffs/tools, histórico/validação, integração com `.joblib`, exemplo com valores verificados no modelo |
| Arquitetura Multiagente (PDF FIAP) | [`docs/arquitetura_multiagente_fiap_pdf.md`](docs/arquitetura_multiagente_fiap_pdf.md) | Versão condensada para anexo de até 3 páginas: diagrama, tabela de agentes, handoffs/tools/histórico/validação, exemplo E/S |
| Execução local (passo a passo) | [`docs/passo_a_passo_execucao_local_fase6.md`](docs/passo_a_passo_execucao_local_fase6.md) | venv, Parte 1 (VS Code + `nbconvert` com `PATH`), Parte 2 (`pytest` **65** testes, `agents.main`, `batch_process`, HTTP `/api/predict-risk`, UTF-8 Windows) |
| Glossário unificado | [`docs/glossario_unificado_cardioia.md`](docs/glossario_unificado_cardioia.md) | Termos canónicos, sinónimos, fases 1–6, mapeamento conversação → features ML |
| Notebook ML | [`notebooks/fase6_modelo_preditivo.ipynb`](notebooks/fase6_modelo_preditivo.ipynb) | Dataset, treino, avaliação, simulação de novo paciente |

### Fase 5 (base)

| Documento | Caminho | Conteúdo |
|-----------|---------|----------|
| Relatório Fase 5 | `docs/relatorio_fase5.md` | Metodologia, arquitetura conversacional, resultados |
| Arquitetura da Solução | `docs/arquitetura_solucao.md` | Componentes Flask, Watson, fluxo de dados |
| Fluxo Conversacional | `assistant/fluxo_conversacional.md` | Máquina de estados, estágios, exceções |
| Video Demonstração Fase 5 | [YouTube](https://youtu.be/dn5lhY7gvAY) | Gravação de tela ~3 min |

### Consolidado (Fases 0 a 6)

- Fonte de requisitos: enunciados em `.fiap/fases_unificadas/` (ex.: [**Fase 6 — enunciado e avaliação**](.fiap/fases_unificadas/fase06_enunciado_avaliacao.md))
- Critério de rastreabilidade: evidências de código/documentação no repositório + avaliações oficiais registradas em cada arquivo de fase

---

## ⚠️ Limitações

**Fase 6 — Sistema Preditivo:**
- Dataset 100% sintético: regras heurísticas de geração podem não refletir padrões clínicos reais.
- Modelo usa apenas 5 variáveis; dados reais incluiriam ECG, enzimas cardíacas, comorbidades.
- Avaliação com único split aleatório (sem validação cruzada).
- O sistema multiagente depende de conectividade com a API OpenAI.

**Fase 5 — Assistente Conversacional (base):**
- Fallback local usa regras simples por palavras-chave.
- Não há banco de dados nem histórico persistente de conversas.

> Em ambas as fases, o sistema não substitui avaliação médica profissional.

---

## ⚙️ Como Executar — Fase 5 (Backend)

```bash
cp .env.example .env
# Preencha variáveis Watson se disponível (opcional — modo offline funciona sem elas)
python -m backend.app
```

Acesse: `http://localhost:5000` — inclui o chat (Fase 5) e a etapa de **análise preditiva integrada** (Fase 6) no mesmo fluxo. Endpoints JSON: `POST /api/chat`, `POST /api/predict-risk`, `GET /health`.

Para configuração detalhada do IBM Watson Assistant, consulte [`docs/instrucoes_configuracao_watson.md`](docs/instrucoes_configuracao_watson.md).

---

## 📝 Licença

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
Este projeto segue o modelo FIAP e está licenciado sob
<a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer">Attribution 4.0 International (CC BY 4.0)</a>.
</p>
