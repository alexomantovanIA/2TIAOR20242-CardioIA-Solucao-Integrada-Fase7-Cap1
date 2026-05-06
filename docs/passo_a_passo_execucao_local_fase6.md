# Passo a passo — execução local (Fase 6)

**Objetivo:** validar a **Parte 1** (notebook + modelo) e a **Parte 2** (testes + pipeline multiagente + integração HTTP) **sem Google Colab**, no Windows (PowerShell).  
**Última verificação no repositório:** 2026-04-25 — `pytest backend/tests agents/tests -q`: **65 passed**; notebook executável com `nbconvert` após corrigir o `PATH` do `venv`.

---

## Pré-requisitos

- Python **3.10+** instalado e disponível no `PATH` como `python`.
- Conta OpenAI com **API Key** para o pipeline completo com LLM (`python -m agents.main` ou `POST /api/predict-risk` com `mode=agents`). Para laboratório **sem** OpenAI: use `mode=ml_only` no HTTP ou `python -m agents.batch_process`.
- PowerShell na raiz do clone (ajuste o caminho ao seu ambiente).

---

## 1. Ambiente virtual e dependências

Na **raiz** do repositório:

```powershell
cd c:\Fiap\dev\2TIAOR20242-CardioIA-Fase6-Cap1

# Criar o venv (só precisa uma vez)
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Dependências do projeto + ferramentas de notebook
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-notebook.txt
```

**Verificação rápida:** o interpretador ativo deve ser o do projeto:

```powershell
python -c "import sys; print(sys.executable)"
```

Deve terminar em `...\venv\Scripts\python.exe`.

---

## 2. Parte 1 — Notebook (`notebooks/fase6_modelo_preditivo.ipynb`)

### Opção A — Cursor / VS Code (recomendado)

1. Abra a pasta do repositório no editor.
2. Abra `notebooks/fase6_modelo_preditivo.ipynb`.
3. **Selecionar kernel:** o Python do `venv` (`.\venv\Scripts\python.exe`).
4. **Executar tudo** (Run All).

**Resultado esperado:** células com dataset, treino, métricas, matriz de confusão, simulação de paciente e gravação de `ml/modelo_risco_cardiaco.joblib`.

### Opção B — Linha de comando (`jupyter nbconvert`)

No Windows, o `jupyter` do **Python global** pode aparecer **antes** do do `venv` no `PATH`, e o kernel executa **sem** `matplotlib` do projeto. **Coloque o `Scripts` do `venv` no início do `PATH`** na mesma sessão:

```powershell
cd c:\Fiap\dev\2TIAOR20242-CardioIA-Fase6-Cap1
.\venv\Scripts\Activate.ps1

$venvScripts = (Resolve-Path ".\venv\Scripts").Path
$env:PATH = "$venvScripts;$env:PATH"

jupyter nbconvert --to notebook --execute "notebooks\fase6_modelo_preditivo.ipynb" --output "fase6_modelo_preditivo_executed.ipynb" --output-dir "notebooks" --ExecutePreprocessor.timeout=600
```

**Resultado observado em 2026-04-21:** conversão concluída; ficheiro gerado `notebooks\fase6_modelo_preditivo_executed.ipynb` (~109 KB). Este ficheiro está no `.gitignore` (`notebooks/*_executed.ipynb`) para não poluir o Git.

