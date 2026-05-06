import { StatusBar } from 'expo-status-bar';
import { useMemo, useState } from 'react';
import {
  Activity,
  Bot,
  HeartPulse,
  Home,
  Info,
  LogIn,
  MessageCircle,
  RefreshCw,
  Send,
  ShieldCheck,
  Thermometer,
} from 'lucide-react-native';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:5000';
const DISCLAIMER = 'Sistema acadêmico. Não substitui avaliação médica.';

type TabId = 'home' | 'vitals' | 'chat' | 'recommendations' | 'about';

type IotReading = {
  device_id: string;
  heart_rate: number;
  temperature: number;
  spo2: number;
  timestamp: string;
  status: 'normal' | 'atencao' | 'critico';
};

type Summary = {
  latest_iot_reading: IotReading | null;
  risk_current: string | null;
  recommendation: string;
  recommendation_detail?: {
    probability?: number;
    suggested_protocols?: Array<{ nome?: string; acoes?: string[] }>;
  } | null;
};

type ChatItem = {
  role: 'user' | 'assistant';
  text: string;
};

const tabs: Array<{ id: TabId; label: string; icon: typeof Home }> = [
  { id: 'home', label: 'Home', icon: Home },
  { id: 'vitals', label: 'Sinais', icon: Activity },
  { id: 'chat', label: 'Chat', icon: MessageCircle },
  { id: 'recommendations', label: 'Recom.', icon: ShieldCheck },
  { id: 'about', label: 'Sobre', icon: Info },
];

function statusLabel(value?: string | null) {
  if (value === 'critico' || value === 'alto') return 'Crítico';
  if (value === 'atencao' || value === 'médio') return 'Atenção';
  if (!value) return 'Aguardando';
  return 'Normal';
}

function formatTime(value?: string) {
  if (!value) return 'Sem leitura';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' });
}

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || 'Falha ao consultar a API CardioIA.');
  }
  return data as T;
}

