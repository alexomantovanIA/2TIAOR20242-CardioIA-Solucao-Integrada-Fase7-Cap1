# Guia Detalhado - Entra ID, Testes e Publicacao (Fase 7)

Este documento descreve o passo a passo completo para:

1. Configurar autenticacao real com Microsoft Entra ID (single-tenant)
2. Validar o fluxo protegido no backend, Web e Mobile
3. Publicar Web (Vercel), gerar APK (Expo EAS) e fechar evidencias de entrega

Escopo alinhado a Fase 7 obrigatoria, sem IR ALEM.

---

## 1. Pre-requisitos

- Conta Azure com acesso ao Microsoft Entra ID
- Conta Vercel
- Conta Expo (EAS)
- Node.js e npm instalados
- Python 3.11+ instalado
- Git configurado

Recomendado:

- Navegador logado no tenant correto do Entra ID
- Projeto já atualizado na branch `005-fase7-mvp`

---

## 2. Configurar Entra ID (single-tenant)

### 2.1 Criar App Registration da API (backend)

No portal Azure:

1. Acesse `Microsoft Entra ID` -> `App registrations` -> `New registration`
2. Nome: `cardioia-api`
3. Supported account types: `Accounts in this organizational directory only (Single tenant)`
4. Clique em `Register`

Depois da criacao:

1. Abra `Expose an API`
2. Clique em `Set` para `Application ID URI`
   - Sugestao: `api://<API_CLIENT_ID>`
3. Clique em `Add a scope`
   - Scope name: `access_as_user`
   - Who can consent: `Admins and users`
   - Admin consent display name: `Acessar API CardioIA`
   - Admin consent description: `Permite acesso aos endpoints protegidos da API`
   - User consent display name: `Acessar API CardioIA`
   - User consent description: `Permite acesso aos endpoints protegidos da API`
   - State: `Enabled`
4. Salve

Anote os valores:

- `TENANT_ID`
- `API_CLIENT_ID`
- `APPLICATION_ID_URI` (ex.: `api://<API_CLIENT_ID>`)

### 2.2 Criar App Registration da Web (SPA)

1. `App registrations` -> `New registration`
2. Nome: `cardioia-web`
3. Single tenant
4. Redirect URI:
   - Platform: `Single-page application (SPA)`
   - URI dev: `http://localhost:5173`
5. Register

Depois:

1. `Authentication` -> adicione URI de producao:
   - `https://SEU_DEPLOY.vercel.app`
2. `API permissions` -> `Add a permission` -> `My APIs` -> selecione `cardioia-api`
3. Marque o scope `access_as_user`
4. Clique em `Grant admin consent` (quando aplicavel)

Anote:

- `WEB_CLIENT_ID`

### 2.3 Criar App Registration do Mobile (Expo)

1. `App registrations` -> `New registration`
2. Nome: `cardioia-mobile`
3. Single tenant
4. Register

Depois:

1. `Authentication` -> `Add a platform` -> `Mobile and desktop applications`
2. Adicione redirect URIs conforme fluxo adotado:
   - `exp://127.0.0.1:19000/--/auth` (dev comum Expo)
   - `cardioiafase7://auth` (se usar scheme custom)
3. Em `Advanced settings`, habilite `Allow public client flows` se necessario
4. `API permissions` -> adicione `cardioia-api/access_as_user`
5. `Grant admin consent` (quando aplicavel)

Anote:

- `MOBILE_CLIENT_ID`

---

## 3. Configurar variaveis no backend

Na raiz do projeto, ajuste `.env` (ou variaveis de ambiente do sistema):

```env
AUTH_ENABLED=true
ENTRA_TENANT_ID=<TENANT_ID>
ENTRA_AUDIENCE=cardioia-api
ENTRA_ISSUER=https://login.microsoftonline.com/<TENANT_ID>/v2.0
```

Observacao importante sobre `aud`:

- Se o token vier com `aud=api://<API_CLIENT_ID>`, ajuste `ENTRA_AUDIENCE` para esse valor.
- O valor de `ENTRA_AUDIENCE` deve bater exatamente com o `aud` do token recebido.

---

## 4. Configurar Web e Mobile para login Entra ID

### 4.1 Web

No frontend web, configure:

- `CLIENT_ID` da app `cardioia-web`
- `TENANT_ID`
- scope `api://<API_CLIENT_ID>/access_as_user` (ou conforme URI configurada)

