"""Mock Banking API Adapter."""
import random
from typing import Dict

class BankingAPIAdapter:
    """Mock adapter for backend services."""

    def __init__(self):
        self.mock_accounts = {
            "checking": {"balance": 2450.32, "account_id": "****7890"},
            "savings": {"balance": 15230.50, "account_id": "****3421"},
            "credit_card": {"balance": -1250.00, "account_id": "****5678"}
        }

    def query(self, intent: str, slots: Dict) -> Dict:
        """Query mock backend."""

        if intent == "get_balance":
            return self._get_balance(slots)
        elif intent == "transaction_history":
            return self._get_transactions(slots)
        elif intent == "transfer_money":
            return self._transfer_money(slots)
        elif intent == "lost_or_stolen_card":
            return self._report_card_lost(slots)
        else:
            return {"message": "Request processed"}

    def _get_balance(self, slots: Dict) -> Dict:
        account_type = slots.get("account_type", "checking")
        account = self.mock_accounts.get(account_type,
                                        self.mock_accounts["checking"])
        return {
            "balance": account["balance"],
            "account_id": account["account_id"],
            "account_type": account_type
        }

    def _get_transactions(self, slots: Dict) -> Dict:
        merchants = ["Amazon", "Starbucks", "Walmart", "Gas Station", "Netflix"]
        transactions = []

        for i in range(5):
            transactions.append({
                "merchant": random.choice(merchants),
                "amount": round(random.uniform(5, 200), 2),
                "type": "debit"
            })

        return {"transactions": transactions}

    def _transfer_money(self, slots: Dict) -> Dict:
        return {
            "status": "success",
            "confirmation_code": f"TRANS{random.randint(100000, 999999)}"
        }

    def _report_card_lost(self, slots: Dict) -> Dict:
        return {
            "status": "reported",
            "new_card_eta": "3-5 business days"
        }
