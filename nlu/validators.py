"""Entity validators."""
import re
from datetime import datetime, timedelta
from typing import Optional, Dict

class EntityValidator:
    @staticmethod
    def validate_account_number(text: str) -> Optional[str]:
        match = re.match(r"(\d{10})$", text.replace(" ", "").replace("-", ""))
        if match:
            return match.group(1)
        return None

    @staticmethod
    def validate_card_last4(text: str) -> Optional[str]:
        match = re.search(r"(\d{4})", text)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def parse_date_range(text: str) -> Optional[Dict]:
        text_lower = text.lower()

        if "last week" in text_lower:
            end = datetime.now()
            start = end - timedelta(days=7)
            return {"start": start.isoformat(), "end": end.isoformat()}

        if "last month" in text_lower:
            end = datetime.now()
            start = end - timedelta(days=30)
            return {"start": start.isoformat(), "end": end.isoformat()}

        pattern = r"(\d{4}-\d{2}-\d{2})\s*(?:to|through|-)\s*(\d{4}-\d{2}-\d{2})"
        match = re.search(pattern, text)
        if match:
            try:
                start = datetime.strptime(match.group(1), "%Y-%m-%d")
                end = datetime.strptime(match.group(2), "%Y-%m-%d")
                return {"start": start.isoformat(), "end": end.isoformat()}
            except ValueError:
                pass

        return None

    @staticmethod
    def parse_amount(text: str) -> Optional[Dict]:
        pattern = r"([$€¥£]?)\s*(\d+\.?\d*)\s*([A-Z]{3})?"
        match = re.search(pattern, text)
        if match:
            symbol = match.group(1)
            amount_str = match.group(2)
            currency = match.group(3)

            if not currency:
                currency_map = {"$": "USD", "€": "EUR", "¥": "JPY", "£": "GBP"}
                currency = currency_map.get(symbol, "USD")

            try:
                return {"amount": float(amount_str), "currency": currency}
            except ValueError:
                pass

        return None
