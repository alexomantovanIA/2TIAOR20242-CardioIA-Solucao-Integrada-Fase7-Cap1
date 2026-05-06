# Exemplos de Conversas - CardioIA

Este documento apresenta exemplos completos de interacoes com o CardioIA, incluindo cenarios positivos, negativos e de borda. Cada exemplo inclui analise tecnica da classificacao realizada pelo sistema.

---

## Conversa 1 - Fluxo Completo com Sintoma

**Cenario:** Usuario relata palpitacoes leves, recebe orientacao e encerra.

```
Usuario: Oi, bom dia!
CardioIA: Ola! Sou o CardioIA, um assistente academico de apoio educacional
          em saude cardiovascular. Voce pode me contar seu principal sintoma,
          perguntar sobre exames ou tirar duvidas gerais. Lembre-se: este
          assistente nao realiza diagnostico e nao substitui avaliacao medica.
```

**Analise:** Intent `#saudacao` detectado. Resposta de boas-vindas com apresentacao do escopo e disclaimer.

```
Usuario: Estou com palpitacoes leves ha 2 dias e queria uma orientacao inicial.
CardioIA: Palpitacoes podem ser percebidas como batimentos acelerados,
          irregulares ou mais fortes. Para fins educativos, vale observar:
          frequencia dos episodios, duracao, gatilhos (cafeina, estresse,
          exercicio) e sintomas associados. Na maioria dos casos, palpitacoes
          isoladas e esporadicas nao indicam gravidade, mas um acompanhamento
          medico e sempre recomendado.
```

**Analise:**
- Intent: `#informar_palpitacao`
- Entities extraidas: `@intensidade=leve`, `@duracao=dias`
- Fonte: Watson Assistant (ou Fallback local)
- Regra de seguranca: nao ativada (sem palavras-chave de urgencia)

```
Usuario: Obrigado, era isso!
CardioIA: Obrigado por utilizar o CardioIA. Lembre-se: qualquer orientacao
          aqui e educacional. Para decisoes clinicas, consulte sempre um
          profissional de saude. Ate mais!
```

**Analise:** Intent `#despedida` detectado. Mensagem de encerramento com reforco educacional.

---

## Conversa 2 - Pergunta sobre Exame Especifico

**Cenario:** Usuario quer entender o que e um ECG.

```
Usuario: Quero entender o que e um ECG e quando ele costuma ser solicitado.
CardioIA: O Eletrocardiograma (ECG) e um exame que registra a atividade
          eletrica do coracao. E rapido, indolor e nao invasivo. Costuma
          ser solicitado para investigar arritmias, isquemia, infarto e
          outras alteracoes cardiacas. O exame usa eletrodos na pele do
          torax e membros para captar os sinais eletricos.
```

**Analise:**
- Intent: `#perguntar_ecg`
- Entities extraidas: `@exame=ecg`
- Resposta contem: definicao, indicacoes, descricao do procedimento

---

## Conversa 3 - Cenario de Urgencia (Regra de Seguranca)

**Cenario:** Usuario relata sintomas graves que ativam a regra de seguranca.

```
Usuario: Estou com dor intensa no peito e falta de ar.
CardioIA: ATENCAO: Os sintomas que voce relatou podem indicar uma situacao
          de urgencia cardiovascular. Procure atendimento medico imediatamente
          ou ligue para o SAMU (192). Este assistente nao substitui avaliacao
          profissional e nao pode confirmar diagnosticos. Em caso de dor
          intensa no peito, falta de ar ou desmaio, nao aguarde: busque
          ajuda agora.
```

**Analise:**
- Regra de seguranca ativada **antes** do Watson
- Palavras-chave detectadas: `dor intensa no peito`, `falta de ar` (combinacao)
- Fonte: `safety_override`
- O Watson NAO e consultado neste cenario - a resposta de urgencia sobrescreve qualquer processamento

---

## Conversa 4 - Solicitacao de Diagnostico (Limite Etico)

**Cenario:** Usuario pede diagnostico - o assistente recusa educadamente.

```
Usuario: O que eu tenho? Me da um diagnostico.
CardioIA: Entendo sua preocupacao, mas este assistente nao tem capacidade
          de realizar diagnosticos. Minha funcao e estritamente educacional:
          posso orientar sobre sinais de alerta, explicar exames e sugerir
          que voce procure acompanhamento medico adequado. Para um
          diagnostico, consulte um cardiologista.
```

**Analise:**
- Intent: `#solicitar_diagnostico`
- Resposta de limite etico aplicada
- O assistente NAO tenta diagnosticar, prescrever ou confirmar doencas

