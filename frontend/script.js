const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("chatForm");
const inputEl = document.getElementById("messageInput");
const sendButtonEl = document.getElementById("sendButton");
const clearButtonEl = document.getElementById("clearButton");
const statusBadgeEl = document.getElementById("statusBadge");
const statusContainer = document.getElementById("statusContainer");
const promptGridEl = document.getElementById("quickPrompts");
const journeyStepsEl = document.getElementById("journeySteps");
const infoToggle = document.getElementById("infoToggle");
const infoPanel = document.getElementById("infoPanel");
const closeInfo = document.getElementById("closeInfo");

let conversationId = window.localStorage.getItem("cardioia_conversation_id") || null;
let loadingMessageEl = null;
let lastChatUserMessage = "";
let predictiveState = { active: false, analysisCompleted: false };

// ─── Utilities ───────────────────────────────────────────────────────────────

function getTimeLabel() {
  return new Intl.DateTimeFormat("pt-BR", { hour: "2-digit", minute: "2-digit" }).format(new Date());
}

function setStatus(text, mode = "default") {
  statusBadgeEl.textContent = text;
  statusContainer.className = `status-indicator is-${mode}`;
}

function updateJourneyStage(stage) {
  const stages = ["acolhimento", "investigacao", "orientacao", "proximos-passos"];
  const idx = stages.indexOf(stage);
  document.querySelectorAll(".journey-step").forEach((el, i) => {
    el.classList.toggle("is-active", i === idx);
    el.classList.toggle("is-complete", i < idx);
  });
}

function lockChatInput() {
  inputEl.disabled = true;
  sendButtonEl.disabled = true;
  inputEl.placeholder = "Preencha o formulário acima para continuar.";
}

function unlockChatInput() {
  inputEl.disabled = false;
  sendButtonEl.disabled = false;
  inputEl.placeholder = "Escreva aqui sua dúvida ou sintoma principal.";
  inputEl.focus();
}

function setLoadingState(loading) {
  sendButtonEl.disabled = loading;
  inputEl.disabled = loading;
}

// ─── Messages ────────────────────────────────────────────────────────────────

