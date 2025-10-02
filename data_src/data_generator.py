"""Synthetic dialogue generation."""
import json
import random
from typing import List, Dict
from pathlib import Path
from .dialogue_templates import DIALOGUE_TEMPLATES, SIMPLE_INTENTS

class DialogueGenerator:
    def __init__(self, templates: Dict = None):
        self.templates = templates or DIALOGUE_TEMPLATES

    def generate_synthetic_dialogues(self, n_samples_per_intent: int = 50,
                                     output_file: str = "data/raw/synthetic_dialogues.jsonl") -> None:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            for intent, templates_dict in self.templates.items():
                for _ in range(n_samples_per_intent):
                    if "single_turn" in templates_dict:
                        text = random.choice(templates_dict["single_turn"])
                        record = {
                            "intent": intent,
                            "text": text,
                            "entities": {}
                        }
                        f.write(json.dumps(record) + "\n")

            for intent in SIMPLE_INTENTS:
                for _ in range(n_samples_per_intent // 2):
                    text = f"I need help with {intent.replace('_', ' ')}"
                    record = {
                        "intent": intent,
                        "text": text,
                        "entities": {}
                    }
                    f.write(json.dumps(record) + "\n")

def main():
    generator = DialogueGenerator()
    generator.generate_synthetic_dialogues(n_samples_per_intent=50)

if __name__ == "__main__":
    main()
