"""Multi-turn dialogue context management."""
from typing import Dict, List, Optional
from datetime import datetime

class ContextManager:
    """Manage conversation context across turns."""

    def __init__(self, session_id: str, max_turns: int = 20):
        self.session_id = session_id
        self.max_turns = max_turns
        self.context = {
            "history": [],
            "slots": {},
            "state": "idle",
            "intent": None,
            "entities": [],
        }

    def add_turn(self, role: str, message: str, metadata: Dict = None):
        """Add conversation turn."""
        turn = {
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        self.context["history"].append(turn)
        if len(self.context["history"]) > self.max_turns:
            self.context["history"] = self.context["history"][-self.max_turns:]

    def get_history(self, max_turns: int = 5) -> str:
        """Get formatted conversation history."""
        recent = self.context["history"][-max_turns:]
        return "\n".join([f"{t['role']}: {t['message']}" for t in recent])

    def update_slots(self, slots: Dict):
        """Update dialogue slots."""
        self.context["slots"].update(slots)

    def get_context_summary(self) -> Dict:
        """Get context summary."""
        return {
            "session_id": self.session_id,
            "turns": len(self.context["history"]),
            "state": self.context["state"],
            "slots": self.context["slots"],
            "intent": self.context["intent"],
        }
