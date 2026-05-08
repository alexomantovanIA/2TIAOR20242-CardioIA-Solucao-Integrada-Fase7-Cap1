# Relatorio Tecnico - CardioIA Fase 7

## 1. Objetivo

O objetivo da Fase 7 foi entregar um MVP final integrado da plataforma CardioIA, consolidando o backend Flask e o modelo RandomForestClassifier da Fase 6 com novas interfaces Web, Mobile e um fluxo IoT simulado em MicroPython/Wokwi.

O sistema tem finalidade estritamente academica. Ele nao realiza diagnostico definitivo, nao substitui avaliacao medica e nao deve ser usado para decisoes clinicas reais.

## 2. Arquitetura

O fluxo integrado segue a cadeia:

Sensor simulado -> ESP32 MicroPython -> Backend Python -> IA/ML -> Web React e Mobile Expo.

O backend e o ponto integrador. Ele recebe leituras IoT em `/api/iot/ingest`, mantem a ultima leitura em memoria/JSON local, transforma os sinais em payload numerico compativel com o modelo da Fase 6 e disponibiliza o resumo em `/api/dashboard/summary`. O endpoint `/api/full-analysis` combina mensagem textual, dados do paciente, classificacao preditiva e resposta segura do assistente.

## 3. Backend e IA

Foi mantido o backend Flask da Fase 6 como base principal. Os endpoints existentes `/health`, `/api/chat` e `/api/predict-risk` foram preservados, e os endpoints integradores foram adicionados:

- `POST /api/iot/ingest`
- `GET /api/dashboard/summary`
- `GET /api/patient/latest`
- `POST /api/full-analysis`

O modo padrao e `ml_only`, usando o arquivo `ml/modelo_risco_cardiaco.joblib`. OpenAI Agents e Watson permanecem opcionais via variaveis de ambiente. Sem chaves, o sistema opera com fallback local seguro.

## 4. Web e Mobile

A Web foi criada em `apps/web` com React, Vite e TypeScript. Ela inclui login com Entra ID (single-tenant), dashboard de sinais vitais, card de risco, chat cardiologico, historico simples e tela Sobre. O deploy na Vercel e preparado por `vercel.json`, com rewrite para `/index.html`.

O Mobile foi criado em `apps/mobile` com React Native e Expo. Ele inclui login com Entra ID (single-tenant), home com risco atual, sinais vitais, chat, recomendacoes e sobre. O `app.json` define `android.package` como `br.com.fiap.cardioiafase7`, e o `eas.json` possui profile `preview` com APK.

## 5. IoT MicroPython

O diretorio `iot/` contem `main.py` e `diagram.json` para Wokwi. O ESP32 simula frequencia cardiaca, temperatura e SpO2, classifica o status em `normal`, `atencao` ou `critico`, exibe feedback por LED RGB e pode enviar POST opcional para o backend.

## 6. Validacao

Comandos executados:

- `pytest backend/tests agents/tests -q`: 76 testes passaram.
- `cd apps/web && npm run lint`: sem erros.
- `cd apps/web && npm run build`: build Vite concluido.
- `cd apps/web && npm run preview`: servidor de preview iniciou.
- `cd apps/mobile && npx expo-doctor`: 17/17 checks passaram.
- `cd apps/mobile && npx expo start`: Metro iniciou e exibiu QR/URL.
- `curl /api/iot/ingest`: leitura aceita com status `atencao`.
- `curl /api/full-analysis`: resposta combinada com chat fallback local e risco `médio`.
- benchmark autenticado `/api/full-analysis` (100 req): `p95=15.97ms`, `media=66.49ms`.

## 7. Limitacoes

O MVP nao possui banco de dados, historico persistente completo, consentimento LGPD formal ou deploy backend publico configurado neste workspace. As URLs publicas da Vercel, APK/Expo e Wokwi devem ser preenchidas apos publicacao. A visao computacional pesada ficou fora do fluxo principal por decisao de custo e estabilidade.
