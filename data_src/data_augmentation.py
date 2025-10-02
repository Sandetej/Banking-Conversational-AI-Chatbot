"""Data augmentation utilities for NLP."""
import random
from typing import List, Dict
from collections import Counter

class DataAugmentation:
    """Data augmentation strategies."""

    def __init__(self):
        self.synonyms = {
            "balance": ["account balance", "funds", "money"],
            "transaction": ["purchase", "charge", "payment"],
            "show": ["display", "list", "tell me", "give me"],
            "card": ["debit card", "credit card"],
            "account": ["bank account"],
        }

    def paraphrase(self, text: str) -> str:
        """Simple synonym-based paraphrasing."""
        for word, subs in self.synonyms.items():
            if word in text.lower():
                text = text.lower().replace(word, random.choice(subs))
        return text

    def add_typo(self, text: str, typo_prob: float = 0.05) -> str:
        """Introduce random typos."""
        words = text.split()
        if not words:
            return text

        for _ in range(max(1, int(len(words) * typo_prob))):
            idx = random.randint(0, len(words) - 1)
            word = list(words[idx])

            if len(word) > 1:
                i = random.randint(0, len(word) - 2)
                word[i], word[i + 1] = word[i + 1], word[i]

            words[idx] = "".join(word)

        return " ".join(words)

    def balance_dataset(self, data: List[Dict], label_key: str = 'intent', min_samples: int = 50) -> List[Dict]:
        """Balance class distribution by upsampling minority classes."""

        label_counts = Counter(d[label_key] for d in data)
        balanced = list(data)

        for label, count in label_counts.items():
            if count < min_samples:
                samples = [d for d in data if d[label_key] == label]
                additional = random.choices(samples, k=min_samples - count)
                balanced.extend(additional)

        return balanced

    def augment_batch(self, data: List[Dict], num_augmented: int = 2, strategy: str = "paraphrase") -> List[Dict]:
        """Augment dataset by creating variations."""

        augmented = list(data)

        for original in data:
            text = original.get("text", "")
            if not text:
                continue

            for _ in range(num_augmented):
                if strategy == "paraphrase":
                    new_text = self.paraphrase(text)
                elif strategy == "typo":
                    new_text = self.add_typo(text)
                else:
                    new_text = text

                augmented_record = original.copy()
                augmented_record["text"] = new_text
                augmented_record["augmented"] = True
                augmented.append(augmented_record)

        return augmented

def balance_dataset(data: List[Dict], label_key: str = 'intent', min_samples: int = 50) -> List[Dict]:
    """Simple function to balance dataset."""
    label_counts = Counter(d[label_key] for d in data)
    balanced = list(data)
    for label, count in label_counts.items():
        if count < min_samples:
            samples = [d for d in data if d[label_key] == label]
            additional = random.choices(samples, k=min_samples - count)
            balanced.extend(additional)
    return balanced