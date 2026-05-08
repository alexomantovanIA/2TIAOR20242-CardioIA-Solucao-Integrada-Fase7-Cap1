<!--
Sync Impact Report
- Version change: 0.0.0-template -> 1.0.0
- Modified principles:
  - Placeholder PRINCIPLE_1_NAME -> I. Integração Fim-a-Fim Obrigatória
  - Placeholder PRINCIPLE_2_NAME -> II. Deploy Profissional e Entrega Reprodutível
  - Placeholder PRINCIPLE_3_NAME -> III. Segurança Clínica e Uso Acadêmico Responsável
  - Placeholder PRINCIPLE_4_NAME -> IV. Evidências de Qualidade e Validação
  - Placeholder PRINCIPLE_5_NAME -> V. Colaboração, Rastreabilidade e Documentação
- Added sections:
  - Restrições Técnicas e de Entrega da Fase 7
  - Fluxo de Execução e Quality Gates
- Removed sections:
  - Nenhuma
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (alinhado; gate constitucional já previsto)
  - ✅ .specify/templates/spec-template.md (alinhado; requisitos e critérios mensuráveis já previstos)
  - ✅ .specify/templates/tasks-template.md (alinhado; fases e checkpoints já previstos)
  - ✅ .specify/extensions/git/commands/speckit.git.commit.md (sem referência desatualizada)
  - ✅ .specify/extensions/git/commands/speckit.git.feature.md (sem referência desatualizada)
  - ✅ .specify/extensions/git/commands/speckit.git.initialize.md (sem referência desatualizada)
  - ✅ .specify/extensions/git/commands/speckit.git.remote.md (sem referência desatualizada)
  - ✅ .specify/extensions/git/commands/speckit.git.validate.md (sem referência desatualizada)
  - ✅ README.md (alinhado ao escopo de integração e entrega da Fase 7)
  - ✅ CLAUDE.md (sem conflito com esta constituição)
  - ✅ AGENTS.md (sem conflito com esta constituição)
- Follow-up TODOs:
  - Nenhum
-->
# CardioIA Fase 7 Constitution

## Core Principles

### I. Integração Fim-a-Fim Obrigatória
Toda entrega funcional MUST demonstrar o fluxo completo Sensor -> MicroPython ->
Backend Python -> APIs de IA -> Web/Mobile. Mudanças locais em um único módulo
sem validação do impacto no ecossistema integrado são consideradas incompletas.
Rationale: o objetivo da Fase 7 é consolidar um produto integrado, não módulos
isolados.

### II. Deploy Profissional e Entrega Reprodutível
A aplicação Web MUST possuir deploy público com CI/CD ativo por push em repositório
Git, e o app Mobile MUST gerar APK instalável via pipeline de build em nuvem.
Arquivos de configuração de entrega (`vercel.json`, `app.json`, `eas.json`) MUST
ser versionados e válidos. Rationale: a avaliação prioriza disponibilidade real e
capacidade de distribuição profissional.

### III. Segurança Clínica e Uso Acadêmico Responsável
Todas as interfaces e artefatos MUST explicitar caráter acadêmico do sistema e
MUST NOT apresentar inferências como diagnóstico definitivo. O sistema MUST tratar
dados de demonstração como simulados e minimizar exposição de informações sensíveis.
Rationale: o domínio de saúde exige comunicação segura e prevenção de uso indevido.

### IV. Evidências de Qualidade e Validação
Cada incremento MUST ser acompanhado de evidências verificáveis: URL funcional da
Web, instalação/execução do APK, simulação Wokwi acessível e documentação de teste
do fluxo de login e visualização de risco cardíaco. Qualquer regressão nesses
eixos bloqueia conclusão da entrega. Rationale: entregáveis da Fase 7 são avaliados
por funcionamento comprovável, não apenas por código-fonte.

### V. Colaboração, Rastreabilidade e Documentação
O trabalho MUST manter rastreabilidade entre requisito, implementação e evidência,
com README e relatório técnico claros, objetivos e atualizados. A equipe SHOULD
operar com papéis e responsabilidades explícitas para garantir divisão equilibrada
das entregas. Rationale: colaboração e clareza documental são parte dos critérios
de avaliação e da maturidade do projeto.

## Restrições Técnicas e de Entrega da Fase 7

- A solução MUST manter backend integrador em Python para conexão entre interfaces,
  modelos preditivos e componentes conversacionais.
- A lógica de sensores MUST estar portada/simulada em MicroPython com evidência em
  ambiente Wokwi público.
- A arquitetura final MUST ser documentada com o fluxo de dados ponta a ponta.
- O repositório MUST conter instruções de execução e links públicos de validação.
- Funcionalidades "IR ALÉM" MAY ser entregues como extensão e MUST NOT degradar o
  MVP obrigatório.

## Fluxo de Execução e Quality Gates

1. Planejamento de integração: definir contratos de dados entre IoT, backend e UIs.
2. Implementação incremental: evoluir backend, web, mobile e iot com checkpoints.
3. Validação técnica: executar testes locais e validar endpoints essenciais.
4. Validação operacional: comprovar deploy web, build mobile e simulação Wokwi.
5. Validação documental: atualizar README, relatório e artefatos de demonstração.

Critérios de aprovação por PR/revisão:
- MUST manter o fluxo fim-a-fim funcional.
- MUST preservar avisos de uso acadêmico e segurança clínica.
- MUST incluir evidência de execução para o escopo alterado.
- SHOULD registrar riscos e limitações quando houver impacto clínico percebido.

## Governance

Esta constituição prevalece sobre guias locais de implementação quando houver
conflito de interpretação sobre qualidade mínima de entrega.

Processo de emenda:
- Propostas MUST descrever princípio afetado, motivação, impacto em templates e
  plano de migração para trabalho em andamento.
- Toda emenda MUST atualizar o Sync Impact Report nesta própria constituição.

Política de versionamento constitucional (SemVer):
- MAJOR: remoção/redefinição incompatível de princípio ou governança.
- MINOR: adição de princípio/seção ou expansão material de regras obrigatórias.
- PATCH: esclarecimentos editoriais sem mudança de obrigação normativa.

Revisão de conformidade:
- Todo plano, especificação e conjunto de tarefas MUST declarar conformidade com
  esta constituição no respectivo gate/checklist.
- A revisão final de entrega MUST verificar links, builds e evidências exigidas.

**Version**: 1.0.0 | **Ratified**: 2026-05-08 | **Last Amended**: 2026-05-08
