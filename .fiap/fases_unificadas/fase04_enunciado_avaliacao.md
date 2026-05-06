# Fase 04 - Enunciado e Avaliação

## Enunciado

### Introdução
ATIVIDADE – FASE 4: Assistente Cardiológico Virtual COM VISÃO COMPUTACIONAL

### Enunciado de Atividade:

Após estruturarmos o monitoramento contínuo na fase anterior, a CardioIA avança para a análise de dados médicos com da Visão Computacional. O desafio agora é desenvolver um protótipo capaz de transformar imagens médicas simuladas em informações interpretáveis, auxiliando a tomada de decisão clínica.

Para isso, exploraremos técnicas demonstradas nas aulas, como redes neurais convolucionais (CNNs), pré-processamento e classificação de imagens, aplicadas em um contexto realista de apoio à saúde.

Nesta etapa, disciplinas como Mobile, Generative AI, Governança, além de outras, também podem contribuir para criação desse novo protótipo.

Para situar melhor a jornada, observe no mapa mental a seguir em que ponto o projeto CardioIA se encontra nesta Fase 4. A visualização ajuda a compreender como as etapas já realizadas se conectam com as próximas e como os conhecimentos acumulados sustentam esta fase do trabalho.

Para visualizar o mapa mental completo, acesse o link: mapaMental - CardioIA_ A Nova Era da Cardiologia Inteligente.svg

### Objetivo geral dessa atividade:

Construir um protótipo de Assistente Cardiológico Virtual que:

