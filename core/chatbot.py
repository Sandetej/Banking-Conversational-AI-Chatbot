from typing import Dict

class BankingChatbot:
    """Main chatbot orchestrator class."""

    def __init__(self, intent_classifier, ner_extractor, dialogue_manager, backend):
        self.intent_classifier = intent_classifier
        self.ner_extractor = ner_extractor
        self.dialogue_manager = dialogue_manager
        self.backend = backend

    def chat(self, session_id: str, user_message: str) -> Dict:
        """Process user message and return bot response."""
        return self.dialogue_manager.process_user_message(session_id, user_message)
