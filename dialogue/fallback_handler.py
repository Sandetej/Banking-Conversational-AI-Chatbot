"""Fallback and recovery strategies."""
from typing import Dict

class FallbackHandler:
    """Handle low-confidence and out-of-domain queries."""

    def __init__(self, escalation_threshold: float = 0.3):
        self.escalation_threshold = escalation_threshold

    def handle_low_confidence(self, intent: str, confidence: float) -> Dict:
        """Handle low confidence prediction."""

        if confidence < self.escalation_threshold:
            return {
                "action": "escalate_to_human",
                "reason": "very_low_confidence",
                "message": "I'm having trouble. Let me connect you with an agent.",
            }

        return {
            "action": "clarify_intent",
            "reason": "low_confidence",
            "message": f"I think you mean {intent}. Is that correct?",
            "intent": intent,
        }

    def handle_jailbreak_attempt(self, text: str) -> Dict:
        """Detect and refuse jailbreak attempts."""
        refusal_keywords = ["password", "security code", "PIN", "ssn"]

        if any(kw in text.lower() for kw in refusal_keywords):
            return {
                "action": "refuse_and_escalate",
                "reason": "jailbreak_attempt",
                "message": "I'll never ask for passwords or SSN.",
            }

        return {"action": "allow", "reason": "safe"}
