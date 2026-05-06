# Fluxo Conversacional - CardioIA

## 1. Visao Geral

O CardioIA implementa um fluxo conversacional estruturado em 4 etapas, projetado para simular uma triagem inicial educacional em saude cardiovascular. O fluxo prioriza seguranca, clareza e respeito aos limites do assistente.

---

## 2. Maquina de Estados do Dialogo

```
                         +------------------+
                         |     INICIO       |
                         +--------+---------+
                                  |
                                  v
                         +--------+---------+
                    +----|    SAUDACAO       |----+
                    |    +--------+---------+    |
                    |             |               |
                    v             v               v
           +-------+----+ +------+------+ +------+-------+
           |  SINTOMA   | |   EXAME     | | DIAGNOSTICO  |
           |  (coleta)  | | (pergunta)  | |  (limite)    |
           +------+-----+ +------+------+ +------+-------+
                  |              |               |
                  v              v               v
         +--------+--------+----+----+----------+--------+
         |                CLASSIFICACAO                   |
         |                                                |
         |  +-----------+  +---------+  +-------------+  |
         |  | URGENCIA  |  | EDUCAC. |  |   LIMITE    |  |
         |  | (SAMU)    |  | (orient)|  | (sem diag.) |  |
         |  +-----------+  +---------+  +-------------+  |
         +------------------------+-----------------------+
                                  |
                                  v
                         +--------+---------+
                         |  ENCERRAMENTO    |
                         |  (despedida)     |
                         +------------------+
```

---

## 3. Detalhamento de Cada Etapa

### 3.1 Etapa 1 - Saudacao e Apresentacao

**Condicao de entrada:** mensagem inicial do usuario ou cumprimento reconhecido pelo intent `saudacao`.

**Comportamento:**
- O assistente se apresenta como ferramenta educacional.
- Informa escopo e limitacoes (nao realiza diagnostico, nao prescreve medicamentos).
- Convida o usuario a descrever sintomas, perguntar sobre exames ou tirar duvidas.

**Palavras-chave que ativam:** oi, ola, bom dia, boa tarde, boa noite, hey, hello.

**Exemplo de interacao:**
```
Usuario: Oi, bom dia!
CardioIA: Ola! Sou o CardioIA, um assistente academico de apoio educacional
          em saude cardiovascular. Voce pode me contar seu principal sintoma,
          perguntar sobre exames ou tirar duvidas gerais. Lembre-se: este
          assistente nao realiza diagnostico e nao substitui avaliacao medica.
          [Fonte: Watson Assistant]
          [Tag: Orientacao educacional]
```

---

### 3.2 Etapa 2 - Coleta de Informacoes

**Condicao de entrada:** usuario descreve sintoma, relata queixa ou faz pergunta sobre saude cardiovascular.

**Processamento:**

1. **Identificacao da intencao (intent):** O Watson Assistant (ou fallback local) classifica a mensagem em uma das 16 intencoes definidas.

2. **Extracao de entidades:** Informacoes especificas sao extraidas automaticamente:
   - `@sintoma` - tipo de sintoma (dor no peito, palpitacao, falta de ar, etc.)
   - `@duracao` - tempo de persistencia (minutos, horas, dias, semanas, meses)
   - `@intensidade` - grau do sintoma (leve, moderada, intensa)
   - `@exame` - exame mencionado (ECG, ecocardiograma, holter, etc.)

3. **Solicitacao de detalhes:** Se a mensagem e generica (intent `informar_sintoma_geral`) ou faltam entidades de duracao/intensidade, o assistente solicita mais informacoes.

**Exemplo - sintoma com detalhes:**
```
Usuario: Estou com palpitacoes leves ha 2 dias e queria uma orientacao.
Watson detecta:
  - Intent: informar_palpitacao (confianca: 89%)
  - Entities: @duracao=dias, @intensidade=leve
CardioIA: Palpitacoes podem ser percebidas como batimentos acelerados,
          irregulares ou mais fortes. Para fins educativos, vale observar:
          frequencia, duracao, gatilhos e sintomas associados.
          [Fonte: Watson Assistant]
          [Tag: Orientacao educacional]
          [Follow-up: Orientacao educacional entregue.]
```

**Exemplo - sintoma generico:**
```
Usuario: Nao estou me sentindo bem.
Watson detecta:
  - Intent: informar_sintoma_geral
  - Entities: (nenhuma extraida)
CardioIA: Obrigado por compartilhar. Para que eu possa oferecer uma orientacao
          mais precisa, poderia detalhar: qual o sintoma principal, ha quanto
          tempo ocorre, qual a intensidade e se ha outros sintomas associados?
          [Follow-up: Solicitar mais detalhes: duracao e intensidade do sintoma.]
```

---

### 3.3 Etapa 3 - Classificacao e Resposta

Apos coletar informacoes, o sistema classifica a situacao em uma de tres categorias. A verificacao de urgencia ocorre **antes** do processamento pelo Watson, com prioridade absoluta.

#### 3.3a - Alerta de Urgencia (prioridade maxima)

**Condicao:** Palavras-chave de urgencia detectadas pelo modulo `safety_rules.py`.