Em ambiente local, mantenha:

```env
VITE_API_BASE_URL=http://localhost:5000
```

Em producao (Vercel), configure:

- `VITE_API_BASE_URL=https://URL_PUBLICA_DO_BACKEND`

### 4.2 Mobile

No app Expo, configure:

- `MOBILE_CLIENT_ID`
- `TENANT_ID`
- redirect URI compativel com o app
- scope da API (`access_as_user`)

Variavel existente:

```env
EXPO_PUBLIC_API_BASE_URL=http://localhost:5000
```

---

## 5. Subir ambiente local

### 5.1 Backend

```bash
python -m venv .venv311
.venv311\Scripts\pip install -r requirements.txt
set PORT=5000
.venv311\Scripts\python -m backend.app
```

### 5.2 Web

```bash
cd apps/web
npm install
npm run dev
```

### 5.3 Mobile

```bash
cd apps/mobile
npm install
npx expo start
```

---

## 6. Testar autenticacao e protecao de rotas

### 6.1 Testes esperados

- `GET /health` sem token -> `200`
- `/api/*` sem token -> `401`
- `/api/*` com token invalido -> `401`
- `/api/*` com token de outro tenant -> `401`
- `/api/*` com token valido -> `200`

### 6.2 Teste rapido com suite automatizada

Na raiz:

```bash
pytest backend/tests agents/tests -q
```

Resultado esperado atual: todos os testes passando.

---

## 7. Validacoes tecnicas obrigatorias antes da banca

### 7.1 Backend/IA

```bash
pytest backend/tests agents/tests -q
```

### 7.2 Web build

```bash
cd apps/web
npm run build
```

### 7.3 Mobile health check

```bash
cd apps/mobile
npx expo-doctor
```

### 7.4 Meta de performance (p95)

Validar benchmark de `POST /api/full-analysis` autenticado.

Meta: `p95 <= 3s` (em demo).  
Referencia atual do projeto: p95 em milissegundos, muito abaixo da meta.

---

## 8. Publicar Web (Vercel)

1. Conecte o repositorio na Vercel
2. Defina `Root Directory = apps/web`
3. Garanta que `vercel.json` esta sendo aplicado
4. Configure variaveis de ambiente (principalmente `VITE_API_BASE_URL`)
5. Execute deploy
6. Teste:
   - app abre
   - login Entra ID funciona
   - chamadas protegidas funcionam com token

Guardar evidencia:

- URL publica da Web
- print da tela de deploy OK

---

## 9. Gerar APK (Expo EAS)

No mobile:

```bash
cd apps/mobile
npx eas login
npx eas build --platform android --profile preview
```

Ao concluir:

- copiar link do build no dashboard Expo
- gerar/guardar QR Code
- instalar APK em dispositivo real e validar login + fluxo principal

Guardar evidencia:

- link/QR do APK
- print da instalacao/execucao

---

## 10. Publicar simulacao Wokwi

1. Abrir projeto Wokwi do `iot/`
2. Validar leituras + LED RGB
3. Publicar projeto como publico
4. Copiar URL publica

Guardar evidencia:

- link Wokwi
- print do circuito/console em execucao

---

## 11. Fechar documentacao de entrega

Atualize no `README.md`:

- `Vercel Web`
- `APK/Expo Dashboard ou QR Code`
- `Wokwi publico`
- `Video demonstrativo`

Revise:

- `docs/relatorio_fase7.md`
- `docs/roteiro_video.md`
- `docs/fase7_checklist_entrega.md`

---

## 12. Checklist final (go/no-go)

Antes da submissao:

- [ ] Login Entra ID funcionando no Web
- [ ] Login Entra ID funcionando no Mobile
- [ ] `/health` publico retorna 200
- [ ] `/api/*` sem token retorna 401
- [ ] `/api/*` com token valido retorna 200
- [ ] `pytest` passando
- [ ] `npm run build` web passando
- [ ] `expo-doctor` mobile passando
- [ ] URL web publicada
- [ ] APK gerado e testado em device real
- [ ] Wokwi publico com link valido
- [ ] Relatorio e video prontos

Se todos os itens acima estiverem OK, o projeto esta pronto para entrega da Fase 7 com foco na nota maxima (escopo obrigatorio).
