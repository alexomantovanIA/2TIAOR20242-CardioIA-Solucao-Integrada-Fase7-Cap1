# Modelagem de Intents e Entities - CardioIA

## 1. Visao Geral do Modelo NLP

O modelo de linguagem natural do CardioIA foi projetado para reconhecer intencoes conversacionais e extrair entidades relevantes no dominio de saude cardiovascular educacional. A modelagem segue as melhores praticas do IBM Watson Assistant, com foco em cobertura de vocabulario leigo e tecnico em portugues brasileiro.

**Resumo quantitativo do modelo:**

| Componente        | Quantidade | Detalhes                                      |
|-------------------|------------|-----------------------------------------------|
| Intents           | 16         | 10 exemplos cada = 160 exemplos de treino     |
| Entities          | 4          | 23 valores com ~85 sinonimos                  |
| Dialog Nodes      | 18         | Incluindo welcome, fallback e limite          |
| Regras de urgencia| 20+2       | 20 palavras-chave + 2 regras combinatorias    |

---

## 2. Intents (Intencoes)

Cada intent possui exatamente **10 exemplos de treino**, conforme recomendacao minima do Watson para classificacao confiavel. Os exemplos foram escritos em linguagem coloquial brasileira, sem acentos, para maximizar correspondencia com entrada de usuarios reais.

### 2.1 Intencoes de Navegacao

Controlam o ciclo de vida da conversa (abertura e encerramento).

#### `#saudacao`
- **Descricao:** O usuario cumprimenta ou inicia a conversa.
- **Funcao no fluxo:** Dispara a mensagem de boas-vindas com apresentacao do escopo educacional.
- **Exemplos de treino:**

| # | Exemplo                              |
|---|--------------------------------------|
| 1 | Oi                                   |
| 2 | Ola                                  |
| 3 | Bom dia                              |
| 4 | Boa tarde                            |
| 5 | Boa noite                            |
| 6 | Oi tudo bem                          |
| 7 | Ola, preciso de ajuda                |
| 8 | Hey                                  |
| 9 | Oi, como funciona o assistente?      |
|10 | Bom dia, quero tirar uma duvida      |

#### `#despedida`
- **Descricao:** O usuario encerra a conversa ou agradece.
- **Funcao no fluxo:** Dispara mensagem de encerramento com reforco do carater educacional.
- **Exemplos de treino:**

| # | Exemplo                              |
|---|--------------------------------------|
| 1 | Tchau                                |
| 2 | Adeus                                |
| 3 | Ate logo                             |
| 4 | Obrigado                             |
| 5 | Obrigada                             |
| 6 | Valeu                                |
| 7 | Era isso, obrigado                   |
| 8 | Encerrar conversa                    |
| 9 | Pode encerrar                        |
|10 | Muito obrigado pela ajuda            |

---

### 2.2 Intencoes de Sintomas

Capturam relatos de sintomas cardiovasculares. Sao o nucleo do assistente educacional.

#### `#informar_dor_peito`
- **Descricao:** Dor ou desconforto na regiao toracica.
- **Funcao no fluxo:** Fornece orientacao educativa sobre dor toracica, quando procurar ajuda.
- **Palavras-chave relacionadas:** dor, peito, aperto, pontada, pressao, torax, queimacao.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | Estou com dor no peito                              |
| 2 | Sinto um aperto no peito                            |
| 3 | Tenho uma pontada no peito                          |
| 4 | Dor toracica ha 2 horas                             |
| 5 | Pressao no peito ao caminhar                        |
| 6 | Desconforto no peito quando faco esforco             |
| 7 | Dor no torax do lado esquerdo                       |
| 8 | Sinto dor no peito quando respiro fundo             |
| 9 | Tenho sentido aperto no peito ha 3 dias             |
|10 | Queimacao no peito apos refeicao                    |

#### `#informar_palpitacao`
- **Descricao:** Palpitacoes, batimentos irregulares ou acelerados.
- **Funcao no fluxo:** Orientacao sobre quando palpitacoes sao preocupantes, gatilhos comuns.
- **Palavras-chave relacionadas:** palpitacao, coracao, acelerado, disparado, batimentos, taquicardia.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | Estou com palpitacoes                               |
| 2 | Meu coracao esta acelerado                          |
| 3 | Sinto o coracao disparado                           |
| 4 | Batimentos irregulares ha 2 dias                    |
| 5 | Taquicardia frequente                               |
| 6 | Palpitacao leve ha uma semana                       |
| 7 | Sinto o coracao batendo muito rapido                |
| 8 | Meu coracao as vezes pula batidas                   |
| 9 | Coracao acelerado sem motivo                        |
|10 | Sinto batimentos fortes no peito                    |

