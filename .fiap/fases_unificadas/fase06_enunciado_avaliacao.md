# Fase 06 - Enunciado e Avaliação

## Enunciado

### Introdução
ATIVIDADE – FASE 6: Coração Sob Controle: Previsão de Crises com IA

### Enunciado de Atividade:

Estamos chegando na reta final da evolução da CardioIA, e após consolidarmos a etapa de interação conversacional, a Fase 6 marca uma mudança estratégica no projeto: passamos da comunicação inteligente para a inteligência preditiva orientada a risco.

Nesta etapa, o sistema deixa de atuar apenas de forma reativa e passa a operar de maneira analítica, identificando padrões em dados clínicos simulados e transformando essas informações em suporte estruturado à decisão.

A proposta desta fase é explorar como modelos de Machine Learning podem ser integrados a arquiteturas baseadas em agentes especializados, permitindo que diferentes componentes do sistema colaborem entre si para interpretar cenários e organizar respostas estratégicas. Mais do que prever um evento isolado, buscamos compreender como probabilidades, protocolos e regras operacionais podem ser articulados dentro de uma lógica sistêmica, uma verdadeira orquestração de agentes.

Assim, o desafio consiste em desenvolver um Sistema Preditivo Multiagente para Eventos Cardíacos, utilizando exclusivamente técnicas, arquiteturas e exemplos trabalhados nas disciplinas desta fase ou de fases anteriores, respeitando o material apresentado nas disciplinas.

### Objetivo geral dessa atividade:

Desenvolver um sistema inteligente capaz de:

Treinar um modelo de Machine Learning para prever picos de risco cardíaco, utilizando a base sintética apresentada em aula, aplicando as etapas de preparação de dados, separação entre treino e teste e validação, conforme demonstrado nos exemplos nas disciplinas.
Integrar esse modelo a uma arquitetura multiagente, estruturando o fluxo de chamada do modelo dentro de um agente específico e garantindo que o resultado da predição possa ser compartilhado entre os demais agentes do sistema.
Utilizar agentes especializados para analisar o risco previsto e cruzar esse resultado com a base de protocolos simulada, organizando as informações de forma lógica e coerente, conforme a arquitetura vista em sala.
Gerar uma recomendação final estruturada com base na colaboração entre agentes, apresentando de forma clara a probabilidade calculada, a classificação de risco e os protocolos sugeridos, demonstrando o funcionamento completo do pipeline multiagente.
Trabalho em equipe e colaboração interdisciplinar, recomendamos o desenvolvimento do projeto em grupo de 4 a 5 integrantes, estimulando habilidades de comunicação, cooperação e divisão equilibrada de tarefas. O trabalho em equipe é considerado uma soft skill essencial para o ambiente profissional e acadêmico, e será concedido 1 ponto extra para as equipes que se organizarem dentro dessa estrutura recomendada.
Ao final desta fase, a equipe terá desenvolvido uma solução prática que demonstra como agentes conversacionais podem ser aplicados em contextos de saúde digital, respeitando boas práticas técnicas e conceituais.

Dica: para reforçar a importância da colaboração e entender as boas práticas de trabalho em equipe, recomendamos assistir ao curso da Alura “Princípios do trabalho em equipe, relações colaborativas”, disponível na plataforma da Alura: <https://www.alura.com.br/curso-online-principios-trabalho-equipe-relacao-colaborativa>.

### Atividade detalhada:

#### PARTE 1 – Modelo Preditivo de Pico de Risco

Utilizando a base sintética fornecida em aula, a equipe deverá:

Gerar ou utilizar a base de dados simulada para treinamento.
Treinar um modelo supervisionado de classificação para prever a variável pico_risco.
Avaliar o desempenho do modelo utilizando métricas vistas em aula (exemplo: acurácia, matriz de confusão).
Salvar o modelo treinado para posterior integração no sistema multiagente.

### Entregáveis:

Notebook em Google Colab contendo:
Geração da base de dados.
Treinamento do modelo.
Avaliação com métricas.
Simulação de previsão para um novo paciente, criando manualmente um novo conjunto de dados com características clínicas simuladas (exemplo: idade, frequência cardíaca, SPO2, carga do sistema, disponibilidade de recursos – podendo, se desejado, utilizar uma ferramenta de IA Generativa para auxiliar na criação desses valores simulados), aplicando o modelo treinado para gerar a probabilidade de pico de risco e apresentando o resultado obtido de forma interpretável.
Relatório técnico (máximo duas páginas) explicando as decisões do modelo, incluindo justificativa da escolha do algoritmo, interpretação das métricas obtidas, análise dos resultados da matriz de confusão e reflexão sobre possíveis limitações ou melhorias.

#### PARTE 2 – Sistema Multiagente com OpenAI Agents SDK

Com base no modelo treinado, a equipe deverá implementar um Sistema Multiagente, conforme arquitetura apresentada em aula.

O sistema deverá conter, no mínimo:

Agente Analista de Risco – responsável por consultar o modelo preditivo e gerar o score de risco.
Agente Especialista em Protocolos – responsável por consultar a base de protocolos médicos simulados.
Agente Orquestrador – responsável por coordenar o fluxo entre os agentes utilizando handoffs.
O sistema deverá:

