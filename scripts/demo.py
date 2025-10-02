#!/usr/bin/env python
"""Interactive chatbot demo."""

import sys
from pathlib import Path
import uuid

sys.path.append(str(Path(__file__).parent.parent))

from nlu.intent_classifier import IntentClassifier
from dialogue.state_machine import DialogueManager
from tools.bank_api_adapter import BankingAPIAdapter

def run_demo():
    """Run interactive demo."""

    print("\n" + "="*70)
    print("BANKING CHATBOT - DEMO")
    print("="*70 + "\n")

    print("Loading chatbot...")

    try:
        intent_classifier = IntentClassifier()
        intent_classifier.load_model("trained_model/distilbert_intent")
        print("✓ Intent classifier loaded")
    except Exception as e:
        print(f"⚠️  Error: {e}")
        print("Train model first: python scripts/train_all.py")
        return 0

    backend = BankingAPIAdapter()
    manager = DialogueManager(intent_classifier=intent_classifier, 
                             backend_adapter=backend)

    print("✓ Chatbot ready!\n")
    print("="*70)
    print("Example queries:")
    print("  - What's my checking balance?")
    print("  - Show my recent transactions")
    print("  - I lost my card")
    print("\nType 'quit' to exit.")
    print("="*70 + "\n")

    session_id = str(uuid.uuid4())

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nBot: Goodbye!")
                break

            result = manager.process_message(session_id, user_input)

            print(f"Bot: {result['response']}")
            print(f"[Intent: {result['intent']} ({result['confidence']:.2f})]\n")

        except KeyboardInterrupt:
            print("\n\nBot: Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_demo()