#### `#informar_falta_ar`
- **Descricao:** Dificuldade respiratoria, dispneia ou cansaco excessivo.
- **Funcao no fluxo:** Diferencia causas pulmonares e cardiovasculares em nivel educativo.
- **Palavras-chave relacionadas:** falta de ar, respirar, cansaco, fadiga, dispneia, ofegante.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | Estou com falta de ar                               |
| 2 | Dificuldade para respirar                           |
| 3 | Cansaco ao subir escadas                            |
| 4 | Falta de folego ao caminhar                         |
| 5 | Dispneia ao fazer esforco                           |
| 6 | Fadiga constante                                    |
| 7 | Nao consigo respirar direito                        |
| 8 | Fico ofegante rapidamente                           |
| 9 | Cansaco excessivo ao me esforcar                    |
|10 | Falta de ar quando deito                            |

#### `#informar_tontura`
- **Descricao:** Tontura, vertigem, sensacao de desmaio ou sincope.
- **Funcao no fluxo:** Alerta sobre causas cardiovasculares de tontura (arritmia, hipotensao).
- **Palavras-chave relacionadas:** tontura, vertigem, desmaio, sincope, cabeca leve.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | Estou com tontura                                   |
| 2 | Sinto vertigem                                      |
| 3 | Quase desmaiei                                      |
| 4 | Sensacao de cabeca leve                             |
| 5 | Tontura ao levantar rapido                          |
| 6 | Desmaio ontem                                       |
| 7 | Sincope durante exercicio                           |
| 8 | Tenho sentido tonturas frequentes                   |
| 9 | Tudo roda quando levanto                            |
|10 | Sensacao de que vou desmaiar                        |

#### `#informar_pressao`
- **Descricao:** Pressao arterial elevada ou baixa.
- **Funcao no fluxo:** Informacao educativa sobre valores de referencia e importancia do monitoramento.
- **Palavras-chave relacionadas:** pressao, hipertensao, hipotensao, arterial, mmHg.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | Minha pressao esta alta                             |
| 2 | Tenho hipertensao                                   |
| 3 | Pressao arterial 18 por 10                          |
| 4 | Pressao baixa                                       |
| 5 | Hipotensao frequente                                |
| 6 | Minha pressao subiu muito                           |
| 7 | Pressao descontrolada                               |
| 8 | Nao consigo controlar a pressao                     |
| 9 | Pressao arterial elevada                            |
|10 | Tomo remedio para pressao e continua alta           |

#### `#informar_inchaco`
- **Descricao:** Inchaco nas pernas, tornozelos ou pes (edema).
- **Funcao no fluxo:** Orientacao sobre edema como possivel sinal cardiovascular (insuficiencia cardiaca).
- **Palavras-chave relacionadas:** inchaco, edema, inchada, pernas pesadas, retencao de liquido, tornozelos.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | Minhas pernas estao inchadas                        |
| 2 | Inchaco nos tornozelos                              |
| 3 | Meus pes estao muito inchados                       |
| 4 | Edema nas pernas                                    |
| 5 | Faz uma semana que meus tornozelos estao inchando no final do dia |
| 6 | Minhas pernas estao retendo liquido e ficam enormes a noite |
| 7 | Quando aperto a canela fica a marca do dedo, ta muito inchado |
| 8 | Meus pes incham tanto que nao consigo calcar sapato a tarde |
| 9 | Sinto as pernas pesadas e inchadas, sera que e do coracao? |
|10 | Notei um inchaco nos pes que nao tinha antes, estou preocupado |

---

#### `#informar_sintoma_geral`
- **Descricao:** Relato generico de mal-estar sem sintoma especifico.
- **Funcao no fluxo:** Solicita detalhamento para classificacao mais precisa.
- **Palavras-chave relacionadas:** desconforto, mal-estar, nao me sinto bem, estranho, dor generica.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | Estou sentindo um desconforto                       |
| 2 | Nao estou me sentindo bem                           |
| 3 | Tenho um mal estar                                  |
| 4 | Sinto dor                                           |
| 5 | Estou com um incomodo                               |
| 6 | Nao me sinto bem ha dias                            |
| 7 | Tenho sentido algo estranho                         |
| 8 | Meu corpo esta estranho                             |
| 9 | Estou com um sintoma preocupante                    |
|10 | Me sinto mal                                        |

