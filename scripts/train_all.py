#!/usr/bin/env python
"""Train all models end-to-end."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from data_src.data_generator import DialogueGenerator
from data_src.data_loader import DataLoader, prepare_datasets
from nlu.intent_classifier import IntentClassifier

def generate_data():
    """Generate synthetic data."""
    print("\n" + "="*60)
    print("STEP 1: Generating Synthetic Data")
    print("="*60)

    generator = DialogueGenerator()
    generator.generate_synthetic_dialogues(
        n_samples_per_intent=50,
        output_file="data/raw/synthetic_dialogues.jsonl"
    )

def prepare_data():
    """Prepare data splits."""
    print("\n" + "="*60)
    print("STEP 2: Preparing Data Splits")
    print("="*60)

    prepare_datasets()

def train_intent_classifier():
    """Train intent classifier."""
    print("\n" + "="*60)
    print("STEP 3: Training Intent Classifier")
    print("="*60)

    classifier = IntentClassifier()

    try:
        classifier.train(
            train_filepath="data/processed/intents_train.jsonl",
            val_filepath="data/processed/intents_val.jsonl",
            output_dir="models/distilbert_intent",
            epochs=3,
            batch_size=16
        )
        print("✓ Training completed")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("\n" + "="*60)
    print("BANKING CHATBOT - TRAINING PIPELINE")
    print("="*60 + "\n")

    generate_data()
    prepare_data()
    train_intent_classifier()

    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run demo: python scripts/demo.py")
    print("2. Start API: python api/main.py")

if __name__ == "__main__":
    main()
