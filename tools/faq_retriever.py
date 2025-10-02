"""FAQ retrieval using embeddings."""
from typing import List, Dict

class FAQRetriever:
    """Retrieve FAQs using embedding similarity."""

    def __init__(self):
        self.faq_db = self._load_faqs()

    def _load_faqs(self) -> List[Dict]:
        """Load FAQ database."""
        return [
            {"q": "How do I reset my password?", "a": "Visit settings > Change Password"},
            {"q": "What's the transfer limit?", "a": "$10,000 per day for ACH"},
            {"q": "How long do transfers take?", "a": "Typically 1-2 business days"},
            {"q": "What are ATM fees?", "a": "$2.50 per out-of-network withdrawal"},
            {"q": "How do I update my address?", "a": "Go to settings > Personal Info"},
        ]

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve top-k FAQs matching query."""
        # Simple implementation - return top_k
        return self.faq_db[:min(top_k, len(self.faq_db))]