---

### 2.3 Intencoes de Exames

Capturam duvidas sobre procedimentos cardiologicos. Permitem ao assistente fornecer explicacoes educativas sobre cada tipo de exame.

#### `#perguntar_ecg`
- **Descricao:** Duvida sobre eletrocardiograma (ECG).
- **Exemplos incluem:** "O que e um ECG?", "Para que serve o eletrocardiograma?", "O ECG doi?", "O que o ECG detecta?"

#### `#perguntar_ecocardiograma`
- **Descricao:** Duvida sobre ecocardiograma ou eco doppler.
- **Exemplos incluem:** "O que e ecocardiograma?", "Para que serve?", "Qual a diferenca entre ECG e ecocardiograma?"

#### `#perguntar_holter`
- **Descricao:** Duvida sobre monitoramento Holter 24h.
- **Exemplos incluem:** "O que e o Holter?", "Posso dormir com o Holter?", "Holter detecta arritmia?"

#### `#perguntar_teste_ergometrico`
- **Descricao:** Duvida sobre teste ergometrico (teste de esforco).
- **Exemplos incluem:** "O que e teste ergometrico?", "O teste ergometrico e perigoso?", "Preciso de preparo?"

#### `#perguntar_cateterismo`
- **Descricao:** Duvida sobre cateterismo cardiaco / angiografia.
- **Exemplos incluem:** "O que e cateterismo?", "Cateterismo e perigoso?", "Riscos do cateterismo cardiaco"

#### `#perguntar_exame`
- **Descricao:** Pergunta generica sobre exames cardiovasculares.
- **Exemplos incluem:** "Quais exames do coracao existem?", "Me fala sobre exames cardiacos", "Quais exames o cardiologista pede?"

Cada intent de exame possui 10 exemplos de treino no arquivo `cardioia_assistant_export.json`.

---

### 2.4 Intent de Limite

#### `#solicitar_diagnostico`
- **Descricao:** O usuario pede diagnostico, confirmacao de doenca ou prescricao.
- **Funcao no fluxo:** Ativa resposta de limite etico - reforca que o assistente NAO diagnostica.
- **Importancia:** Esta intent e critica para a governanca do sistema, garantindo que o assistente jamais ultrapasse sua funcao educacional.
- **Exemplos de treino:**

| # | Exemplo                                            |
|---|-----------------------------------------------------|
| 1 | O que eu tenho?                                     |
| 2 | Qual e meu diagnostico?                             |
| 3 | Voce pode me diagnosticar?                          |
| 4 | Qual minha doenca?                                  |
| 5 | Me diz o que eu tenho                               |
| 6 | Sera que tenho problema no coracao?                 |
| 7 | Acho que estou com infarto, confirma?               |
| 8 | Diagnostica meu problema                            |
| 9 | Tenho alguma doenca cardiaca?                       |
|10 | Meus sintomas indicam o que?                        |

---

## 3. Entities (Entidades)

As entidades sao informacoes estruturadas extraidas da mensagem do usuario. O CardioIA utiliza 4 entidades com reconhecimento por sinonimos.

### 3.1 @sintoma

Classifica o tipo de sintoma cardiovascular relatado.

| Valor              | Sinonimos                                                         | Qtd |
|--------------------|-------------------------------------------------------------------|-----|
| `dor_peito`        | dor no peito, dor toracica, aperto no peito, pontada no peito, pressao no peito | 5 |
| `palpitacao`       | palpitacao, coracao acelerado, taquicardia, batimento rapido, coracao disparado  | 5 |
| `falta_ar`         | falta de ar, dispneia, dificuldade para respirar, cansaco, fadiga              | 5 |
| `tontura`          | tontura, vertigem, desmaio, sincope, cabeca leve                               | 5 |
| `pressao_alterada` | pressao alta, hipertensao, pressao baixa, hipotensao, pressao descontrolada | 5 |
| `inchaco`          | inchaco, edema, pernas inchadas, pes inchados, tornozelos inchados, retencao de liquido | 6 |
| `nausea`           | nausea, enjoo, vontade de vomitar                                              | 3 |
| `suor_frio`        | suor frio, sudorese, suando frio                                               | 3 |

