"""Natural language response generation."""
from typing import Dict

class ResponseGenerator:
    """Generate natural language responses from templates."""

    def __init__(self):
        self.templates = {
            "balance_inquiry": "Your {account} balance is ${amount}.",
            "transaction_history": "Here are your transactions from {date_range}:\n{transactions}",
            "transfer_success": "Transfer complete. ${amount} sent to {target_account}.",
            "card_lost": "Card {last4} reported lost. New card in 3-5 business days.",
        }

    def generate(self, intent: str, data: Dict) -> str:
        """Generate response from template."""

        if intent not in self.templates:
            return "I've processed your request."

        template = self.templates[intent]
        try:
            return template.format(**data)
        except KeyError:
            return "I processed your request but couldn't format the response."

    def add_followup_options(self, response: str, intent: str) -> str:
        """Add follow-up suggestions."""
        followups = {
            "balance_inquiry": "\nWould you like to see transactions?",
            "transaction_history": "\nNeed anything else?",
        }

        if intent in followups:
            response += followups[intent]

        return response
