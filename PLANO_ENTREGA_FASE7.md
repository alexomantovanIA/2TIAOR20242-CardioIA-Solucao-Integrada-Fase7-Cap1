# Plano de Entrega — Fase 7 (sem IR Além)

Documento criado para guiar a execução passo a passo dos itens faltantes
para entrega da Fase 7 do CardioIA. Execute na ordem indicada.

## Status dos passos

- [x] PASSO 1: Wokwi
- [x] PASSO 2: Entra ID Azure
- [x] PASSO 3: Backend .env
- [ ] PASSO 4: Deploy Vercel
- [ ] PASSO 5: EAS Build APK
- [ ] PASSO 6: Relatório PDF
- [ ] PASSO 7: Gravar vídeo
- [ ] PASSO 8: Atualizar README

---

## Contexto

O código está 100% pronto. O que falta são os artefatos de publicação e documentação:

| Item faltante | Onde preencher depois |
|---|---|
| URL pública Web (Vercel) | `README.md` linha 11 |
| Link/QR do APK (EAS) | `README.md` linha 12 |
| Link público do Wokwi | `README.md` linha 13 |
| Link do vídeo demonstrativo | `README.md` linha 14 |
| Relatório PDF (máx 5 pág) | Entregar junto com o repositório |

---

## PASSO 1 — Wokwi (~20 min)

O código já está pronto em `iot/main.py` e `iot/diagram.json`.

1. Acesse wokwi.com e faça login
2. New Project → selecione ESP32
3. Substitua o conteúdo do arquivo `main.py` pelo conteúdo de `iot/main.py`
4. Clique no ícone de arquivo → Add file → crie `diagram.json` e cole o conteúdo de `iot/diagram.json`
5. Clique em Play — verifique no console: `CardioIA IoT | FC: XX bpm | Temp: XX C | SpO2: XX% | Status: normal/atencao/critico`
6. Verifique o LED RGB mudando de cor (verde = normal, amarelo = atencao, vermelho = critico)
7. Clique em Share → Make public → copie a URL

**Evidência a guardar:** link público + print do console em execução

---

## PASSO 2 — Entra ID no Azure (~45 min)

Pré-requisito: conta em portal.azure.com com acesso ao Microsoft Entra ID.

### 2a) App da API (backend)

1. portal.azure.com → Microsoft Entra ID → App registrations → New registration
   - Nome: `cardioia-api`
   - Supported account types: `Accounts in this organizational directory only (Single tenant)`
   - Clique em Register
2. Expose an API → Set → aceite o URI `api://<CLIENT_ID>` → Add a scope
   - Scope name: `access_as_user`
   - Who can consent: `Admins and users`
   - Admin consent display name: `Acessar API CardioIA`
   - State: Enabled
   - Add scope
3. **Anote:**
   - `TENANT_ID` (visível na Overview da app registration)
   - `API_CLIENT_ID` (Application (client) ID na Overview)

### 2b) App da Web (SPA)

1. App registrations → New registration
   - Nome: `cardioia-web` | Single tenant
   - Redirect URI: plataforma `Single-page application (SPA)` → `http://localhost:5173`
   - Register
2. API permissions → Add a permission → My APIs → `cardioia-api` → marque `access_as_user` → Add
3. Grant admin consent for [seu tenant]
4. **Anote:** `WEB_CLIENT_ID` (Application (client) ID)
5. Após o deploy Vercel (Passo 4): voltar aqui em Authentication → Add URI → `https://SEU_APP.vercel.app`

### 2c) App do Mobile

1. App registrations → New registration
   - Nome: `cardioia-mobile` | Single tenant | Register
2. Authentication → Add a platform → Mobile and desktop applications
   - Adicione os redirect URIs:
     - `exp://127.0.0.1:19000/--/auth`
     - `cardioiafase7://auth`
   - Habilite: Allow public client flows = Yes
3. API permissions → Add a permission → My APIs → `cardioia-api` → `access_as_user` → Add
4. Grant admin consent
5. **Anote:** `MOBILE_CLIENT_ID`

---

## PASSO 3 — Atualizar .env do backend (~10 min)

Edite o arquivo `.env` na raiz do projeto com os valores obtidos no Passo 2:

```env
AUTH_ENABLED=true
ENTRA_TENANT_ID=<TENANT_ID>
ENTRA_AUDIENCE=api://<API_CLIENT_ID>
ENTRA_ISSUER=https://login.microsoftonline.com/<TENANT_ID>/v2.0
```

Teste local:

```bash
.venv311/Scripts/python -m backend.app
curl http://localhost:5000/health        # deve retornar 200
curl http://localhost:5000/api/chat      # deve retornar 401 (sem token)
```

---

## PASSO 4 — Deploy Vercel (~20 min)

Pré-requisito: conta em vercel.com e repositório no GitHub.