**Total:** 8 valores, 37 sinonimos.

### 3.2 @duracao

Captura o periodo de tempo que o sintoma persiste. Fundamental para a contextualizacao educativa.

| Valor     | Sinonimos                                           | Qtd |
|-----------|-----------------------------------------------------|-----|
| `minutos` | minutos, poucos minutos, alguns minutos             | 3   |
| `horas`   | horas, algumas horas, ha horas                      | 3   |
| `dias`    | dias, ha dias, alguns dias, ha 2 dias, ha 3 dias    | 5   |
| `semanas` | semanas, ha semanas, uma semana, ha 2 semanas       | 4   |
| `meses`   | meses, ha meses, alguns meses, ha 1 mes             | 4   |

**Total:** 5 valores, 19 sinonimos.

### 3.3 @intensidade

Classifica o grau de intensidade do sintoma relatado.

| Valor      | Sinonimos                                          | Qtd |
|------------|-----------------------------------------------------|-----|
| `leve`     | leve, fraco, fraca, suave, sutil                    | 5   |
| `moderada` | moderada, moderado, medio, media                    | 4   |
| `intensa`  | intensa, intenso, forte, severa, severo, aguda, agudo | 7 |

**Total:** 3 valores, 16 sinonimos.

### 3.4 @exame

Identifica exames cardiovasculares mencionados pelo usuario.

| Valor               | Sinonimos                                       | Qtd |
|---------------------|-------------------------------------------------|-----|
| `ecg`               | ECG, eletrocardiograma, eletro                  | 3   |
| `ecocardiograma`    | ecocardiograma, eco, eco doppler                | 3   |
| `holter`            | holter, holter 24h, holter 24 horas             | 3   |
| `teste_ergometrico` | teste ergometrico, teste de esforco, esteira    | 3   |
| `cateterismo`       | cateterismo, cateterismo cardiaco, angiografia   | 3   |

**Total:** 5 valores, 15 sinonimos (inclui o valor principal como match direto).

---

## 4. Regras de Seguranca (Pre-Watson)

As regras de seguranca operam **antes** da classificacao de intents, como uma camada de protecao que garante resposta imediata em cenarios potencialmente criticos. Sao implementadas no backend (`backend/utils/safety_rules.py`) e nao dependem da disponibilidade do Watson.

### 4.1 Palavras-chave individuais (20 termos)

Se **qualquer uma** dessas palavras-chave for detectada na mensagem (apos normalizacao de acentos), o sistema sobrescreve a resposta com alerta de urgencia:

| # | Palavra-chave                  | Categoria               |
|---|-------------------------------|-------------------------|
| 1 | dor intensa no peito          | Dor toracica severa     |
| 2 | dor forte no peito            | Dor toracica severa     |
| 3 | aperto forte no peito         | Dor toracica severa     |
| 4 | pressao forte no peito        | Dor toracica severa     |
| 5 | falta de ar intensa           | Dispneia severa         |
| 6 | falta de ar forte             | Dispneia severa         |
| 7 | nao consigo respirar          | Dispneia severa         |
| 8 | desmaio                       | Sincope                 |
| 9 | desmaiei                      | Sincope                 |
|10 | perda de consciencia          | Sincope                 |
|11 | perdi a consciencia           | Sincope                 |
|12 | infarto                       | Evento cardiovascular   |
|13 | avc                           | Evento cerebrovascular  |
|14 | parada cardiaca               | Emergencia              |
|15 | parada cardiaca (com acento)  | Emergencia              |
|16 | suor frio                     | Sinal de alerta         |
|17 | dor irradiando para o braco   | Dor referida            |
|18 | dor no braco esquerdo         | Dor referida            |
|19 | formigamento no braco         | Dor referida            |
|20 | convulsao                     | Emergencia neurologica  |

### 4.2 Regras combinatorias (2 regras)

Se **ambos os grupos** forem detectados simultaneamente na mensagem:

**Regra 1 - Dor toracica com sinais associados:**
- Grupo A: `dor no peito`, `dor toracica`, `aperto no peito`
- Grupo B: `falta de ar`, `suor`, `nausea`, `braco`
- Logica: Se pelo menos 1 termo do Grupo A **E** pelo menos 1 termo do Grupo B estiverem presentes.

