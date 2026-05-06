import uuid
import logging

from backend.config import Config
from backend.models.message_models import ChatResponse
from backend.utils.safety_rules import check_urgency, URGENCY_RESPONSE, _normalize

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Intent / Entity definitions for the local fallback NLP engine
# ---------------------------------------------------------------------------

INTENT_KEYWORDS = {
    "saudacao": ["oi", "ola", "bom dia", "boa tarde", "boa noite", "hey", "hello", "oi tudo bem"],
    "despedida": ["tchau", "adeus", "ate logo", "obrigado", "obrigada", "valeu", "encerrar", "bye"],
    "informar_dor_peito": [
        "dor no peito", "dor toracica", "aperto no peito", "pressao no peito",
        "pontada no peito", "desconforto toracico", "dor no torax",
        "queimacao no peito", "fisgada no peito",
    ],
    "informar_palpitacao": [
        "palpitacao", "palpitacoes", "coracao acelerado", "batimento rapido",
        "taquicardia", "coracao disparado", "batimento irregular",
        "batedeira", "coracao falhando", "pula batida",
    ],
    "informar_falta_ar": [
        "falta de ar", "dispneia", "dificuldade para respirar",
        "cansaco", "fadiga", "falta de folego", "ofegante", "sufocado",
    ],
    "informar_tontura": [
        "tontura", "vertigem", "desmaio", "sincope", "cabeca leve",
        "vista escureceu", "quase apaguei",
    ],
    "informar_pressao": [
        "pressao alta", "hipertensao", "pressao baixa", "hipotensao",
        "pressao arterial", "pressao descontrolada",
    ],
    "informar_inchaco": [
        "inchaco", "inchada", "inchadas", "inchado", "inchados",
        "edema", "retencao de liquido", "pernas inchadas",
        "pes inchados", "tornozelos inchados", "pernas pesadas",
    ],
    "perguntar_ecg": ["ecg", "eletrocardiograma"],
    "perguntar_ecocardiograma": ["ecocardiograma", "eco doppler", "ultrassom do coracao"],
    "perguntar_holter": ["holter", "monitor cardiaco"],
    "perguntar_teste_ergometrico": ["teste ergometrico", "teste de esforco", "esteira"],
    "perguntar_cateterismo": ["cateterismo", "angiografia", "angioplastia"],
    "perguntar_exame": ["exame", "exames cardiovasculares", "exames do coracao", "exames cardiacos"],
    "solicitar_diagnostico": [
        "diagnostico", "o que eu tenho", "qual minha doenca",
        "qual e meu problema", "me diagnostica",
    ],
    "informar_sintoma_geral": [
        "sintoma", "sentindo", "sinto", "desconforto", "mal estar",
        "dor", "incomodo",
    ],
}

ENTITY_PATTERNS = {
    "sintoma": [
        "dor no peito", "palpitacao", "falta de ar", "tontura",
        "cansaco", "fadiga", "desmaio", "pressao alta", "pressao baixa",
        "nausea", "suor frio", "formigamento",
        "inchaco", "edema", "inchada", "inchado",
        "queimacao", "fisgada", "batedeira", "sufocado", "ofegante",
    ],
    "duracao": [
        "minutos", "horas", "dias", "semanas", "meses",
        "ha \\d+", "faz \\d+", "desde",
    ],
    "intensidade": [
        "leve", "moderada", "moderado", "intensa", "intenso",
        "forte", "fraca", "fraco",
    ],
    "exame": [
        "ecg", "eletrocardiograma", "ecocardiograma", "holter",
        "teste ergometrico", "cateterismo",
    ],
}

# ---------------------------------------------------------------------------
# Predefined responses per intent (fallback local)
# ---------------------------------------------------------------------------