function appendMessage(author, text, options = {}) {
  const div = document.createElement("div");
  div.className = `message ${author} ${options.alert ? "alert" : ""}`.trim();

  const tagHtml = options.tag
    ? `<span class="message-tag ${options.tagClass || "message-tag--neutral"}">${options.tag}</span>`
    : "";
  const sourceHtml = options.source
    ? `<span class="message-tag message-tag--source">${options.source}</span>`
    : "";
  const noteHtml = options.note
    ? `<p class="message__note">${options.note}</p>`
    : "";

  div.innerHTML = `
    <strong>${author === "user" ? "Você" : "CardioIA"} • ${getTimeLabel()}</strong>
    ${tagHtml}${sourceHtml}
    <div class="message__text">${text}</div>
    ${noteHtml}
  `;

  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function appendLoadingMessage() {
  loadingMessageEl = document.createElement("div");
  loadingMessageEl.className = "message assistant";
  loadingMessageEl.innerHTML = `
    <strong>CardioIA • ${getTimeLabel()}</strong>
    <div class="typing-dots" aria-label="Processando">
      <span></span><span></span><span></span>
    </div>
  `;
  messagesEl.appendChild(loadingMessageEl);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeLoadingMessage() {
  if (loadingMessageEl) { loadingMessageEl.remove(); loadingMessageEl = null; }
}

// ─── Risk Form Card ───────────────────────────────────────────────────────────

function showPredictiveFormCard(suggestion) {
  if (predictiveState.active || predictiveState.analysisCompleted) return;
  predictiveState.active = true;

  const prefilled = suggestion.extracted_fields || {};

  const wrapper = document.createElement("div");
  wrapper.className = "message assistant form-message";
  wrapper.innerHTML = buildFormCardHTML(prefilled);
  messagesEl.appendChild(wrapper);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  lockChatInput();
  updateJourneyStage("proximos-passos");

  // Slider live update
  const cargaInput = wrapper.querySelector("#rf-carga");
  const cargaVal = wrapper.querySelector("#rf-carga-val");
  cargaInput.addEventListener("input", () => { cargaVal.textContent = cargaInput.value + "%"; });

  const dispInput = wrapper.querySelector("#rf-disp");
  const dispVal = wrapper.querySelector("#rf-disp-val");
  dispInput.addEventListener("input", () => { dispVal.textContent = dispInput.value + "%"; });

  wrapper.querySelector("#rf-confirm").addEventListener("click", () => handleFormConfirm(wrapper));
  wrapper.querySelector("#rf-cancel").addEventListener("click", () => handleFormCancel(wrapper));
}

function buildFormCardHTML(prefilled) {
  const cargaDefault = prefilled.carga_sistema != null
    ? Math.round(prefilled.carga_sistema * 100) : 50;
  const dispDefault = prefilled.disponibilidade_recursos != null
    ? Math.round(prefilled.disponibilidade_recursos * 100) : 50;

  return `
    <strong>CardioIA • ${getTimeLabel()}</strong>
    <span class="message-tag message-tag--neutral">Avaliação de risco</span>
    <div class="risk-form-card">
      <p class="risk-form-card__desc">
        Preencha os dados clínicos abaixo para calcular a probabilidade de pico de risco.
      </p>
      <div class="risk-form-card__fields">

        <div class="field-row">
          <label for="rf-idade">Idade <span class="field-hint">18 – 90 anos</span></label>
          <input type="number" id="rf-idade" min="18" max="90"
            placeholder="Ex.: 45" value="${prefilled.idade ?? ""}">
        </div>

        <div class="field-row">
          <label for="rf-fc">Frequência cardíaca <span class="field-hint">bpm</span></label>
          <input type="number" id="rf-fc" min="40" max="200"
            placeholder="Ex.: 80" value="${prefilled.freq_cardiaca ?? ""}">
        </div>

        <div class="field-row">
          <label for="rf-spo2">Saturação de oxigênio <span class="field-hint">SpO2 — 80 a 100 %</span></label>
          <input type="number" id="rf-spo2" min="80" max="100"
            placeholder="Ex.: 97" value="${prefilled.spo2 ?? ""}">
        </div>

        <div class="field-row field-row--slider">
          <label for="rf-carga">
            Nível de atendimento no local
            <span class="slider-value" id="rf-carga-val">${cargaDefault}%</span>
          </label>
          <input type="range" id="rf-carga" min="0" max="100" step="1" value="${cargaDefault}">
          <div class="slider-labels"><span>Tranquilo</span><span>Muito lotado</span></div>
        </div>

        <div class="field-row field-row--slider">
          <label for="rf-disp">
            Disponibilidade de recursos médicos
            <span class="slider-value" id="rf-disp-val">${dispDefault}%</span>
          </label>
          <input type="range" id="rf-disp" min="0" max="100" step="1" value="${dispDefault}">
          <div class="slider-labels"><span>Sem recursos</span><span>Plenamente disponível</span></div>
        </div>

      </div>
      <p class="risk-form-card__error" id="rf-error" hidden></p>
      <div class="risk-form-card__actions">
        <button class="btn-secondary" id="rf-cancel">Cancelar</button>
        <button class="btn-primary" id="rf-confirm">Calcular avaliação →</button>
      </div>
    </div>
  `;
}

function handleFormConfirm(wrapper) {
  const errorEl = wrapper.querySelector("#rf-error");
  errorEl.hidden = true;

  const idade = Number(wrapper.querySelector("#rf-idade").value);
  const fc = Number(wrapper.querySelector("#rf-fc").value);
  const spo2 = Number(wrapper.querySelector("#rf-spo2").value);
  const carga = Number(wrapper.querySelector("#rf-carga").value) / 100;
  const disp = Number(wrapper.querySelector("#rf-disp").value) / 100;

  const errors = [];
  if (!idade || idade < 18 || idade > 90) errors.push("Idade deve estar entre 18 e 90 anos.");
  if (!fc || fc < 40 || fc > 200) errors.push("Frequência cardíaca deve estar entre 40 e 200 bpm.");
  if (!spo2 || spo2 < 80 || spo2 > 100) errors.push("SpO2 deve estar entre 80 e 100%.");

  if (errors.length) {
    errorEl.textContent = errors.join(" ");
    errorEl.hidden = false;
    return;
  }

  wrapper.querySelector("#rf-confirm").disabled = true;
  wrapper.querySelector("#rf-cancel").disabled = true;
  wrapper.remove();
  unlockChatInput();

  runAnalysis({ idade, freq_cardiaca: fc, spo2, carga_sistema: carga, disponibilidade_recursos: disp });
}

function handleFormCancel(wrapper) {
  wrapper.remove();
  predictiveState.active = false;
  unlockChatInput();
  appendMessage("assistant", "Formulário cancelado. Pode continuar a conversa normalmente.", {
    tag: "Avaliação de risco",
    tagClass: "message-tag--neutral",
  });
}

// ─── Predictive Analysis ──────────────────────────────────────────────────────

async function runAnalysis(patient) {
  setStatus("Calculando avaliação...", "loading");
  appendMessage("assistant", "Calculando avaliação de risco com os dados informados.", {
    tag: "Avaliação de risco",
    tagClass: "message-tag--neutral",
  });
  appendLoadingMessage();

  try {
    const payload = { ...patient, mode: "agents", context_message: lastChatUserMessage };
    const res = await fetch("/api/predict-risk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    removeLoadingMessage();

    if (data.urgency_detected) {
      appendMessage("assistant", data.urgency_message || "Atenção: sinais de urgência identificados.", {
        alert: true,
        tag: "Atenção imediata",
        tagClass: "message-tag--warning",
      });
    } else {
      const rec = data.recommendation || {};
      const lines = [];
      if (rec.probability != null) {
        lines.push(`Probabilidade de pico de risco: ${(Number(rec.probability) * 100).toFixed(1)}%`);
      }
      if (rec.risk_classification) {
        lines.push(`Classificação: ${String(rec.risk_classification).toUpperCase()}`);
      }
      (rec.suggested_protocols || []).forEach((p) => {
        lines.push(`\nProtocolo: ${p.nome || p.protocol_id}`);
        (p.acoes || []).forEach((a) => lines.push(`  • ${a}`));
      });
      if (rec.disclaimer) lines.push(`\n${rec.disclaimer}`);

      appendMessage("assistant", lines.join("\n") || "Avaliação concluída.", {
        tag: "Resultado",
        tagClass: "message-tag--neutral",
        source: data.mode === "agents" ? "Multiagentes (Fase 6)" : "Modelo preditivo",
      });
    }

    predictiveState.analysisCompleted = true;
    setStatus("Avaliação concluída", "default");
  } catch {
    removeLoadingMessage();
    appendMessage("assistant", "Não foi possível concluir a avaliação agora. Tente novamente.", {
      alert: true,
    });
    predictiveState.active = false;
    setStatus("Erro na avaliação", "warning");
  }
}

// ─── Chat ─────────────────────────────────────────────────────────────────────

async function sendMessage(message) {
  lastChatUserMessage = message;
  if (promptGridEl) promptGridEl.style.display = "none";

  setLoadingState(true);
  updateJourneyStage("investigacao");
  setStatus("Analisando seu relato...", "loading");
  appendMessage("user", message);
  appendLoadingMessage();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });

    const data = await response.json();
    removeLoadingMessage();
    setLoadingState(false);

    if (!response.ok) throw new Error(data.message);

    conversationId = data.conversation_id || conversationId;

    const sourceLabel = data.source === "watson_assistant"
      ? "Watson Assistant"
      : data.source === "safety_override"
        ? "Regra de segurança"
        : "Fallback local";

    appendMessage("assistant", data.reply, {
      alert: data.urgency_detected,
      tag: data.urgency_detected ? "Urgência" : "Orientação educacional",
      tagClass: data.urgency_detected ? "message-tag--warning" : "message-tag--neutral",
      source: sourceLabel,
      note: data.urgency_detected
        ? "Procure atendimento médico imediato."
        : "Lembrete: este assistente é educacional e não substitui avaliação médica.",
    });

    updateJourneyStage("orientacao");
    setStatus(data.urgency_detected ? "Sinal de alerta" : "Pronto", data.urgency_detected ? "warning" : "default");

    if (data.predictive_suggestion && !data.urgency_detected && !predictiveState.active && !predictiveState.analysisCompleted) {
      showPredictiveFormCard(data.predictive_suggestion);
    }
  } catch (error) {
    removeLoadingMessage();
    setLoadingState(false);
    appendMessage("assistant", "Erro de conexão. Verifique a aplicação e tente novamente.", { alert: true });
    setStatus("Erro de conexão", "warning");
  } finally {
    if (!inputEl.disabled) inputEl.focus();
  }
}

