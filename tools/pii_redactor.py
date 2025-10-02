"""Response PII redaction."""
import re

class ResponseRedactor:
    """Redact PII from bot responses."""

    def __init__(self):
        self.patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "account": r"\b\d{10}\b",
        }

    def redact(self, text: str) -> str:
        """Redact all PII from text."""
        for pattern in self.patterns.values():
            text = re.sub(pattern, "****", text)
        return text