INTENT_RESPONSES = {
    "saudacao": (
        "Ola! Sou o CardioIA, um assistente academico de apoio educacional em saude cardiovascular. "
        "Voce pode me contar seu principal sintoma, perguntar sobre exames ou tirar duvidas gerais. "
        "Lembre-se: este assistente nao realiza diagnostico e nao substitui avaliacao medica."
    ),
    "despedida": (
        "Obrigado por utilizar o CardioIA. Lembre-se: qualquer orientacao aqui e educacional. "
        "Para decisoes clinicas, consulte sempre um profissional de saude. Ate mais!"
    ),
    "informar_dor_peito": (
        "A dor no peito pode ter diversas causas, desde muscular ate cardiovascular. "
        "Para fins educativos, e importante observar: localizacao exata, duracao, "
        "se irradia para braco ou mandibula, e se ha sintomas associados como falta de ar ou suor frio. "
        "Se a dor for intensa ou acompanhada desses sinais, procure atendimento medico imediatamente."
    ),
    "informar_palpitacao": (
        "Palpitacoes podem ser percebidas como batimentos acelerados, irregulares ou mais fortes. "
        "Para fins educativos, vale observar: frequencia dos episodios, duracao, "
        "gatilhos (cafeina, estresse, exercicio) e sintomas associados. "
        "Na maioria dos casos, palpitacoes isoladas e esporadicas nao indicam gravidade, "
        "mas um acompanhamento medico e sempre recomendado para investigacao adequada."
    ),
    "informar_falta_ar": (
        "A falta de ar (dispneia) pode estar relacionada a causas pulmonares ou cardiovasculares. "
        "Observe se ocorre em repouso ou ao esforco, se piora ao deitar, "
        "e se ha sintomas associados como dor no peito ou inchacos. "
        "Caso a falta de ar seja intensa ou surgir subitamente, busque atendimento medico imediato."
    ),
    "informar_tontura": (
        "Tontura pode ter causas variadas, incluindo queda de pressao, arritmias ou desidratacao. "
        "Observe se ocorre ao levantar, durante esforco, ou se acompanhada de palpitacoes. "
        "Episodios de desmaio ou perda de consciencia exigem avaliacao medica urgente."
    ),
    "informar_pressao": (
        "A pressao arterial e um dos principais indicadores de saude cardiovascular. "
        "Valores de referencia para adultos: sistolica ate 120 mmHg e diastolica ate 80 mmHg. "
        "Hipertensao (pressao alta) e um fator de risco importante para eventos cardiovasculares. "
        "O monitoramento regular e o acompanhamento medico sao essenciais."
    ),
    "informar_inchaco": (
        "O inchaco (edema) nas pernas, tornozelos ou pes pode estar relacionado a problemas "
        "cardiovasculares como insuficiencia cardiaca, quando o coracao nao bombeia sangue de "
        "forma eficiente e ocorre acumulo de liquido. Observe se o inchaco piora ao longo do dia, "
        "se e acompanhado de falta de ar ou cansaco, e se ao pressionar a pele a marca permanece "
        "(sinal de cacifo). Esse sintoma merece acompanhamento medico para investigacao adequada."
    ),
    "perguntar_ecg": (
        "O Eletrocardiograma (ECG) e um exame que registra a atividade eletrica do coracao. "
        "E rapido, indolor e nao invasivo. Costuma ser solicitado para investigar arritmias, "
        "isquemia, infarto e outras alteracoes cardiacas. "
        "O exame usa eletrodos na pele do torax e membros para captar os sinais eletricos."
    ),
    "perguntar_ecocardiograma": (
        "O Ecocardiograma e um exame de ultrassom do coracao que permite avaliar "
        "a estrutura e o funcionamento das camaras e valvulas cardiacas. "
        "E indolor, nao invasivo e frequentemente solicitado para investigar sopros, "
        "insuficiencia cardiaca e doencas valvulares."
    ),
    "perguntar_holter": (
        "O Holter e um exame que monitora o ritmo cardiaco continuamente por 24 a 72 horas. "
        "Um pequeno aparelho e conectado ao corpo com eletrodos e registra todos os batimentos. "
        "E indicado para investigar palpitacoes, arritmias e episodios intermitentes de sintomas."
    ),
    "perguntar_teste_ergometrico": (
        "O Teste Ergometrico (teste de esforco) avalia o comportamento do coracao durante "
        "exercicio progressivo em esteira ou bicicleta. "
        "E utilizado para detectar isquemia, avaliar capacidade funcional e auxiliar "
        "na investigacao de dor toracica ao esforco."
    ),
    "perguntar_cateterismo": (
        "O Cateterismo Cardiaco e um procedimento invasivo no qual um cateter fino "
        "e introduzido por uma arteria ate o coracao para avaliar as arterias coronarias. "
        "E indicado quando ha forte suspeita de doenca arterial coronariana e pode incluir "
        "angioplastia para desobstrucao no mesmo procedimento."
    ),
    "perguntar_exame": (
        "Os principais exames cardiovasculares incluem: ECG (eletrocardiograma), "
        "Ecocardiograma, Holter 24h, Teste Ergometrico e Cateterismo Cardiaco. "
        "Cada um investiga aspectos diferentes da saude do coracao. "
        "Voce pode me perguntar sobre qualquer um deles para mais detalhes."
    ),
    "solicitar_diagnostico": (
        "Entendo sua preocupacao, mas este assistente nao tem capacidade de realizar diagnosticos. "
        "Minha funcao e estritamente educacional: posso orientar sobre sinais de alerta, "
        "explicar exames e sugerir que voce procure acompanhamento medico adequado. "
        "Para um diagnostico, consulte um cardiologista."
    ),
    "informar_sintoma_geral": (
        "Obrigado por compartilhar. Para que eu possa oferecer uma orientacao educacional mais precisa, "
        "poderia detalhar: qual o sintoma principal, ha quanto tempo ocorre, "
        "qual a intensidade e se ha outros sintomas associados?"
    ),
}

