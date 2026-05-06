# Relatório Técnico — Parte 1: Modelo Preditivo de Pico de Risco Cardíaco

**Projeto**: CardioIA — Fase 6  
**FIAP — 2TIAOR20242**  
**Data**: 2026-04-21

---

## 1. Justificativa da Escolha do Algoritmo

O algoritmo adotado foi o **RandomForestClassifier** (Scikit-learn), configurado com
`n_estimators=100` e `random_state=42`, por apresentar bom equilíbrio entre robustez,
desempenho e interpretabilidade em dados tabulares.

**Critérios técnicos da escolha:**

- **Robustez em dados tabulares**: o modelo combina múltiplas árvores de decisão,
  reduzindo variância e mitigando overfitting, aspecto importante para datasets sintéticos
  de pequeno/médio porte.

- **Baixa sensibilidade à escala**: as variáveis clínicas utilizadas (idade, frequência cardíaca,
  SpO2, carga do sistema e disponibilidade de recursos) possuem escalas distintas, e o modelo
  não exige normalização para bom funcionamento inicial.

- **Interpretabilidade**: o algoritmo permite extrair importância das variáveis, favorecendo
  análise técnica dos fatores preditivos e rastreabilidade acadêmica.

- **Desempenho consistente com baixa complexidade de ajuste**: em problemas binários
  tabulares com volume semelhante, tende a apresentar resultados competitivos sem necessidade
  de tuning extensivo.

**Alternativas consideradas:**
- *Logistic Regression*: adequada como baseline, porém com hipótese de linearidade entre
  atributos e target.
- *GradientBoostingClassifier*: potencial de performance superior, mas com maior custo de
  ajuste e maior sensibilidade a overfitting sem validação cruzada robusta.
- *DecisionTreeClassifier*: simples e interpretável, porém mais instável e propensa a
  sobreajuste em divisões aleatórias.

---

## 2. Interpretação das Métricas Obtidas

| Métrica | Valor obtido | Interpretação |
|---------|-------------|---------------|
| Acurácia | **87,5%** | 175 de 200 amostras do conjunto de teste classificadas corretamente |
| Precisão (classe 1) | **95,0%** | Dos pacientes classificados com pico, 95,0% realmente tinham pico |
| Recall (classe 1) | **44,2%** | Dos 43 pacientes com pico real, 19 foram corretamente identificados |
| F1-Score (classe 1) | **60,3%** | Equilíbrio moderado entre precisão e recall |

**Leitura técnica no contexto de triagem:**  
Em triagem de risco cardíaco, o **recall** (sensibilidade) é a métrica de maior criticidade,
pois falsos negativos representam pacientes de risco não identificados pelo sistema.
Apesar da precisão elevada para a classe positiva, o recall de **44,2%** demonstra que o modelo,
na forma atual, ainda não atende a um patamar desejável de segurança para uso em cenários reais.

---

## 3. Análise da Matriz de Confusão

```
                    Predito: Sem Pico   Predito: Pico
Real: Sem Pico      TN = 156            FP = 1
Real: Pico          FN = 24             TP = 19
```

**Análise dos quadrantes:**

- **Verdadeiros Negativos (TN)**: pacientes sem pico corretamente classificados, reduzindo
  acionamentos desnecessários.

- **Falsos Positivos (FP)**: pacientes sem pico classificados como risco. Em triagem, esse erro
  tende a ser operacionalmente mais aceitável do que perder casos críticos.

- **Falsos Negativos (FN)**: pacientes com pico classificados como seguros. Trata-se do erro
  de maior impacto clínico; os 24 FN observados evidenciam necessidade de ajuste do modelo
  e/ou do limiar de decisão.

- **Verdadeiros Positivos (TP)**: pacientes de risco corretamente identificados, possibilitando
  acionamento tempestivo dos protocolos.

---

## 4. Limitações e Possíveis Melhorias

**Limitações identificadas:**

1. **Dataset 100% sintético**: as regras heurísticas de geração do target podem não
   refletir padrões clínicos reais de pico de risco cardíaco, limitando a generalização.

2. **Features simplificadas**: o modelo utiliza apenas 5 variáveis. Em cenário real, seria
   necessário incorporar atributos adicionais (por exemplo, sinais de ECG, biomarcadores,
   comorbidades e histórico terapêutico).

3. **Desbalanceamento de classes**: dependendo da proporção de eventos positivos, o modelo
   pode ser tendencioso para a classe majoritária.

4. **Ausência de validação cruzada**: a avaliação foi realizada com único split aleatório,
   o que pode
   introduzir variabilidade nos resultados.

**Plano de melhoria recomendado:**

- Implementar validação cruzada estratificada (5-fold) para estimativa mais robusta.
- Aplicar SMOTE ou ajuste de pesos de classe (`class_weight='balanced'`) para lidar
  com desbalanceamento.
- Ajustar o limiar de decisão com base em curva Precisão-Recall/ROC para priorizar recall.
- Explorar features derivadas (ex.: frequência cardíaca × SPO2) como indicadores compostos.
- Usar dados clínicos reais anonimizados (ex.: bases públicas como PhysioNet) para
  validação externa do modelo.
- Implementar monitoramento de drift do modelo em produção.

---

## 5. Conclusão

O entregável da Parte 1 atende aos requisitos de implementação (geração de dados, treino,
avaliação, persistência e simulação de inferência). Do ponto de vista de desempenho, os
resultados indicam um classificador funcional para fins acadêmicos, porém com limitação
relevante de sensibilidade na classe de maior criticidade clínica. Assim, recomenda-se a
evolução do modelo com foco explícito em redução de falsos negativos antes de qualquer
uso além do contexto educacional.

---

**Equipe**: Alexandre Mantovani · Edmar Souza · Ricardo Coube · Jose Andre Filho  
**Turma**: 2TIAOR20242 — FIAP