// ─── Events ───────────────────────────────────────────────────────────────────

formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  const msg = inputEl.value.trim();
  if (msg) {
    inputEl.value = "";
    inputEl.style.height = "auto";
    sendMessage(msg);
  }
});

inputEl.addEventListener("input", () => {
  inputEl.style.height = "auto";
  inputEl.style.height = inputEl.scrollHeight + "px";
});

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    formEl.dispatchEvent(new Event("submit"));
  }
});

clearButtonEl.addEventListener("click", () => {
  messagesEl.innerHTML = "";
  conversationId = null;
  predictiveState = { active: false, analysisCompleted: false };
  unlockChatInput();
  if (promptGridEl) promptGridEl.style.display = "flex";
  renderWelcome();
});

if (infoToggle) infoToggle.addEventListener("click", () => { infoPanel.hidden = false; });
if (closeInfo) closeInfo.addEventListener("click", () => { infoPanel.hidden = true; });

if (promptGridEl) {
  promptGridEl.addEventListener("click", (e) => {
    const btn = e.target.closest(".prompt-chip");
    if (btn) { inputEl.value = btn.dataset.prompt; inputEl.focus(); }
  });
}

// ─── Init ─────────────────────────────────────────────────────────────────────

function renderWelcome() {
  updateJourneyStage("acolhimento");
  appendMessage(
    "assistant",
    "Olá! Sou o CardioIA. Me conte o que está sentindo e vou orientar você da melhor forma possível.",
    { note: "Assistente educacional — não substitui avaliação médica profissional." }
  );
}

renderWelcome();
