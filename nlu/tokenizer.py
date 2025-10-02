"""Tokenization wrapper for multi-layer token processing."""
import spacy
from transformers import AutoTokenizer

class BankingTokenizer:
    """Handle both spaCy and BERT tokenization."""

    def __init__(self, model_name="distilbert-base-uncased"):
        self.spacy_nlp = spacy.load("en_core_web_sm")
        self.bert_tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(self, text: str) -> dict:
        """Tokenize text using both spaCy and BERT."""
        doc = self.spacy_nlp(text)
        spacy_tokens = [token.text for token in doc]
        bert_tokens = self.bert_tokenizer.tokenize(text)
        return {"spacy": spacy_tokens, "bert": bert_tokens, "doc": doc}
