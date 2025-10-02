"""Optional: Knowledge graph for product information."""
from typing import Dict, List

class KnowledgeGraph:
    """Product and banking knowledge base."""

    def __init__(self):
        self.entities = {
            "products": {
                "checking": {"type": "deposit", "min_balance": 0, "apr": 0, "monthly_fee": 0},
                "savings": {"type": "deposit", "min_balance": 25, "apr": 4.5, "monthly_fee": 0},
                "credit_card": {"type": "credit", "credit_limit": 5000, "apr": 18.99},
            },
            "locations": {
                "downtown": {"address": "123 Main St", "hours": "9-5 M-F"},
                "mall": {"address": "456 Park Ave", "hours": "10-8 M-Sat"},
            }
        }

    def lookup_product(self, product_name: str) -> Dict:
        """Look up product details."""
        return self.entities["products"].get(product_name, {})

    def lookup_location(self, location_name: str) -> Dict:
        """Look up branch location."""
        return self.entities["locations"].get(location_name, {})
