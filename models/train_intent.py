"""Training script for intent classifier."""
from src.nlu.intent_classifier import IntentClassifier

def train_intent_model(train_path: str, val_path: str, output_dir: str = "models/distilbert_intent", epochs: int = 5):
    """Train intent classification model."""
    classifier = IntentClassifier()
    classifier.train(
        train_filepath=train_path,
        val_filepath=val_path,
        output_dir=output_dir,
        epochs=epochs,
    )
    print(f"✓ Intent model trained and saved to {output_dir}")