---

## Conversa 5 - Multiplas Interacoes (Tontura + Exames)

**Cenario:** Usuario relata tontura e depois pergunta sobre exames.

```
Usuario: Boa tarde, tenho sentido tontura ao levantar.
CardioIA: Tontura pode ter causas variadas, incluindo queda de pressao,
          arritmias ou desidratacao. Observe se ocorre ao levantar, durante
          esforco, ou se acompanhada de palpitacoes. Episodios de desmaio
          ou perda de consciencia exigem avaliacao medica urgente.
```

**Analise:** Intent `#informar_tontura`. Entities: `@sintoma=tontura`.

```
Usuario: Quais exames do coracao posso fazer?
CardioIA: Os principais exames cardiovasculares incluem: ECG (eletrocardiograma),
          Ecocardiograma, Holter 24h, Teste Ergometrico e Cateterismo Cardiaco.
          Cada um investiga aspectos diferentes da saude do coracao. Voce pode
          me perguntar sobre qualquer um deles para mais detalhes.
```

**Analise:** Intent `#perguntar_exame`. Resposta lista os 5 exames suportados.

```
Usuario: Me fala sobre o Holter.
CardioIA: O Holter e um exame que monitora o ritmo cardiaco continuamente
          por 24 a 72 horas. Um pequeno aparelho e conectado ao corpo com
          eletrodos e registra todos os batimentos. E indicado para
          investigar palpitacoes, arritmias e episodios intermitentes
          de sintomas.
```

**Analise:** Intent `#perguntar_holter`. Entity: `@exame=holter`.

---

## Conversa 6 - Pressao Arterial

**Cenario:** Usuario relata pressao alta.

```
Usuario: Minha pressao esta muito alta ultimamente, 18 por 10.
CardioIA: A pressao arterial e um dos principais indicadores de saude
          cardiovascular. Valores de referencia para adultos: sistolica
          ate 120 mmHg e diastolica ate 80 mmHg. Hipertensao (pressao alta)
          e um fator de risco importante para eventos cardiovasculares.
          O monitoramento regular e o acompanhamento medico sao essenciais.
```

**Analise:**
- Intent: `#informar_pressao`
- Entity: `@sintoma=pressao_alterada`
- Valores de referencia fornecidos para contexto educativo

---

## Conversa 7 - Mensagem Fora do Escopo (Fallback)

**Cenario:** Usuario pergunta algo nao relacionado a cardiologia.

```
Usuario: Qual a previsao do tempo para amanha?
CardioIA: Nao identifiquei com clareza o tema da sua mensagem. Voce pode
          me perguntar sobre sintomas cardiovasculares (dor no peito,
          palpitacoes, falta de ar, tontura), exames (ECG, ecocardiograma,
          holter) ou orientacoes gerais de saude cardiaca. Como posso ajudar?
```

**Analise:**
- Intent: `anything_else` (fallback)
- O sistema redireciona educadamente para o escopo do assistente
- Lista exemplos de topicos suportados para guiar o usuario

---

## Conversa 8 - Urgencia por Combinacao de Sintomas

**Cenario:** Nenhuma palavra-chave individual e detectada, mas a combinacao ativa a regra.

```
Usuario: Estou com dor no peito e nausea forte.
CardioIA: ATENCAO: Os sintomas que voce relatou podem indicar uma situacao
          de urgencia cardiovascular. Procure atendimento medico imediatamente
          ou ligue para o SAMU (192). Este assistente nao substitui avaliacao
          profissional e nao pode confirmar diagnosticos. Em caso de dor
          intensa no peito, falta de ar ou desmaio, nao aguarde: busque
          ajuda agora.
```

**Analise:**
- Regra combinatoria ativada: Grupo A (`dor no peito`) + Grupo B (`nausea`)
- Fonte: `safety_override`
- Mesmo sem "dor intensa" ou "dor forte", a combinacao e suficiente para alerta

---

## Conversa 9 - Sintoma Generico (Solicitacao de Detalhamento)

**Cenario:** Usuario descreve mal-estar vago.

```
Usuario: Nao estou me sentindo bem.
CardioIA: Obrigado por compartilhar. Para que eu possa oferecer uma
          orientacao educacional mais precisa, poderia detalhar: qual o
          sintoma principal, ha quanto tempo ocorre, qual a intensidade
          e se ha outros sintomas associados?
```

