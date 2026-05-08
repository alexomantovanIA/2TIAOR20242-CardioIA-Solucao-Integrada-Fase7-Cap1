# Quickstart - Fase 7 MVP Integrado

## 1. Backend

```bash
python -m venv .venv311
.venv311\Scripts\pip install -r requirements.txt
set PORT=5000
.venv311\Scripts\python -m backend.app
```

## 2. Web

```bash
cd apps/web
npm install
npm run build
npm run dev
```

## 3. Mobile

```bash
cd apps/mobile
npm install
npx expo-doctor
npx expo start
```

APK de preview:

```bash
npx eas build --platform android --profile preview
```

## 4. IoT (MicroPython/Wokwi)

- Abrir projeto Wokwi com `iot/main.py`.
- Ajustar `API_URL` quando quiser enviar dados ao backend.
- Verificar mudanca de status visual (`normal|atencao|critico`).

## 5. Autenticacao Entra ID (single-tenant)

- Configurar app registration para Web/Mobile e API.
- Garantir que tokens emitidos tenham tenant e audience esperados.
- Validar:
  - `/health` acessivel sem token.
  - `/api/*` retorna `401` sem token.
  - `/api/*` retorna `200` com token valido.

## 6. Validacoes obrigatorias antes da avaliacao

```bash
pytest backend/tests agents/tests -q
```

```bash
cd apps/web && npm run build
```

```bash
cd apps/mobile && npx expo-doctor
```

Checklist final:

- URL publica da Web preenchida no README.
- Link/QR do APK final preenchido no README.
- Link Wokwi publico valido.
- Video demonstrativo publicado e referenciado.