FALLBACK_RESPONSE = (
    "Nao identifiquei com clareza o tema da sua mensagem. "
    "Voce pode me perguntar sobre sintomas cardiovasculares (dor no peito, palpitacoes, "
    "falta de ar, tontura), exames (ECG, ecocardiograma, holter) ou "
    "orientacoes gerais de saude cardiaca. Como posso ajudar?"
)


def _detect_intents(normalized_text):
    detected = []
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in normalized_text:
                detected.append(intent)
                break
    return detected


def _detect_entities(normalized_text):
    import re as _re
    detected = []
    for entity, patterns in ENTITY_PATTERNS.items():
        for pattern in patterns:
            if _re.search(pattern, normalized_text):
                detected.append(entity)
                break
    return detected


def _choose_response(intents):
    priority = [
        "solicitar_diagnostico",
        "informar_dor_peito",
        "informar_palpitacao",
        "informar_falta_ar",
        "informar_tontura",
        "informar_pressao",
        "informar_inchaco",
        "perguntar_ecg",
        "perguntar_ecocardiograma",
        "perguntar_holter",
        "perguntar_teste_ergometrico",
        "perguntar_cateterismo",
        "perguntar_exame",
        "informar_sintoma_geral",
        "saudacao",
        "despedida",
    ]
    for intent in priority:
        if intent in intents:
            return INTENT_RESPONSES[intent], intent
    return FALLBACK_RESPONSE, "fallback"


def _follow_up_text(primary_intent, urgency, entities):
    if urgency:
        return "Procure atendimento medico imediatamente."
    if primary_intent == "solicitar_diagnostico":
        return "Reforcar limite de uso educacional do assistente."
    if primary_intent == "despedida":
        return "Conversa encerrada pelo usuario."
    if primary_intent in ("saudacao", "fallback"):
        return "Aguardando descricao de sintoma ou duvida."
    if "intensidade" not in entities and "duracao" not in entities:
        return "Solicitar mais detalhes: duracao e intensidade do sintoma."
    return "Orientacao educacional entregue."


# ---------------------------------------------------------------------------
# Watson Assistant service (real integration)
# ---------------------------------------------------------------------------