**Modelo:** o notebook grava `ml\modelo_risco_cardiaco.joblib` (caminho relativo à pasta `notebooks/`). Após execução bem-sucedida, confira data/tamanho do ficheiro em `ml\`.

---

## 3. Testes automáticos (backend + agents)

Com o `venv` ativo, na raiz:

```powershell
pytest agents/tests/ -v
pytest backend/tests/ -q
pytest backend/tests agents/tests -q
```

**Resultado esperado:** suites **agents** e **backend** a verde; comando completo típico: **`65 passed`**.

| Área | Pastas | Conteúdo resumido |
|------|--------|-------------------|
| Agents | `agents/tests/` | ML, protocolos, governança, pipeline `ml_only`, lote |
| Backend | `backend/tests/` | Chat, segurança, health (incl. `fase6_prediction`), `POST /api/predict-risk`, extração de texto |

---

## 4. Parte 2 — Pipeline multiagente (`python -m agents.main`)

### 4.1 Variáveis de ambiente

```powershell
Copy-Item .env.example .env
# Edite .env e preencha OPENAI_API_KEY=sk-...
```

Opcional: `OPENAI_MODEL=gpt-4o-mini` (ou outro modelo suportado pela sua chave).

### 4.2 UTF-8 no terminal (Windows)

Para evitar erros de encoding no consola ao imprimir texto com acentos ou símbolos, recomenda-se:

```powershell
$env:PYTHONUTF8 = "1"
```

### 4.3 Executar

```powershell
cd c:\Fiap\dev\2TIAOR20242-CardioIA-Fase6-Cap1
.\venv\Scripts\Activate.ps1
python -m agents.main
```

**Resultado esperado:** banners no terminal, linhas de fluxo (handoff / tool), recomendação final com **probabilidade**, **classificação**, **protocolos**, **disclaimer** e **`governance`**; mensagem **Log salvo em:** `agents\logs\<timestamp>_<id>_execution.json` (nome único por execução).

**Nota:** o `run_pipeline` tenta extrair JSON do texto final do Orquestrador. Se o LLM omitir campos, o código **preenche** `probability`, `risk_classification` e `suggested_protocols` com as mesmas funções determinísticas usadas pelas tools (`predict_risk` + `get_protocols`), para a validação de saída e a demo não dependerem do formato perfeito do modelo de linguagem.

### 4.4 Ajuste feito no código (Windows)

Os separadores de handoff no log do terminal usam agora **`->`** em vez do carácter Unicode `→`, para compatibilidade com consolas **cp1252** sem `PYTHONUTF8`.

---

## 5. Integração web (Flask) — predição e health

Com o backend a correr (`python -m backend.app`):

1. **`GET /health`** — deve incluir `fase6_prediction` com prontidão do modelo e dependências.
2. **`POST /api/predict-risk`** — corpo JSON com os cinco campos numéricos; use `mode: "ml_only"` se não tiver `OPENAI_API_KEY` no servidor.
3. **`POST /api/chat`** — mensagens com dados vitais reconhecíveis podem devolver **`predictive_suggestion`** (ponte conversação -> etapa preditiva no proprio chat).
4. **Interface web** — abra `http://localhost:5000` no browser:
   - Escreva um sintoma (ex.: "Estou com palpitações frequentes há 2 dias")
   - O assistente responde e exibe um **mini-formulário preditivo embutido** no chat
   - Preencha os 5 campos (idade, FC, SpO2, sliders de carga e disponibilidade) e confirme
   - A avaliação multiagente aparece diretamente na conversa com badge "Multiagentes (Fase 6)"

Detalhes de contrato: `backend/routes/prediction_routes.py`, `backend/routes/chat_routes.py`, `frontend/script.js`.

---

## 6. Lote simulado (IR ALÉM 2)

Na raiz, com `venv` ativo:

```powershell
python -m agents.batch_process
```

**Resultado esperado:** três casos processados em sequência; ficheiro **`agents/logs/batch_last_summary.json`** com resumo por índice.

---

## 7. Checklist rápido

| Passo | Comando / ação | Sucesso |
|--------|----------------|---------|
| Dependências | `pip install -r requirements.txt -r requirements-notebook.txt` | Sem erros |
| Parte 1 (UI) | VS Code → Run All no `.ipynb` com kernel do `venv` | Métricas + `ml/*.joblib` |
| Parte 1 (CLI) | `PATH` com `venv\Scripts` primeiro + `jupyter nbconvert --execute ...` | Ficheiro `*_executed.ipynb` |
| Testes | `pytest backend/tests agents/tests -q` | `65 passed` |
| Parte 2 (API LLM) | `.env` + `python -m agents.main` | Recomendação + log em `agents/logs/` |
| Parte 2 (HTTP) | Flask + `POST /api/predict-risk` (`ml_only` ou `agents`) | JSON com `recommendation` + `governance` |
| IR ALÉM 2 | `python -m agents.batch_process` | `batch_last_summary.json` |

---

## 8. Referências no repositório

- Instruções resumidas no **README:** secções **Como Executar — Fase 6** e **Testes**.
- Notebook: `notebooks/fase6_modelo_preditivo.ipynb`.
- Pipeline CLI: `agents/main.py` (`python -m agents.main`).
- Lote: `agents/batch_process.py` (`python -m agents.batch_process`).
- Governança: `agents/governance/coherence.py`.
- Contrato de demo: `specs/003-unify-multi-agent-solution/contracts/unified-demo-flow.md` (v1.1).
