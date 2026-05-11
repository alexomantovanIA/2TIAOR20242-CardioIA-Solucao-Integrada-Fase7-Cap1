import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Activity,
  Bot,
  HeartPulse,
  History,
  Info,
  LogIn,
  LogOut,
  RefreshCw,
  Send,
  ShieldAlert,
  Thermometer,
} from "lucide-react";
import {
  acquireApiToken,
  hasMsalAccount,
  isMsalConfigured,
  loginEntraPopup,
  logoutEntra,
} from "./auth/msal";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";
const DISCLAIMER = "Sistema acadêmico. Não substitui avaliação médica.";

type ReadingStatus = "normal" | "atencao" | "critico";

type IotReading = {
  device_id: string;
  heart_rate: number;
  temperature: number;
  spo2: number;
  timestamp: string;
  status: ReadingStatus;
};

type Recommendation = {
  probability?: number;
  risk_classification?: string;
  suggested_protocols?: Array<{ nome?: string; acoes?: string[] }>;
};

type DashboardSummary = {
  latest_iot_reading: IotReading | null;
  risk_current: string | null;
  recommendation: string;
  recommendation_detail?: Recommendation | null;
  disclaimer: string;
};

type ChatMessage = {
  role: "user" | "assistant";
  text: string;
};

const tabs = [
  { id: "dashboard", label: "Dashboard", icon: Activity },
  { id: "chat", label: "Chat", icon: Bot },
  { id: "history", label: "Historico", icon: History },
  { id: "about", label: "Sobre", icon: Info },
] as const;

type TabId = (typeof tabs)[number]["id"];

function statusLabel(status?: string | null) {
  if (status === "critico") return "Crítico";
  if (status === "atencao") return "Atenção";
  return "Normal";
}

function riskTone(risk?: string | null) {
  if (risk === "alto" || risk === "critico") return "riskHigh";
  if (risk === "médio" || risk === "atencao") return "riskMedium";
  return "riskLow";
}

