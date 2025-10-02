"""Extract and validate slots from user input."""
from typing import Dict, List

class SlotFiller:
    """Extract and validate dialogue slots."""

    def __init__(self, validators: Dict = None):
        self.validators = validators or {}

    def fill_slots(self, entities: List[Dict], intent: str) -> Dict:
        """Fill slots from extracted entities."""
        slots = {}
        for entity in entities:
            entity_type = entity["type"].lower()
            entity_text = entity["text"]
            if entity_type in self.validators:
                validated = self.validators[entity_type](entity_text)
                if validated:
                    slots[entity_type] = validated
        return slots

    def get_missing_slots(self, intent: str, filled_slots: Dict) -> List[str]:
        """Identify missing required slots."""
        required = self.get_required_slots(intent)
        return [s for s in required if s not in filled_slots]

    def get_required_slots(self, intent: str) -> List[str]:
        """Get required slots for each intent."""
        mapping = {
            "balance_inquiry": ["account_type"],
            "transaction_history": ["account_type", "date_range"],
            "transfer_money": ["source_account", "target_account", "amount"],
            "lost_or_stolen_card": ["card_last4"],
        }
        return mapping.get(intent, [])
