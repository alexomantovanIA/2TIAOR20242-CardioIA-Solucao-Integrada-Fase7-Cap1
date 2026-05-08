# Roteiro de Video - CardioIA Fase 7

Duração maxima: 5 minutos.

## 0:00 - 0:30 | Abertura

Apresentar o CardioIA Fase 7 como MVP academico FIAP integrado. Reforcar: "Sistema acadêmico. Não substitui avaliação médica."

## 0:30 - 1:15 | Arquitetura

Mostrar o diagrama:

Sensor -> MicroPython -> Backend Python -> IA/ML -> Web/Mobile.

Explicar que a base principal e a Fase 6, reutilizando backend Flask, modelo `.joblib`, pipeline `ml_only` e fallback local.

## 1:15 - 2:00 | Backend

Executar ou mostrar:

```bash
PORT=5000 .venv311/bin/python -m backend.app
curl http://127.0.0.1:5000/health
```

Mostrar os endpoints `/api/iot/ingest`, `/api/dashboard/summary` e `/api/full-analysis`.

## 2:00 - 2:45 | IoT Wokwi

Abrir Wokwi com `iot/main.py`.

Mostrar o console com `heart_rate`, `temperature`, `spo2` e `status`. Mostrar LED RGB:

- Verde: normal.
- Amarelo: atencao.
- Vermelho: critico.

## 2:45 - 3:35 | Web

Abrir a Web Vercel ou local.

Mostrar:

- Login real via Entra ID (single-tenant).
- Dashboard com sinais vitais.
- Card de risco.
- Simular leitura.
- Chat cardiologico.
- Historico.
- Tela Sobre.

## 3:35 - 4:25 | Mobile

Abrir Expo Go/APK.

Mostrar:

- Login real via Entra ID (single-tenant).
- Home com risco atual.
- Sinais vitais.
- Chat.
- Recomendacoes.
- Sobre.

## 4:25 - 5:00 | Validacao e encerramento

Mostrar rapidamente:

```bash
pytest backend/tests agents/tests -q
cd apps/web && npm run build
cd apps/mobile && npx expo-doctor
```

Encerrar reforcando limitacoes: uso academico, dados simulados, sem diagnostico definitivo, OpenAI/Watson opcionais.