function formatTime(value?: string) {
  if (!value) return "Sem leitura";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

export default function App() {
  const [logged, setLogged] = useState(false);
  const [activeTab, setActiveTab] = useState<TabId>("dashboard");
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [history, setHistory] = useState<IotReading[]>([]);
  const [chatInput, setChatInput] = useState("Tenho palpitacoes leves ha dois dias.");
  const [chat, setChat] = useState<ChatMessage[]>([
    {
      role: "assistant",
      text: "Olá. Sou o CardioIA em modo acadêmico. Descreva sintomas ou acompanhe as leituras integradas.",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const callApi = useCallback(async <T,>(path: string, options?: RequestInit): Promise<T> => {
    if (!isMsalConfigured()) {
      throw new Error("Configure VITE_ENTRA_TENANT_ID, VITE_ENTRA_WEB_CLIENT_ID e VITE_ENTRA_API_SCOPE.");
    }
    const token = await acquireApiToken();
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...(options?.headers ?? {}),
      },
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || "Falha ao consultar a API CardioIA.");
    }
    return data as T;
  }, []);

  const loadSummary = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await callApi<DashboardSummary>("/api/dashboard/summary");
      setSummary(data);
      if (data.latest_iot_reading) {
        setHistory((current) => {
          const withoutDuplicate = current.filter(
            (item) => item.timestamp !== data.latest_iot_reading?.timestamp,
          );
          return [data.latest_iot_reading!, ...withoutDuplicate].slice(0, 8);
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }, [callApi]);

  useEffect(() => {
    if (isMsalConfigured() && hasMsalAccount()) {
      setLogged(true);
    }
  }, []);

  useEffect(() => {
    if (logged) {
      void loadSummary();
    }
  }, [logged, loadSummary]);

  const latest = summary?.latest_iot_reading || null;
  const protocol = summary?.recommendation_detail?.suggested_protocols?.[0];
  const riskClass = summary?.risk_current || summary?.recommendation_detail?.risk_classification || latest?.status;

  const vitals = useMemo(
    () => [
      {
        label: "Frequencia",
        value: latest ? `${latest.heart_rate} bpm` : "-- bpm",
        icon: HeartPulse,
      },
      {
        label: "Temperatura",
        value: latest ? `${latest.temperature} C` : "-- C",
        icon: Thermometer,
      },
      {
        label: "SpO2",
        value: latest ? `${latest.spo2}%` : "--%",
        icon: Activity,
      },
    ],
    [latest],
  );

  async function sendDemoReading() {
    setLoading(true);
    setError("");
    const now = new Date();
    try {
      await callApi("/api/iot/ingest", {
        method: "POST",
        body: JSON.stringify({
          device_id: "wokwi-esp32-demo",
          heart_rate: 72 + Math.round(Math.random() * 52),
          temperature: 36.4 + Number((Math.random() * 1.7).toFixed(1)),
          spo2: 93 + Math.round(Math.random() * 6),
          timestamp: now.toISOString(),
        }),
      });
      await loadSummary();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado.");
      setLoading(false);
    }
  }

  async function sendChat() {
    const message = chatInput.trim();
    if (!message) return;
    setChat((current) => [...current, { role: "user", text: message }]);
    setChatInput("");
    setLoading(true);
    setError("");
    try {
      const data = await callApi<{ reply: string; disclaimer: string }>("/api/chat", {
        method: "POST",
        body: JSON.stringify({ message }),
      });
      setChat((current) => [...current, { role: "assistant", text: data.reply }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }

  async function handleLogout() {
    setError("");
    try {
      if (isMsalConfigured()) {
        await logoutEntra();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao sair.");
    } finally {
      setLogged(false);
      setSummary(null);
      setHistory([]);
    }
  }

  if (!logged) {
    if (!isMsalConfigured()) {
      return (
        <main className="loginShell">
          <section className="loginPanel">
            <div className="brandMark">
              <HeartPulse size={32} />
            </div>
            <h1>CardioIA Fase 7</h1>
            <p>MVP integrado de monitoramento cardiovascular acadêmico.</p>
            <p>Para login real com Microsoft Entra ID, defina no arquivo de ambiente do Vite:</p>
            <ul className="loginHintList">
              <li>
                <code>VITE_ENTRA_TENANT_ID</code>
              </li>
              <li>
                <code>VITE_ENTRA_WEB_CLIENT_ID</code> (app SPA)
              </li>
              <li>
                <code>VITE_ENTRA_API_SCOPE</code> (ex.: <code>api://&lt;API_CLIENT_ID&gt;/access_as_user</code>)
              </li>
              <li>
                <code>VITE_API_BASE_URL</code>
              </li>
            </ul>
            <p className="loginHintDoc">
              Passo a passo no repositório: <code>docs/guia_entra_id_testes_publicacao_fase7.md</code>
            </p>
            <small>{DISCLAIMER}</small>
          </section>
        </main>
      );
    }

    return (
      <main className="loginShell">
        <section className="loginPanel">
          <div className="brandMark">
            <HeartPulse size={32} />
          </div>
          <h1>CardioIA Fase 7</h1>
          <p>MVP integrado de monitoramento cardiovascular acadêmico.</p>
          {error ? <div className="errorBanner loginError">{error}</div> : null}
          <button
            type="button"
            className="primaryButton"
            disabled={loading}
            onClick={() => {
              void (async () => {
                try {
                  setError("");
                  setLoading(true);
                  await loginEntraPopup();
                  setLogged(true);
                } catch (err) {
                  setError(err instanceof Error ? err.message : "Falha no login Entra ID.");
                } finally {
                  setLoading(false);
                }
              })();
            }}
          >
            <LogIn size={18} />
            Entrar com Microsoft Entra ID
          </button>
          <small>{DISCLAIMER}</small>
        </section>
      </main>
    );
  }

  return (
    <div className="appShell">
      <aside className="sidebar">
        <div className="brand">
          <HeartPulse />
          <div>
            <strong>CardioIA</strong>
            <span>FIAP Fase 7</span>
          </div>
        </div>
        <nav>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                type="button"
                className={activeTab === tab.id ? "navItem active" : "navItem"}
                onClick={() => setActiveTab(tab.id)}
                title={tab.label}
              >
                <Icon size={18} />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </aside>

      <main className="content">
        <header className="topbar">
          <div>
            <span className="eyebrow">MVP integrado</span>
            <h1>{tabs.find((tab) => tab.id === activeTab)?.label}</h1>
          </div>
          <div className="topbarActions">
            <button type="button" className="iconButton" onClick={loadSummary} disabled={loading} title="Atualizar dados">
              <RefreshCw size={18} />
            </button>
            <button type="button" className="iconButton" onClick={() => void handleLogout()} title="Sair">
              <LogOut size={18} />
            </button>
          </div>
        </header>

        {error && <div className="errorBanner">{error}</div>}

        {activeTab === "dashboard" && (
          <section className="dashboardGrid">
            <div className="summaryBand">
              {vitals.map((vital) => {
                const Icon = vital.icon;
                return (
                  <article className="metric" key={vital.label}>
                    <Icon size={22} />
                    <span>{vital.label}</span>
                    <strong>{vital.value}</strong>
                  </article>
                );
              })}
            </div>

            <section className={`riskPanel ${riskTone(riskClass)}`}>
              <div>
                <span className="eyebrow">Risco atual</span>
                <h2>{riskClass ? statusLabel(riskClass) : "Aguardando leitura"}</h2>
                <p>{summary?.recommendation || "Envie uma leitura IoT para iniciar a análise."}</p>
              </div>
              <ShieldAlert size={44} />
            </section>

            <section className="workflow">
              <h2>Fluxo integrado</h2>
              <div className="steps">
                <span>Sensor</span>
                <span>MicroPython</span>
                <span>Backend</span>
                <span>IA</span>
                <span>Web/Mobile</span>
              </div>
            </section>

            <section className="actions">
              <button type="button" className="primaryButton" onClick={sendDemoReading} disabled={loading}>
                <Activity size={18} />
                Simular leitura Wokwi
              </button>
              <p>Ultima leitura: {formatTime(latest?.timestamp)}</p>
            </section>
          </section>
        )}

        {activeTab === "chat" && (
          <section className="chatPanel">
            <div className="messages">
              {chat.map((item, index) => (
                <div className={`message ${item.role}`} key={`${item.role}-${index}`}>
                  {item.text}
                </div>
              ))}
            </div>
            <div className="composer">
              <input
                value={chatInput}
                onChange={(event) => setChatInput(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") void sendChat();
                }}
                placeholder="Digite sua mensagem"
              />
              <button type="button" className="iconButton filled" onClick={sendChat} disabled={loading} title="Enviar">
                <Send size={18} />
              </button>
            </div>
          </section>
        )}

        {activeTab === "history" && (
          <section className="historyList">
            {(history.length ? history : latest ? [latest] : []).map((item) => (
              <article className="historyItem" key={`${item.device_id}-${item.timestamp}`}>
                <div>
                  <strong>{item.device_id}</strong>
                  <span>{formatTime(item.timestamp)}</span>
                </div>
                <span>{item.heart_rate} bpm</span>
                <span>{item.temperature} C</span>
                <span>{item.spo2}%</span>
                <b className={riskTone(item.status)}>{statusLabel(item.status)}</b>
              </article>
            ))}
            {!history.length && !latest && <p>Nenhuma leitura recebida nesta sessão.</p>}
          </section>
        )}

        {activeTab === "about" && (
          <section className="about">
            <h2>CardioIA Fase 7</h2>
            <p>
              Plataforma acadêmica integrada com sensor simulado, backend Python, modelo preditivo supervisionado e
              assistente local seguro. A visão apresentada não emite diagnóstico definitivo e deve ser usada apenas para
              demonstração educacional.
            </p>
            <p>{DISCLAIMER}</p>
            <p>API configurada: {API_BASE_URL}</p>
            {protocol?.acoes?.length ? (
              <div>
                <h3>{protocol.nome}</h3>
                <ul>
                  {protocol.acoes.slice(0, 4).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null}
          </section>
        )}

        <footer>{DISCLAIMER}</footer>
      </main>
    </div>
  );
}