Realize o pré-processamento de imagens médicas simuladas (exemplo: ECGs, raios-X ou datasets públicos de saúde, como o <https://www.kaggle.com/datasets/nih-chest-xrays/data>).
Treine e avalie modelos de CNN para classificar e identificar padrões em imagens médicas.
Apresente os resultados de forma acessível em uma aplicação simples, como por exemplo um notebook interativo, uma interface web básica (Flask) ou um app mobile inicial, priorizando clareza e facilidade de interpretação dos resultados obtidos pelo modelo.
Trabalho em equipe e colaboração interdisciplinar — recomendamos o desenvolvimento do projeto em grupo de 2 a 5 integrantes, estimulando habilidades de comunicação, cooperação e divisão equilibrada de tarefas. O trabalho em equipe é considerado uma soft skill essencial para o ambiente profissional e acadêmico, e será concedido 1 ponto extra para as equipes que se organizarem dentro dessa estrutura recomendada.
Ao final desta fase, sua equipe terá desenvolvido uma solução prática que demonstra, de forma técnica, como técnicas de Visão Computacional podem ser aplicadas na análise de exames médicos simulados, priorizando eficiência, confiabilidade e responsabilidade no uso dos dados em saúde. Essa solução pode ser adaptada para contextos reais de pesquisa e desenvolvimento.

Dica: para reforçar a importância da colaboração e entender as boas práticas de trabalho em equipe, recomendamos assistir ao curso da Alura “Princípios do trabalho em equipe, relações colaborativas”, disponível na plataforma da Alura: <https://www.alura.com.br/curso-online-principios-trabalho-equipe-relacao-colaborativa>.

### Atividade detalhada:

#### PARTE 1 – Pré-processamento e Organização das Imagens

Selecionar um dataset público de imagens médicas.
Aplicar técnicas de pré-processamento vistas em aula:
Redimensionamento, normalização e conversão de formatos.
Criação de conjuntos de treino, validação e teste.
Documentar as etapas do pipeline de preparação.
### Entregáveis:

Notebook Python (Google Colab) com o código de pré-processamento.
Relatório curto (de uma a duas páginas) descrevendo as etapas e justificativas das escolhas.

#### PARTE 2 – Classificação de Imagens Médicas com CNN

Implementar uma rede CNN em Python para classificar as imagens pré-processadas.
Testar duas abordagens:
Treino de uma CNN simples do zero.
Uso de Transfer Learning com um modelo pré-treinado (utilizando modelos pré-treinados trabalhados em aula, como VGG16 ou ResNet, quando aplicável).
Avaliar resultados com métricas aprendidas em aula (acurácia, matriz de confusão, precisão, recall, F1-score).
Apresentar a classificação simulada em um protótipo de interface (pode ser em notebook, interface simples em Flask ou app mobile básico com apoio da disciplina Mobile).
### Entregáveis:

Notebook Python com código da CNN e resultados.
Prints das métricas de avaliação.
Protótipo de apresentação dos resultados (notebook interativo ou app simples).

### Critérios de Avaliação (10 pontos totais):

| Critério | Pontos |
| :--- | :--- |
| Pipeline de pré-processamento implementado | 3 |
| Treinamento e avaliação de CNN do zero | 2 |
| Implementação de Transfer Learning funcional | 2 |
| Apresentação dos resultados em protótipo simples | 2 |
| Documentação clara | 1 |
| Trabalho em equipe e formação de grupos como recomendado | 1 (Extra) |

#### IR ALÉM 1 – Ética e Governança em Visão Computacional

Objetivo: analisar possíveis vieses no dataset escolhido e propor práticas de mitigação.

Identificar limitações do dataset (desbalanceamento, representatividade).
Aplicar métricas de fairness e discutir implicações éticas.
### Entregáveis:

Relatório técnico (até duas páginas).
Notebook opcional com experimentos de fairness.
### Critérios de Avaliação:

Clareza na identificação de limitações do dataset.
Aplicação correta de métricas de fairness.
Qualidade e organização do relatório e código.

#### IR ALÉM 2 – Integração com Aplicativo Mobile

Objetivo: levar os resultados da classificação para um protótipo mobile em React Native, exibindo as categorias detectadas pela CNN.

Criar interface simples com tela de upload de imagem e exibição do resultado.
Integrar o backend em Flask ou Node.js com o modelo treinado.
### Entregáveis:

Repositório GitHub com o app.
Vídeo de até 3 minutos mostrando a interação.
### Critérios de Avaliação:

Interface funcional em React Native.
Integração correta com backend (Flask ou Node.js).
Exibição clara das categorias classificadas.
Organização do código e documentação.

### Mensagem final:

A Fase 4 coloca a Visão Computacional no centro do CardioIA, desafiando todos a transformar imagens médicas em informações relevantes. Essa experiência mostra como a análise automatizada pode apoiar decisões médicas, ao mesmo tempo em que convida à reflexão sobre os limites éticos e técnicos do uso de IA na saúde.

## Avaliação

Sua Nota 9
Total: 9.00

feedback do professor
Pontos positivos:

O pré-processamento foi muito bem estruturado, com redimensionamento, normalização, data augmentation adequada para exames médicos e organização correta dos splits. As etapas estão documentadas no relatório do PDF enviado, especialmente na seção sobre o pipeline de dados descrita na página 2, além das evidências visuais das imagens no arquivo pre_processamento.png.

A CNN do zero foi implementada corretamente, com arquitetura clara, checkpoints, early stopping e avaliação completa. As curvas de loss e acurácia apresentadas (baseline treino) mostram entendimento do comportamento do modelo.

O Transfer Learning com VGG16 foi aplicado de forma exemplar, com duas fases (topo e fine-tuning), exatamente como recomendado no enunciado. As duas matrizes de confusão anexadas mostram ganho consistente de desempenho.

O relatório apresenta Grad-CAMs para NORMAL e PNEUMONIA tanto na CNN do zero quanto na VGG16, reforçando a interpretabilidade do modelo de forma alinhada ao objetivo clínico da atividade.

O grupo desenvolveu também um protótipo em Flask e um notebook interativo para apresentação dos resultados, atendendo ao critério de interface simples e funcional.

A documentação do PDF é clara, detalhada, organizada e cobre todos os pontos obrigatórios da Fase 4.

O trabalho está muito acima da média em profundidade técnica e demonstra domínio de visão computacional aplicada à saúde.

Pontos de melhoria:

O relatório poderia incluir uma análise mais textual das diferenças entre as curvas de treino e validação, especialmente destacando o leve overfitting observado na CNN do zero e explicando como isso influenciou a decisão de aplicar Transfer Learning.

Considerações finais:
O seu trabalho demonstra domínio técnico, organização e atenção a todos os requisitos da Fase 4. A implementação das CNNs, o pipeline de dados e a explicabilidade com Grad-CAM ficaram excelentes, e o protótipo complementa perfeitamente a entrega. Você cumpriu todo o escopo e apresentou resultados sólidos, bem documentados e visualmente claros. Excelente desempenho.
