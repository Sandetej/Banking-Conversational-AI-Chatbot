"""Training script for NER model."""
from src.nlu.ner_extractor import NERExtractor

def train_ner_model(train_path: str, val_path: str, output_dir: str = "models/spacy_ner", epochs: int = 5):
    """Train NER model."""
    extractor = NERExtractor()
    extractor.train(
        train_filepath=train_path,
        val_filepath=val_path,
        output_dir=output_dir,
        epochs=epochs,
    )
    print(f"✓ NER model trained and saved to {output_dir}")
