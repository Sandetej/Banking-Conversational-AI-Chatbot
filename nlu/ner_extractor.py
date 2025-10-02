"""Named Entity Recognition."""
import spacy
from typing import List, Dict

class NERExtractor:
    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Downloading {model_name}...")
            import os
            os.system(f"python -m spacy download {model_name}")
            self.nlp = spacy.load(model_name)

    def extract_entities(self, text: str) -> List[Dict]:
        doc = self.nlp(text)
        entities = []

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "type": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })

        return entities
