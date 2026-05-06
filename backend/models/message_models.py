from dataclasses import dataclass, field
from typing import List, Optional


# Aviso do chat (Fase 5 — triagem conversacional). Para predição laboratorial Fase 6,
# o texto canónico está em agents.config.DISCLAIMER (pipeline /api/predict-risk).
DISCLAIMER = (
    "Aviso: este assistente tem finalidade educacional e de triagem inicial simulada. "
    "Ele nao realiza diagnostico, nao prescreve medicamentos e nao substitui avaliacao medica."
)


@dataclass
class ChatRequest:
    message: str
    conversation_id: Optional[str] = None


@dataclass
class ChatResponse:
    reply: str
    source: str
    urgency_detected: bool = False
    disclaimer: str = DISCLAIMER
    conversation_id: str = ""
    detected_intents: List[str] = field(default_factory=list)
    detected_entities: List[str] = field(default_factory=list)
    follow_up: str = ""

    def to_dict(self):
        return {
            "reply": self.reply,
            "source": self.source,
            "urgency_detected": self.urgency_detected,
            "disclaimer": self.disclaimer,
            "conversation_id": self.conversation_id,
            "detected_intents": self.detected_intents,
            "detected_entities": self.detected_entities,
            "follow_up": self.follow_up,
        }