**Analise:**
- Intent: `#informar_sintoma_geral`
- O assistente solicita detalhamento em vez de assumir um diagnostico
- Pede 4 informacoes: sintoma principal, duracao, intensidade, sintomas associados

---

## Conversa 10 - Inchaco nas Pernas (Edema)

**Cenario:** Usuario relata inchaco nos pes e pernas -- sintoma cardiovascular relevante.

```
Usuario: Faz uma semana que meus tornozelos estao inchando no final do dia
         e minhas pernas ficam pesadas. Sera que e do coracao?
CardioIA: O inchaco (edema) nas pernas, tornozelos ou pes pode estar
          relacionado a problemas cardiovasculares como insuficiencia
          cardiaca, quando o coracao nao bombeia sangue de forma eficiente
          e ocorre acumulo de liquido. Observe se o inchaco piora ao longo
          do dia, se e acompanhado de falta de ar ou cansaco, e se ao
          pressionar a pele a marca permanece (sinal de cacifo). Esse
          sintoma merece acompanhamento medico para investigacao adequada.
```

**Analise:**
- Intent: `#informar_inchaco`
- Entity: `@sintoma=inchaco`, `@duracao=semanas`
- Resposta explica relacao edema-coracao e orienta observacao do sinal de cacifo
- Encaminha para acompanhamento medico

---

## Conversa 11 - Fluxo Preditivo Integrado (Fase 6)

**Cenario:** Usuario relata palpitacoes frequentes; o sistema oferece formulario preditivo embutido no chat e retorna avaliacao multiagente.

```
Usuario: Estou com palpitacoes frequentes ha 2 dias e me sinto cansado.
CardioIA: Palpitacoes podem ser percebidas como batimentos acelerados,
          irregulares ou mais fortes. Para fins educativos, vale observar:
          frequencia dos episodios, duracao, gatilhos e sintomas associados.
          [Fonte: Watson Assistant | Tag: Orientacao educacional]

[O chat exibe um formulario de Avaliacao de Risco embutido na propria conversa]

[Usuario preenche:]
  - Idade: 65
  - Frequencia cardiaca: 115 bpm
  - SpO2: 91%
  - Nivel de atendimento: 85%
  - Disponibilidade de recursos: 20%

[Usuario clica em "Calcular avaliacao ->"]

CardioIA: Calculando avaliacao de risco com os dados informados.
          [dots de digitacao aparecem]

CardioIA: Probabilidade de pico de risco: 95.2%
          Classificacao: ALTO
          Protocolo: PROT-003 - Emergencia Imediata
            - Acionar SAMU 192 imediatamente
            - Iniciar RCP se necessario
            - Preparar desfibrilador
          [Aviso academico simulado]
          [Fonte: Multiagentes (Fase 6)]
```

**Analise:**
- Fase 5 (chat): intent `informar_palpitacao` → orientacao educacional
- Formulario preditivo: exibido como card no proprio chat; input travado durante preenchimento
- Fase 6 (predicao): `POST /api/predict-risk` com `mode=agents` → pipeline multiagente
  - Orquestrador → Analista_de_Risco (predict_risk_tool) → Especialista_em_Protocolos (get_protocols_tool)
  - Probabilidade 95.2% → classificacao ALTO → PROT-003
- Fonte identificada com badge verde "Multiagentes (Fase 6)"
- Regra de urgencia nao ativada (dados numericos nao contem palavras-chave de emergencia)

---

## Resumo dos Cenarios Cobertos

| # | Cenario                     | Intent / Regra             | Tipo de Resposta          |
|---|----------------------------|----------------------------|---------------------------|
| 1 | Fluxo completo             | saudacao + palpitacao + despedida | Educacional + encerramento |
| 2 | Exame especifico           | perguntar_ecg              | Explicacao de exame       |
| 3 | Urgencia (keywords)        | safety_override            | Alerta SAMU 192           |
| 4 | Diagnostico (limite)       | solicitar_diagnostico      | Recusa etica              |
| 5 | Multi-turno                | tontura + exame + holter   | Educacional sequencial    |
| 6 | Pressao arterial           | informar_pressao           | Educacional + referencia  |
| 7 | Fora do escopo             | anything_else              | Redirecionamento          |
| 8 | Urgencia (combinacao)      | safety_override            | Alerta SAMU 192           |
| 9 | Sintoma generico           | informar_sintoma_geral     | Solicitacao de detalhes   |
|10 | Inchaco (edema)            | informar_inchaco           | Educacional + observacao  |
|11 | Fluxo preditivo (Fase 6)   | informar_palpitacao + formulario | Educacional + Multiagentes |
