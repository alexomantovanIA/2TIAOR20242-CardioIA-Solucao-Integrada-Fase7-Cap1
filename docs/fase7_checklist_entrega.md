# Checklist de Entrega - Fase 7 (Sem IR ALÉM)

Este checklist cobre exclusivamente os requisitos obrigatorios do enunciado
`.fiap/fases_unificadas/fase07_enunciado_avaliacao.md`.

## 1) Deploy e distribuicao profissional

- [ ] Web publicado e acessivel publicamente.
- [ ] `apps/web/vercel.json` com rewrite SPA valido.
- [ ] Deploy automatico por push no GitHub configurado na plataforma escolhida.
- [ ] Mobile com `apps/mobile/app.json` contendo `android.package` em dominio invertido.
- [ ] Mobile com `apps/mobile/eas.json` contendo profile `preview` para APK.
- [ ] APK gerado em nuvem e testado em dispositivo real.

## 2) Integracao tecnica obrigatoria

- [ ] Backend Python integrador em funcionamento (`backend/app.py`).
- [ ] Endpoints principais testados: `health`, `chat`, `predict-risk`, `iot/ingest`.
- [ ] Script MicroPython funcional em `iot/main.py`.
- [ ] Simulacao Wokwi publica com leitura e feedback visual (LED/OLED).
- [ ] Fluxo completo comprovado: Sensor -> MicroPython -> Backend -> IA -> UI.

## 3) Evidencias e documentacao

- [ ] README com URL Web, link/QR do APK, link Wokwi e instrucoes.
- [ ] Relatorio tecnico (PDF, maximo 5 paginas) com arquitetura e fluxo fim-a-fim.
- [ ] Video demonstrativo (ate 5 minutos) com toda a integracao.
- [ ] Prints/evidencias de deploy, build e validacao funcional anexados.

## 4) Qualidade minima para avaliacao

- [ ] `pytest backend/tests agents/tests -q` com sucesso.
- [ ] `npm run build` em `apps/web` com sucesso.
- [ ] `npx expo-doctor` em `apps/mobile` sem erros criticos.
- [ ] Disclaimer academico visivel (sem diagnostico clinico real).

## Fora de escopo desta submissao

- IR ALÉM 1 - Mineracao de processos e conformidade clinica.
- IR ALÉM 2 - Recuperacao de casos com embeddings visuais.

