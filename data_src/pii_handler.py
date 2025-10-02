"""PII detection and redaction."""
import re
from typing import Tuple, Dict

class PIIRedactor:
    PATTERNS = {
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CARD": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "PHONE": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z|a-z]{2,}\b",
        "ACCOUNT": r"\b\d{10}\b",
    }

    def __init__(self, mask_char: str = "*"):
        self.mask_char = mask_char

    def redact(self, text: str) -> Tuple[str, Dict]:
        redacted = text
        pii_found = {}

        for pii_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                pii_found[pii_type] = matches
                def mask_func(match):
                    val = match.group(0)
                    if len(val) >= 4:
                        return self.mask_char * (len(val) - 4) + val[-4:]
                    return self.mask_char * len(val)
                redacted = re.sub(pattern, mask_func, redacted)

        return redacted, pii_found

redactor = PIIRedactor()