**Regra 2 - Tontura com sincope:**
- Grupo A: `tontura`, `vertigem`
- Grupo B: `desmaio`, `perda de consciencia`
- Logica: Se pelo menos 1 termo do Grupo A **E** pelo menos 1 termo do Grupo B estiverem presentes.

### 4.3 Normalizacao de acentos

O sistema normaliza todos os acentos antes de verificar urgencia, garantindo correspondencia mesmo quando o usuario digita com ou sem acentuacao:

```
a, a, a, a  ->  a
e, e        ->  e
i           ->  i
o, o, o     ->  o
u, u        ->  u
c           ->  c
```

Exemplo: "dor no braco" e "dor no braco" ambos correspondem a "dor no braco esquerdo".

### 4.4 Resposta de urgencia padrao

Quando uma regra de seguranca e ativada, a seguinte resposta e retornada com `source: "safety_override"`:

> ATENCAO: Os sintomas que voce relatou podem indicar uma situacao de urgencia cardiovascular. Procure atendimento medico imediatamente ou ligue para o SAMU (192). Este assistente nao substitui avaliacao profissional e nao pode confirmar diagnosticos. Em caso de dor intensa no peito, falta de ar ou desmaio, nao aguarde: busque ajuda agora.

---

## 5. Dialog Nodes (Nos de Dialogo)

O Watson Assistant utiliza 18 nos de dialogo para processar as respostas. A tabela abaixo descreve cada no, sua condicao de ativacao e o tipo de resposta gerada.

| # | Node ID                    | Titulo                     | Condicao                   | Tipo de Resposta              |
|---|---------------------------|----------------------------|----------------------------|-------------------------------|
| 1 | node_welcome              | Boas-vindas                | `welcome`                  | Apresentacao + escopo         |
| 2 | node_saudacao             | Saudacao                   | `#saudacao`                | Apresentacao + escopo         |
| 3 | node_despedida            | Despedida                  | `#despedida`               | Encerramento + disclaimer     |
| 4 | node_dor_peito            | Dor no peito               | `#informar_dor_peito`      | Orientacao educacional        |
| 5 | node_palpitacao           | Palpitacao                 | `#informar_palpitacao`     | Orientacao educacional        |
| 6 | node_falta_ar             | Falta de ar                | `#informar_falta_ar`       | Orientacao educacional        |
| 7 | node_tontura              | Tontura                    | `#informar_tontura`        | Orientacao educacional        |
| 8 | node_pressao              | Pressao arterial           | `#informar_pressao`        | Orientacao educacional        |
| 9 | node_inchaco              | Inchaco e edema            | `#informar_inchaco`        | Orientacao educacional        |
|10 | node_ecg                  | ECG                        | `#perguntar_ecg`           | Explicacao de exame           |
|11 | node_ecocardiograma       | Ecocardiograma             | `#perguntar_ecocardiograma`| Explicacao de exame           |
|12 | node_holter               | Holter                     | `#perguntar_holter`        | Explicacao de exame           |
|13 | node_teste_ergometrico    | Teste Ergometrico          | `#perguntar_teste_ergometrico` | Explicacao de exame       |
|14 | node_cateterismo          | Cateterismo                | `#perguntar_cateterismo`   | Explicacao de exame           |
|15 | node_exame_geral          | Exames gerais              | `#perguntar_exame`         | Lista de exames disponiveis   |
|16 | node_solicitar_diagnostico| Limite - Diagnostico       | `#solicitar_diagnostico`   | Recusa etica + orientacao     |
|17 | node_sintoma_geral        | Sintoma generico           | `#informar_sintoma_geral`  | Solicitacao de detalhamento   |
|18 | node_fallback             | Fallback                   | `anything_else`            | Redirecionamento para escopo  |

---

## 6. Metricas de Desempenho

### 6.1 Cobertura do modelo

| Metrica                              | Valor                |
|--------------------------------------|----------------------|
| Total de intents                     | 16                   |
| Total de exemplos de treino          | 160 (10 por intent)  |
| Media de palavras por exemplo        | ~5.2                 |
| Total de entities                    | 4                    |
| Total de valores de entities         | 21                   |
| Total de sinonimos                   | ~85                  |
| Dialog nodes                         | 18                   |
| Palavras-chave de urgencia           | 20                   |
| Regras combinatorias                 | 2                    |

### 6.2 Resultados dos testes automatizados

O repositório evoluiu da entrega original (**30** testes apenas em `backend/tests`) para a **integração Fase 5 + 6**. Comando de referência na raiz:

