"""Dialogue policy engine for action selection."""
from typing import Dict, List

class DialoguePolicy:
    """Determine next action based on state and confidence."""

    def __init__(self):
        self.policies = {
            "confidence_threshold": 0.6,
            "fallback_threshold": 0.5,
        }

    def select_action(self, intent: str, confidence: float, context: Dict) -> Dict:
        """Select action based on policy rules."""

        if confidence < self.policies["fallback_threshold"]:
            return {
                "action": "escalate",
                "reason": "very_low_confidence",
            }

        if confidence < self.policies["confidence_threshold"]:
            return {
                "action": "clarify",
                "reason": "medium_confidence",
            }

        # Check missing slots
        required = self._get_required_slots(intent)
        missing = [s for s in required if s not in context.get("slots", {})]

        if missing:
            return {
                "action": "fill_slot",
                "slot": missing[0],
                "reason": "incomplete_information",
            }

        return {
            "action": "query_backend",
            "reason": "ready",
            "confidence": confidence,
        }

    def _get_required_slots(self, intent: str) -> List[str]:
        """Get required slots for intent."""
        mapping = {
            "balance_inquiry": ["account_type"],
            "transaction_history": ["account_type", "date_range"],
            "transfer_money": ["source_account", "target_account", "amount"],
        }
        return mapping.get(intent, [])