Receber dados de um novo paciente.
Acionar o agente de risco.
Encaminhar o resultado ao agente de protocolos.
Gerar uma resposta final estruturada contendo:
Probabilidade prevista.
Classificação de risco.
Protocolos sugeridos.
Devem ser utilizados recursos como:

Handoffs entre agentes.
Uso de tools.
Histórico de mensagens.
Validação de saída.

### Entregáveis:

Código completo do sistema multiagente publicado em repositório GitHub privado. O repositório deverá estar com acesso liberado ao professor responsável, contendo README.md com instruções claras de execução, descrição das dependências, explicação da estrutura do projeto e orientações para reprodução do ambiente.
Vídeo de até 3 minutos demonstrando o fluxo completo do sistema (entrada do novo paciente → acionamento dos agentes → geração da resposta final). O vídeo deve estar publicado como "não listado" no YouTube e o link deve constar no README do repositório.
Documento PDF (máximo três páginas) contendo:
Diagrama simplificado da arquitetura do sistema multiagente.
Descrição objetiva do papel de cada agente implementado.
Explicação de como handoffs e tools foram utilizados.
Exemplo real de entrada e saída do sistema (print ou trecho de log). O PDF deverá ser enviado junto com o link do repositório.

### Critérios de Avaliação (10 pontos totais):

| Critério | Pontos |
| :--- | :--- |
| Treinamento correto do modelo preditivo | 3 |
| Avaliação com métricas adequadas | 2 |
| Implementação da arquitetura multiagente | 3 |
| Integração correta entre agentes e modelo | 1 |
| Organização e clareza do código/documentação | 1 |
| Trabalho em equipe e formação de grupos como recomendado | 1 (Extra) |

#### IR ALÉM 1 – Governança e Monitoramento de Decisões em IA

Com base nos conceitos trabalhados na disciplina de Governança de IA (GBA) nesta fase, expandir o sistema multiagente incorporando uma camada de monitoramento e rastreabilidade das decisões geradas.

A proposta é implementar um mecanismo que:

Registre as decisões tomadas pelo sistema (score previsto, classificação de risco e protocolos sugeridos).
Armazene essas decisões em estrutura organizada (exemplo: log estruturado ou arquivo JSON).
Permita a análise posterior de consistência das recomendações.
Inclua uma verificação simples de coerência (exemplo: validação se os protocolos acionados estão alinhados com as variáveis críticas do paciente).
O objetivo é introduzir uma visão de responsabilidade, rastreabilidade e auditoria do sistema inteligente, conectando o modelo preditivo e os agentes a princípios de governança e boas práticas em IA.

Entregável:

Extensão funcional implementando o mecanismo de registro e validação.
Relatório técnico (máximo duas páginas) explicando:
Como as decisões são registradas.
Como a validação é realizada.
Qual a importância da governança em sistemas de IA aplicados à saúde.
Evidência de execução (print ou trecho de log demonstrando o registro das decisões).
### Critérios de Avaliação:

Implementação correta do registro (logs estruturados e rastreáveis).
Validação de coerência funcionando e bem justificada.
Clareza na documentação do fluxo e das decisões do sistema.
Organização do código e facilidade de reprodução.
Argumentação objetiva sobre governança e responsabilidade em IA aplicada à saúde.

#### IR ALÉM 2 – Otimização e Escalabilidade do Sistema Multiagente

Com base nos conceitos trabalhados na disciplina de Arquiteturas Distribuídas e Cluster (CCCNS), expandir o sistema desenvolvido propondo uma estratégia de escalabilidade e organização modular do pipeline multiagente.

A proposta é estruturar uma simulação de múltiplas requisições simultâneas ao sistema, organizando o código de forma que os agentes possam operar de maneira desacoplada e com separação clara de responsabilidades.

O grupo deverá:

Estruturar o sistema em módulos independentes (modelo preditivo, agentes, orquestrador).
Simular múltiplos pacientes sendo processados em sequência ou lote.
Implementar um mecanismo simples de controle de execução (exemplo: fila simulada ou processamento em loop estruturado).
Documentar como o sistema poderia evoluir para um ambiente distribuído real.
O objetivo é introduzir conceitos de organização arquitetural, escalabilidade e preparação para cenários de maior carga computacional.

Entregável:

Extensão do projeto demonstrando o processamento de múltiplos casos.
Atualização do README explicando a organização modular adotada.
Relatório técnico (máximo duas páginas) apresentando:
Estrutura modular implementada.
Estratégia de simulação de múltiplas requisições.
Possíveis caminhos para evolução para arquitetura distribuída.
### Critérios de Avaliação:

Organização modular clara e coerente.
Simulação funcional de múltiplos casos.
Coerência técnica na proposta de escalabilidade.
Clareza na documentação e argumentação técnica.

### Mensagem final:

Na Fase 6, o CardioIA evolui de um sistema interativo para um sistema preditivo e estratégico. O projeto passa a incorporar modelos de Machine Learning integrados a arquiteturas multiagentes, permitindo antecipar situações críticas e apoiar decisões emergenciais.

Esta etapa consolida competências em modelagem preditiva, integração de agentes inteligentes e tomada de decisão baseada em dados, ampliando a maturidade técnica do projeto e preparando o sistema para cenários de maior complexidade e impacto real.

## Avaliação

Avaliação ainda não disponibilizada, pois esta é a fase atual.