```bash
pytest backend/tests agents/tests -q
```

**Resultado esperado (consolidado):** **65** testes passando — **41** em `backend/tests` e **24** em `agents/tests`.

| Suite de Testes (`backend/tests`) | Descricao |
|------------------------------------|-----------|
| `test_healthcheck.py`              | `/health`, `status`, `fase6_prediction` |
| `test_chat_endpoint.py`          | Chat, intents, disclaimer, `predictive_suggestion` |
| `test_safety_rules.py`           | Urgencia, combinacoes, acentos |
| `test_predict_risk_endpoint.py`  | `POST /api/predict-risk`, urgencia em `context_message` |
| `test_patient_from_text.py`      | Extracao de features a partir de texto |

| Suite (`agents/tests`) | Descricao |
|------------------------|-----------|
| `test_risk_predictor.py`, `test_protocol_database.py` | Tools ML e protocolos |
| `test_governance_coherence.py` | Coerencia protocolo x classificacao |
| `test_pipeline_ml_only.py` | Pipeline sem LLM |
| `test_batch_process.py` | Lote IR ALEM 2 |

**Nota:** a contagem exata pode variar ligeiramente com evolucoes futuras do repositório; o valor acima reflete a ultima consolidacao documentada no `README.md`.

### 6.3 Cenarios de validacao manual

| # | Cenario                         | Entrada                                         | Intent Esperado           | Resposta Esperada                  | Status |
|---|--------------------------------|--------------------------------------------------|---------------------------|------------------------------------|--------|
| 1 | Saudacao                       | "Oi, bom dia!"                                  | #saudacao                 | Apresentacao + escopo              | OK     |
| 2 | Sintoma especifico             | "Estou com palpitacoes leves ha 2 dias"         | #informar_palpitacao      | Orientacao sobre palpitacoes       | OK     |
| 3 | Exame                          | "O que e um ECG?"                               | #perguntar_ecg            | Explicacao do eletrocardiograma    | OK     |
| 4 | Urgencia (regra de seguranca)  | "Estou com dor intensa no peito e falta de ar"  | safety_override           | Alerta SAMU 192                    | OK     |
| 5 | Solicitacao de diagnostico     | "O que eu tenho?"                               | #solicitar_diagnostico    | Recusa etica                       | OK     |
| 6 | Fora do escopo                 | "Qual a previsao do tempo?"                     | anything_else (fallback)  | Redirecionamento                   | OK     |

---

## 7. Consideracoes de Design

### 7.1 Decisoes de modelagem

1. **10 exemplos por intent**: seguindo a recomendacao do Watson para classificacao minimamente confiavel. Mais exemplos melhoram a acuracia, mas 10 e o limiar pratico para um prototipo academico.

2. **Sem acentos nos exemplos de treino**: os exemplos foram escritos sem acentuacao para maximizar a correspondencia, dado que muitos usuarios brasileiros digitam sem acentos em interfaces de chat.

3. **Entity por sinonimos (nao por patterns)**: optou-se por reconhecimento por sinonimos ao inves de expressoes regulares por ser mais legivel, mais facil de manter e mais adequado ao vocabulario leigo.

4. **Regras de seguranca no backend (nao no Watson)**: a camada de urgencia opera antes do Watson para garantir que, mesmo em caso de falha de conexao ou classificacao incorreta pelo modelo, cenarios criticos sejam sempre tratados.

5. **Intent de limite unico**: apenas `#solicitar_diagnostico` como intent de limite, pois e o cenario mais critico de governanca. Outros limites (prescricao, confirmacao de doenca) sao tratados indiretamente pela mesma resposta.

### 7.2 Limitacoes conhecidas

- O modelo nao reconhece variacoes regionais extensas (girias especificas de cada estado).
- Nao ha reconhecimento de contexto multi-turno (cada mensagem e classificada isoladamente).
- A entity @duracao nao extrai valores numericos exatos (ex: "ha 3 dias" e classificado como "dias", nao como "3 dias").
- O fallback local usa correspondencia por palavras-chave simples, sem machine learning.

---

## 8. Arquivo de Referencia

Toda a modelagem descrita neste documento esta implementada no arquivo:

```
assistant/cardioia_assistant_export.json
```

Este arquivo pode ser importado diretamente no IBM Watson Assistant via API v1 (`update_workspace` com `append=False`) ou pela interface grafica (Dialog skill > Import skill).