1. vercel.com → New Project → importe o repositório GitHub
2. **Root Directory:** `apps/web`
3. Framework Preset: Vite (detecta automaticamente)
4. Environment Variables — adicione:
   ```
   VITE_API_BASE_URL        = https://URL_DO_BACKEND (ou http://localhost:5000 para demo local)
   VITE_ENTRA_TENANT_ID     = <TENANT_ID>
   VITE_ENTRA_WEB_CLIENT_ID = <WEB_CLIENT_ID>
   VITE_ENTRA_API_SCOPE     = api://<API_CLIENT_ID>/access_as_user
   ```
   > Se o backend não tiver URL pública, use o Render.com (free tier) para publicar o Flask,
   > ou grave o vídeo com backend rodando localmente.
5. Deploy → aguarde → copie a URL `https://xxx.vercel.app`
6. Volte no Passo 2b → Authentication → adicione a URL da Vercel como Redirect URI

**Evidência a guardar:** URL pública + print do dashboard Vercel com status "Ready"

---

## PASSO 5 — EAS Build APK (~30 min, roda em nuvem)

Execute dentro de `apps/mobile`:

```bash
cd apps/mobile
npx eas login
npx eas build --platform android --profile preview
```

- O build roda em nuvem (15–30 min)
- Acompanhe em expo.dev/builds
- Quando terminar: baixe o `.apk` → instale em dispositivo Android
  (Configurações → Segurança → Instalar de fontes desconhecidas)

**Enquanto o build roda:** execute os Passos 6 e prepare o roteiro do vídeo.

**Evidência a guardar:** link do Expo Dashboard + QR Code + print do APK instalado

---

## PASSO 6 — Relatório PDF (~10 min)

O conteúdo já está pronto em `docs/relatorio_fase7.md`.

**Opção A — VS Code:**
- Instale a extensão "Markdown PDF"
- Abra `docs/relatorio_fase7.md`
- Clique com botão direito → "Markdown PDF: Export (pdf)"
- Arquivo gerado: `docs/relatorio_fase7.pdf`

**Opção B — Pandoc (terminal):**
```bash
pandoc docs/relatorio_fase7.md -o docs/relatorio_fase7.pdf
```

**Opção C — Manual:**
- Abra o arquivo, selecione tudo, cole no Google Docs → Arquivo → Baixar como PDF

Verifique que o PDF tem no **máximo 5 páginas**.

O diagrama de arquitetura está em `docs/arquitetura_final.mmd`.
Renderize em mermaid.live para incluir como imagem no relatório se necessário.

---

## PASSO 7 — Gravar o Vídeo (~30 min)

Roteiro completo em `docs/roteiro_video.md`. Resumo dos 5 minutos:

| Tempo | Cena | O que mostrar |
|-------|------|---------------|
| 0:00–0:30 | Abertura | CardioIA Fase 7, aviso acadêmico |
| 0:30–1:15 | Arquitetura | Diagrama: Sensor → MicroPython → Backend → IA → UI |
| 1:15–2:00 | Backend | Terminal com `/health` + curls dos endpoints |
| 2:00–2:45 | Wokwi | Console com leituras + LED RGB mudando |
| 2:45–3:35 | Web (Vercel) | Login Entra ID + dashboard + card risco + chat |
| 3:35–4:25 | Mobile (APK) | Login + home + vitais + chat + recomendações |
| 4:25–5:00 | Validação | `pytest` passando + `npm run build` + encerramento |

Ferramenta sugerida: OBS Studio (gratuito) ou Loom.

---

## PASSO 8 — Atualizar README (~15 min)

Após ter todos os links, edite o `README.md`:

1. Linha 11: substituir `PREENCHER_APOS_DEPLOY` → URL real da Vercel
2. Linha 12: substituir `PREENCHER_APOS_EAS_BUILD` → link/QR do Expo Dashboard
3. Linha 13: substituir `PREENCHER_APOS_PUBLICAR_WOKWI` → link público do Wokwi
4. Linha 14: substituir `PREENCHER_APOS_GRAVACAO` → link do YouTube/vídeo

5. Marcar todos os checkboxes do checklist (linhas 22–28)

6. Adicionar lista dos integrantes na seção Fase 7 para garantir o ponto extra:
   ```markdown
   ## Integrantes
   - Alexandre Oliveira Mantovani
   - Edmar Ferreira Souza
   - Ricardo Lourenço Coube
   - Jose Andre Filho
   ```

7. Remover ou mover o bloco da Fase 6 do final do README
   (tudo a partir da linha que começa com `# FIAP - Faculdade...`)

8. Adicionar prints de deploy, build e Wokwi como imagens no README

---

## Links de entrega (preencher ao longo dos passos)

| Item | Link |
|---|---|
| Vercel Web | — |
| APK / Expo Dashboard | — |
| Wokwi público | https://wokwi.com/projects/464903322431038465 |
| Vídeo demonstrativo | — |
| Relatório PDF | `docs/relatorio_fase7.pdf` |

---

## Pontuação esperada após completar todos os passos

| Critério | Peso | Meta |
|---|---|---|
| URLs funcionais (Web + APK) | 3,0 | 3,0 |
| Unificação backend + IA + UI | 2,5 | 2,5 |
| Sensores no Wokwi | 1,5 | 1,5 |
| Diagrama + fluxo de dados | 1,5 | 1,5 |
| README + PDF + vídeo | 1,5 | 1,5 |
| Extra (equipe 4 integrantes) | 1,0 | 1,0 |
| **Total** | **10 + 1** | **11,0** |