export default function App() {
  const [logged, setLogged] = useState(false);
  const [tab, setTab] = useState<TabId>('home');
  const [summary, setSummary] = useState<Summary | null>(null);
  const [message, setMessage] = useState('Tenho palpitacoes leves ha dois dias.');
  const [chat, setChat] = useState<ChatItem[]>([
    { role: 'assistant', text: 'CardioIA em modo acadêmico. Descreva sintomas ou consulte sinais.' },
  ]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const latest = summary?.latest_iot_reading || null;
  const risk = summary?.risk_current || latest?.status || null;
  const protocol = summary?.recommendation_detail?.suggested_protocols?.[0];

  const vitals = useMemo(
    () => [
      { label: 'Frequencia', value: latest ? `${latest.heart_rate} bpm` : '-- bpm', icon: HeartPulse },
      { label: 'Temperatura', value: latest ? `${latest.temperature} C` : '-- C', icon: Thermometer },
      { label: 'SpO2', value: latest ? `${latest.spo2}%` : '--%', icon: Activity },
    ],
    [latest],
  );

  async function loadSummary() {
    setLoading(true);
    setError('');
    try {
      setSummary(await api<Summary>('/api/dashboard/summary'));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro inesperado.');
    } finally {
      setLoading(false);
    }
  }

  async function sendDemoReading() {
    setLoading(true);
    setError('');
    try {
      await api('/api/iot/ingest', {
        method: 'POST',
        body: JSON.stringify({
          device_id: 'expo-demo',
          heart_rate: 76 + Math.round(Math.random() * 46),
          temperature: 36.4 + Number((Math.random() * 1.6).toFixed(1)),
          spo2: 93 + Math.round(Math.random() * 6),
          timestamp: new Date().toISOString(),
        }),
      });
      await loadSummary();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro inesperado.');
      setLoading(false);
    }
  }

  async function sendChat() {
    const text = message.trim();
    if (!text) return;
    setChat((current) => [...current, { role: 'user', text }]);
    setMessage('');
    setLoading(true);
    setError('');
    try {
      const data = await api<{ reply: string }>('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ message: text }),
      });
      setChat((current) => [...current, { role: 'assistant', text: data.reply }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro inesperado.');
    } finally {
      setLoading(false);
    }
  }

  if (!logged) {
    return (
      <SafeAreaView style={styles.login}>
        <StatusBar style="dark" />
        <View style={styles.loginPanel}>
          <HeartPulse color="#0f766e" size={42} />
          <Text style={styles.title}>CardioIA Fase 7</Text>
          <Text style={styles.copy}>MVP mobile integrado ao backend Python e ao modelo da Fase 6.</Text>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => {
              setLogged(true);
              void loadSummary();
            }}
          >
            <LogIn color="#fff" size={18} />
            <Text style={styles.primaryText}>Entrar no demo</Text>
          </TouchableOpacity>
          <Text style={styles.disclaimer}>{DISCLAIMER}</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.shell}>
      <StatusBar style="dark" />
      <View style={styles.header}>
        <View>
          <Text style={styles.kicker}>CardioIA FIAP</Text>
          <Text style={styles.title}>{tabs.find((item) => item.id === tab)?.label}</Text>
        </View>
        <TouchableOpacity style={styles.iconButton} onPress={loadSummary} disabled={loading}>
          <RefreshCw color="#173631" size={18} />
        </TouchableOpacity>
      </View>

      {error ? <Text style={styles.error}>{error}</Text> : null}

      <ScrollView contentContainerStyle={styles.content}>
        {tab === 'home' ? (
          <>
            <View style={styles.riskCard}>
              <Text style={styles.kicker}>Risco atual</Text>
              <Text style={styles.riskText}>{statusLabel(risk)}</Text>
              <Text style={styles.copy}>{summary?.recommendation || 'Envie uma leitura IoT para iniciar.'}</Text>
            </View>
            <TouchableOpacity style={styles.primaryButton} onPress={sendDemoReading} disabled={loading}>
              <Activity color="#fff" size={18} />
              <Text style={styles.primaryText}>Simular leitura</Text>
            </TouchableOpacity>
            <Text style={styles.copy}>Ultima leitura: {formatTime(latest?.timestamp)}</Text>
          </>
        ) : null}

        {tab === 'vitals' ? (
          <View style={styles.grid}>
            {vitals.map((vital) => {
              const Icon = vital.icon;
              return (
                <View style={styles.metric} key={vital.label}>
                  <Icon color="#0f766e" size={24} />
                  <Text style={styles.metricLabel}>{vital.label}</Text>
                  <Text style={styles.metricValue}>{vital.value}</Text>
                </View>
              );
            })}
          </View>
        ) : null}

        {tab === 'chat' ? (
          <View style={styles.chatBox}>
            {chat.map((item, index) => (
              <Text
                key={`${item.role}-${index}`}
                style={[styles.bubble, item.role === 'user' ? styles.userBubble : styles.assistantBubble]}
              >
                {item.text}
              </Text>
            ))}
            <View style={styles.composer}>
              <TextInput
                style={styles.input}
                value={message}
                onChangeText={setMessage}
                placeholder="Digite sua mensagem"
              />
              <TouchableOpacity style={styles.sendButton} onPress={sendChat} disabled={loading}>
                <Send color="#fff" size={18} />
              </TouchableOpacity>
            </View>
          </View>
        ) : null}

        {tab === 'recommendations' ? (
          <View style={styles.panel}>
            <Bot color="#0f766e" size={26} />
            <Text style={styles.sectionTitle}>{protocol?.nome || 'Recomendações acadêmicas'}</Text>
            {(protocol?.acoes || ['Monitorar sinais vitais.', 'Procurar avaliação profissional em caso de piora.']).map(
              (item) => (
                <Text style={styles.listItem} key={item}>
                  • {item}
                </Text>
              ),
            )}
          </View>
        ) : null}

        {tab === 'about' ? (
          <View style={styles.panel}>
            <Text style={styles.sectionTitle}>Sobre o MVP</Text>
            <Text style={styles.copy}>
              Aplicativo Expo para demonstrar o fluxo Sensor, MicroPython, Backend Python, IA e canais Web/Mobile.
              Não apresenta diagnóstico definitivo.
            </Text>
            <Text style={styles.disclaimer}>{DISCLAIMER}</Text>
            <Text style={styles.copy}>API: {API_BASE_URL}</Text>
          </View>
        ) : null}
      </ScrollView>

      <View style={styles.tabs}>
        {tabs.map((item) => {
          const Icon = item.icon;
          const active = item.id === tab;
          return (
            <TouchableOpacity key={item.id} style={styles.tabButton} onPress={() => setTab(item.id)}>
              <Icon color={active ? '#0f766e' : '#6b7773'} size={20} />
              <Text style={[styles.tabLabel, active ? styles.tabActive : null]}>{item.label}</Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  login: {
    flex: 1,
    justifyContent: 'center',
    padding: 22,
    backgroundColor: '#edf5f2',
  },
  loginPanel: {
    gap: 14,
    padding: 24,
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  shell: {
    flex: 1,
    backgroundColor: '#f4f7f6',
  },
  header: {
    paddingHorizontal: 18,
    paddingVertical: 14,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  content: {
    gap: 14,
    padding: 18,
    paddingBottom: 110,
  },
  kicker: {
    color: '#687672',
    fontSize: 12,
    fontWeight: '700',
  },
  title: {
    color: '#16211f',
    fontSize: 26,
    fontWeight: '800',
  },
  sectionTitle: {
    color: '#16211f',
    fontSize: 20,
    fontWeight: '800',
    marginBottom: 8,
  },
  copy: {
    color: '#56615e',
    lineHeight: 21,
  },
  disclaimer: {
    color: '#6b4d09',
    lineHeight: 20,
  },
  primaryButton: {
    minHeight: 48,
    paddingHorizontal: 16,
    borderRadius: 8,
    backgroundColor: '#0f766e',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
  },
  primaryText: {
    color: '#fff',
    fontWeight: '800',
  },
  iconButton: {
    width: 44,
    height: 44,
    borderRadius: 8,
    backgroundColor: '#e4ece9',
    alignItems: 'center',
    justifyContent: 'center',
  },
  error: {
    marginHorizontal: 18,
    padding: 10,
    color: '#7f1d1d',
    backgroundColor: '#fee2e2',
    borderRadius: 8,
  },
  riskCard: {
    gap: 8,
    padding: 20,
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  riskText: {
    color: '#0f766e',
    fontSize: 36,
    fontWeight: '900',
  },
  grid: {
    gap: 12,
  },
  metric: {
    minHeight: 120,
    padding: 18,
    borderRadius: 8,
    backgroundColor: '#fff',
    justifyContent: 'center',
    gap: 8,
  },
  metricLabel: {
    color: '#56615e',
  },
  metricValue: {
    color: '#16211f',
    fontSize: 28,
    fontWeight: '900',
  },
  chatBox: {
    gap: 10,
  },
  bubble: {
    padding: 12,
    borderRadius: 8,
    lineHeight: 20,
  },
  assistantBubble: {
    alignSelf: 'flex-start',
    color: '#16211f',
    backgroundColor: '#e4ece9',
  },
  userBubble: {
    alignSelf: 'flex-end',
    color: '#fff',
    backgroundColor: '#0f766e',
  },
  composer: {
    flexDirection: 'row',
    gap: 8,
  },
  input: {
    flex: 1,
    minHeight: 46,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#ccd9d5',
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  sendButton: {
    width: 46,
    height: 46,
    borderRadius: 8,
    backgroundColor: '#0f766e',
    alignItems: 'center',
    justifyContent: 'center',
  },
  panel: {
    padding: 18,
    borderRadius: 8,
    backgroundColor: '#fff',
    gap: 8,
  },
  listItem: {
    color: '#384542',
    lineHeight: 21,
  },
  tabs: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    minHeight: 78,
    paddingTop: 8,
    paddingHorizontal: 6,
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderColor: '#dce6e2',
  },
  tabButton: {
    alignItems: 'center',
    gap: 4,
    width: 68,
  },
  tabLabel: {
    color: '#6b7773',
    fontSize: 11,
    fontWeight: '700',
  },
  tabActive: {
    color: '#0f766e',
  },
});
