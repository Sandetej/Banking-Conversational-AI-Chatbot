"""Dialogue state machine for multi-turn conversations."""
from enum import Enum
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class DialogueContext:
    """Conversation state across turns."""
    session_id: str
    user_id: Optional[str] = None
    state: str = "idle"
    slots: Dict = field(default_factory=dict)
    history: List = field(default_factory=list)
    confidence_threshold: float = 0.6
    fallback_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def add_turn(self, role: str, message: str):
        """Add conversation turn."""
        self.history.append((role, message))

    def get_context(self, max_turns: int = 5) -> str:
        """Get recent conversation context."""
        recent = self.history[-max_turns:]
        return "\n".join([f"{role}: {msg}" for role, msg in recent])

class DialoguePolicy:
    """Action selection policy."""

    def __init__(self):
        self.intent_slot_mapping = {
            "get_balance": ["account_type"],
            "transaction_history": ["account_type", "date_range"],
            "transfer_money": ["source_account", "target_account", "amount"],
            "lost_or_stolen_card": ["card_last4"],
        }

        self.high_risk_intents = [
            "transfer_money",
            "terminate_account",
            "change_pin",
            "disputed_transaction"
        ]

    def select_action(self, intent: str, confidence: float, context: DialogueContext) -> Dict:
        """Select next action based on context."""

        if confidence < 0.5:
            return {
                "action": "clarify",
                "params": {"intent": intent, "confidence": confidence},
                "next_state": "fallback",
                "response": f"I'm not sure I understood. Did you mean '{intent}'?"
            }

        if intent in self.intent_slot_mapping:
            required_slots = self.intent_slot_mapping[intent]
            missing = [s for s in required_slots if s not in context.slots]

            if missing:
                return {
                    "action": "fill_slot",
                    "params": {"slot": missing[0], "intent": intent},
                    "next_state": "slot_filling",
                    "response": f"I need your {missing[0].replace('_', ' ')}. Can you provide it?"
                }

        if intent in self.high_risk_intents:
            return {
                "action": "verify",
                "params": {"intent": intent, "slots": context.slots},
                "next_state": "verification",
                "response": "Please confirm this action by saying 'yes' or 'confirm'."
            }

        return {
            "action": "query_backend",
            "params": {"intent": intent, "slots": context.slots},
            "next_state": "query_backend",
            "response": "Processing your request..."
        }

class DialogueManager:
    """Main dialogue orchestrator."""

    def __init__(self, intent_classifier, ner_extractor=None, backend_adapter=None):
        self.intent_classifier = intent_classifier
        self.ner_extractor = ner_extractor
        self.backend_adapter = backend_adapter
        self.policy = DialoguePolicy()
        self.sessions: Dict[str, DialogueContext] = {}

    def process_message(self, session_id: str, user_message: str) -> Dict:
        """Process user message and return response."""

        if session_id not in self.sessions:
            self.sessions[session_id] = DialogueContext(session_id=session_id, state="greeting")

        context = self.sessions[session_id]
        context.add_turn("user", user_message)

        try:
            intent, confidence = self.intent_classifier.predict(user_message)
        except Exception as e:
            print(f"Intent classification error: {e}")
            intent = "general_inquiry"
            confidence = 0.3

        if self.ner_extractor:
            try:
                entities = self.ner_extractor.extract_entities(user_message)
                for entity in entities:
                    entity_type = entity.get("type", "").lower()
                    if entity_type:
                        context.slots[entity_type] = entity.get("text", "")
            except Exception as e:
                print(f"NER extraction error: {e}")

        action_spec = self.policy.select_action(intent, confidence, context)
        response = action_spec["response"]
        context.state = action_spec["next_state"]

        if action_spec["action"] == "query_backend" and self.backend_adapter:
            try:
                backend_response = self.backend_adapter.query(intent, context.slots)
                response = self._format_response(intent, backend_response, context)
                context.state = "completion"
            except Exception as e:
                print(f"Backend query error: {e}")
                response = "I encountered an issue processing your request."

        context.add_turn("bot", response)

        return {
            "session_id": session_id,
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "state": context.state,
            "slots": context.slots,
            "action": action_spec["action"]
        }

    def _format_response(self, intent: str, data: dict, context: DialogueContext) -> str:
        """Format backend data into response."""

        if intent == "get_balance":
            balance = data.get("balance", "N/A")
            account = context.slots.get("account_type", "Your")
            return f"{account.capitalize()} account balance: ${balance}"

        elif intent == "transaction_history":
            transactions = data.get("transactions", [])
            if not transactions:
                return "No transactions found for the specified period."

            summary = "\n".join([
                f"- {t.get('date', 'N/A')}: {t.get('merchant', 'Unknown')} - ${t.get('amount', '0')}"
                for t in transactions[:5]
            ])
            return f"Recent transactions:\n{summary}"

        return "I've processed your request."