class WatsonService:
    def __init__(self):
        self._assistant = None
        self._assistant_id = None
        self._sessions = {}

        if Config.watson_configured():
            try:
                from ibm_watson import AssistantV2
                from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

                authenticator = IAMAuthenticator(Config.WATSON_API_KEY)
                self._assistant = AssistantV2(
                    version=Config.WATSON_ASSISTANT_VERSION,
                    authenticator=authenticator,
                )
                self._assistant.set_service_url(Config.WATSON_URL)
                self._assistant_id = Config.WATSON_ASSISTANT_ID

                test_session = self._assistant.create_session(
                    assistant_id=self._assistant_id,
                ).get_result()
                logger.info("Watson Assistant conectado. Session de teste: %s", test_session["session_id"])
            except Exception as exc:
                logger.warning("Falha ao conectar Watson Assistant: %s. Usando fallback local.", exc)
                self._assistant = None

    @property
    def is_connected(self):
        return self._assistant is not None

    def _get_session(self, conversation_id):
        if conversation_id and conversation_id in self._sessions:
            return self._sessions[conversation_id]

        if not self._assistant:
            return None

        try:
            response = self._assistant.create_session(
                assistant_id=self._assistant_id,
            ).get_result()
            session_id = response["session_id"]
            cid = conversation_id or str(uuid.uuid4())
            self._sessions[cid] = session_id
            return session_id
        except Exception as exc:
            logger.warning("Falha ao criar sessao Watson: %s", exc)
            return None

    def send_message(self, message, conversation_id=None):
        is_urgent, urgency_keywords = check_urgency(message)

        if is_urgent:
            cid = conversation_id or str(uuid.uuid4())
            return ChatResponse(
                reply=URGENCY_RESPONSE,
                source="safety_override",
                urgency_detected=True,
                conversation_id=cid,
                detected_intents=["emergencia"],
                detected_entities=urgency_keywords,
                follow_up="Procure atendimento medico imediatamente.",
            )

        if self.is_connected:
            return self._send_watson(message, conversation_id)

        return self._send_fallback(message, conversation_id)

    def _send_watson(self, message, conversation_id):
        session_id = self._get_session(conversation_id)
        if not session_id:
            return self._send_fallback(message, conversation_id)

        cid = conversation_id or [k for k, v in self._sessions.items() if v == session_id][0]

        try:
            response = self._assistant.message(
                assistant_id=self._assistant_id,
                session_id=session_id,
                input={"message_type": "text", "text": message},
                user_id="cardioia-user",
            ).get_result()

            output = response.get("output", {})
            generic = output.get("generic", [])
            intents = output.get("intents", [])
            entities = output.get("entities", [])

            reply_parts = [item.get("text", "") for item in generic if item.get("response_type") == "text"]

            # Watson reconheceu o intent mas seu dialog não tem resposta configurada:
            # usa o fallback local, que possui respostas educacionais para todos os intents.
            if not reply_parts:
                logger.debug("Watson sem texto de resposta; usando fallback local.")
                return self._send_fallback(message, conversation_id)

            reply = " ".join(reply_parts)
            intent_names = [i["intent"] for i in intents]
            entity_names = list({e["entity"] for e in entities})

            return ChatResponse(
                reply=reply,
                source="watson_assistant",
                urgency_detected=False,
                conversation_id=cid,
                detected_intents=intent_names,
                detected_entities=entity_names,
                follow_up=_follow_up_text(intent_names[0] if intent_names else "fallback", False, entity_names),
            )

        except Exception as exc:
            logger.warning("Erro ao enviar mensagem Watson: %s. Usando fallback.", exc)
            return self._send_fallback(message, conversation_id)

    def _send_fallback(self, message, conversation_id):
        cid = conversation_id or str(uuid.uuid4())
        normalized = _normalize(message)

        intents = _detect_intents(normalized)
        entities = _detect_entities(normalized)
        reply, primary_intent = _choose_response(intents)
        follow_up = _follow_up_text(primary_intent, False, entities)

        return ChatResponse(
            reply=reply,
            source="fallback_local",
            urgency_detected=False,
            conversation_id=cid,
            detected_intents=intents if intents else [primary_intent],
            detected_entities=entities,
            follow_up=follow_up,
        )