**Comportamento:**
- Verificacao executada ANTES do envio ao Watson.
- Resposta padrao sobrescrita por alerta.
- Orientacao para busca imediata de atendimento (SAMU 192).
- Campo `source` retorna `"safety_override"`.
- Campo `urgency_detected` retorna `true`.

**Gatilhos individuais (20 palavras-chave):**
- "dor intensa no peito", "dor forte no peito", "aperto forte no peito"
- "falta de ar intensa", "falta de ar forte", "nao consigo respirar"
- "desmaio", "desmaiei", "perda de consciencia", "perdi a consciencia"
- "infarto", "AVC", "parada cardiaca"
- "suor frio", "convulsao"
- "dor irradiando para o braco", "dor no braco esquerdo", "formigamento no braco"

**Gatilhos combinatorios (2 regras):**
- Dor toracica + (falta de ar | suor | nausea | dor no braco)
- Tontura/vertigem + (desmaio | perda de consciencia)

**Exemplo:**
```
Usuario: Estou com dor intensa no peito e falta de ar.
Safety Rules detecta: ["dor intensa no peito", "falta de ar"]
CardioIA: ATENCAO: Os sintomas que voce relatou podem indicar uma situacao
          de urgencia cardiovascular. Procure atendimento medico imediatamente
          ou ligue para o SAMU (192).
          [Fonte: Regra de seguranca]
          [Tag: Atencao imediata]
```

#### 3.3b - Orientacao Educacional (padrao)

**Condicao:** Intent reconhecido sem urgencia detectada.

**Comportamento:**
- Fornece informacao educativa contextualizada sobre o sintoma ou exame.
- Sugere observacao de sinais complementares quando aplicavel.
- Recomenda acompanhamento medico de rotina.
- Campo `source` retorna `"watson_assistant"` ou `"fallback_local"`.

**Cobertura de respostas educacionais:**
- 6 sintomas cardiovasculares (dor peito, palpitacao, falta de ar, tontura, pressao, geral)
- 6 exames (ECG, ecocardiograma, holter, teste ergometrico, cateterismo, geral)
- Total: 12 respostas educacionais contextualizadas

#### 3.3c - Limite do Assistente

**Condicao:** Intent `solicitar_diagnostico` reconhecido.

**Comportamento:**
- Recusa educada de realizar diagnostico.
- Reforco de que a funcao e estritamente educacional.
- Sugestao de consulta com cardiologista.
- Campo `follow_up` retorna `"Reforcar limite de uso educacional do assistente."`.

**Exemplo:**
```
Usuario: O que eu tenho? Me da um diagnostico.
CardioIA: Entendo sua preocupacao, mas este assistente nao tem capacidade
          de realizar diagnosticos. Minha funcao e estritamente educacional:
          posso orientar sobre sinais de alerta, explicar exames e sugerir
          que voce procure acompanhamento medico adequado.
          [Fonte: Watson Assistant]
          [Tag: Limite do assistente]
```

---

### 3.4 Etapa 4 - Encerramento

**Condicao de entrada:** Intent `despedida` reconhecido.

**Comportamento:**
- Agradece a interacao.
- Reforca que todas as orientacoes sao educacionais.
- Sugere consulta profissional para decisoes clinicas.

**Exemplo:**
```
Usuario: Obrigado, era isso. Tchau!
CardioIA: Obrigado por utilizar o CardioIA. Lembre-se: qualquer orientacao
          aqui e educacional. Para decisoes clinicas, consulte sempre um
          profissional de saude. Ate mais!
          [Tag: Orientacao educacional]
```

---

## 4. Tratamento de Excecoes

| Situacao | Deteccao | Comportamento | Codigo HTTP |
|----------|----------|---------------|-------------|
| Mensagem vazia | `validate_message()` | Retorna erro com orientacao | 400 |
| Mensagem < 2 caracteres | `validate_message()` | Retorna erro com limite minimo | 400 |
| Mensagem > 1000 caracteres | `validate_message()` | Retorna erro com limite maximo | 400 |
| Corpo da requisicao ausente | `chat_routes.py` | Retorna erro: campo obrigatorio | 400 |
| Intent nao reconhecido | Watson / Fallback | Resposta de fallback com sugestoes | 200 |
| Watson indisponivel | `watson_service.py` | Ativa modo fallback local automaticamente | 200 |
| Sessao Watson expirada | `_get_session()` | Cria nova sessao automaticamente | 200 |
| Tags HTML na mensagem | `sanitize_message()` | Remove tags antes de processar | 200 |

---

## 5. Logica de Follow-up

O campo `follow_up` na resposta orienta o proximo passo sugerido:

| Condicao | Valor de follow_up |
|----------|-------------------|
| Urgencia detectada | "Procure atendimento medico imediatamente." |
| Diagnostico solicitado | "Reforcar limite de uso educacional do assistente." |
| Despedida | "Conversa encerrada pelo usuario." |
| Saudacao ou fallback | "Aguardando descricao de sintoma ou duvida." |
| Sintoma sem duracao/intensidade | "Solicitar mais detalhes: duracao e intensidade do sintoma." |
| Orientacao completa | "Orientacao educacional entregue." |
