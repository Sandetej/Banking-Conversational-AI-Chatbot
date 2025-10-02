"""Intent Classification using DistilBERT (absolute path-safe)."""
import json
import os
from pathlib import Path
from typing import Dict, Tuple, Optional

import numpy as np
import torch
from datasets import Dataset
from sklearn.metrics import precision_recall_fscore_support
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)

class IntentClassifier:
    """DistilBERT-based intent classifier with robust path resolution."""

    def __init__(
        self,
        model_name: str = "distilbert-base-uncased",  # HF id or local folder (relative or absolute)
        num_labels: int = 77,
        device: Optional[str] = None,
        project_root: Optional[Path] = None,  # allow override in tests
    ):
        self.model_name = model_name
        self.num_labels = num_labels
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Resolve project root to the repo root (…/your-repo/)
        # file: .../src/nlu/intent_classifier.py -> parents[2] == repo root with src/ and models/
        self.PROJECT_ROOT = Path(__file__).resolve().parents[2] if project_root is None else Path(project_root)

        self.tokenizer = None
        self.model = None
        self.intent_to_id: Dict[str, int] = {}
        self.id_to_intent: Dict[int, str] = {}

    # ---------- path helpers ----------
    def _resolve_load_path(self, name_or_path: str) -> str:
        """If name_or_path is a local (relative) directory under PROJECT_ROOT, return its absolute path.
        Otherwise return name_or_path (treated as HF repo id or absolute path)."""
        p = Path(name_or_path)
        if p.is_absolute():
            return str(p)
        local = (self.PROJECT_ROOT / p).resolve()
        return str(local) if local.exists() else name_or_path  # fallback to hub id

    def _resolve_save_dir(self, output_dir: str) -> str:
        p = Path(output_dir)
        return str(p if p.is_absolute() else (self.PROJECT_ROOT / p).resolve())

    # ---------- data ----------
    def load_data(self, filepath: str) -> list:
        data = []
        with open(filepath, "r") as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    data.append({"text": record.get("text", ""), "intent": record["intent"]})
        return data

    def build_vocab(self, data: list) -> None:
        intents = sorted({d["intent"] for d in data})
        self.intent_to_id = {intent: idx for idx, intent in enumerate(intents)}
        self.id_to_intent = {idx: intent for intent, idx in self.intent_to_id.items()}
        self.num_labels = len(intents)

    def prepare_dataset(self, data: list, max_length: int = 128) -> Dataset:
        if not self.tokenizer:
            # IMPORTANT: resolve to absolute if local
            load_path = self._resolve_load_path(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(load_path)

        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                padding="max_length",
                truncation=True,
                max_length=max_length,
            )

        dataset = Dataset.from_dict(
            {
                "text": [d["text"] for d in data],
                # Use 'labels' (preferred by HF Trainer)
                "labels": [self.intent_to_id[d["intent"]] for d in data],
            }
        )
        dataset = dataset.map(tokenize_function, batched=True)
        dataset = dataset.remove_columns(["text"])
        return dataset

    # ---------- metrics ----------
    def compute_metrics(self, eval_pred):
        predictions, labels = eval_pred
        preds = np.argmax(predictions, axis=1)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, preds, average="weighted", zero_division=0
        )
        return {"precision": precision, "recall": recall, "f1": f1}

    # ---------- training ----------
    def train(
        self,
        train_filepath: str,
        val_filepath: str,
        output_dir: str = "models/distilbert_intent",
        epochs: int = 5,
        batch_size: int = 32,
        learning_rate: float = 2e-5,
        warmup_steps: int = 500,
    ):
        print("Loading training data...")
        train_data = self.load_data(train_filepath)
        val_data = self.load_data(val_filepath)
        print(f"Train: {len(train_data)}, Val: {len(val_data)}")

        self.build_vocab(train_data + val_data)
        print(f"Intents: {self.num_labels}")

        # Resolve local or hub id for initialization
        load_path = self._resolve_load_path(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            load_path, num_labels=self.num_labels
        ).to(self.device)

        train_dataset = self.prepare_dataset(train_data)
        val_dataset = self.prepare_dataset(val_data)

        # Save directory must be absolute to avoid cwd surprises
        abs_output = self._resolve_save_dir(output_dir)
        Path(abs_output).mkdir(parents=True, exist_ok=True)

        training_args = TrainingArguments(
            output_dir=abs_output,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=learning_rate,
            warmup_steps=warmup_steps,
            weight_decay=0.01,
            logging_steps=100,
            evaluation_strategy="epoch",   # <- correct arg name
            save_strategy="epoch",
            save_total_limit=3,
            metric_for_best_model="f1",
            greater_is_better=True,
            load_best_model_at_end=True,
            push_to_hub=False,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=self.tokenizer,
            compute_metrics=self.compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
        )

        print("Training...")
        trainer.train()

        # Persist artifacts
        self.model.save_pretrained(abs_output)
        self.tokenizer.save_pretrained(abs_output)
        with open(Path(abs_output) / "intent_mapping.json", "w") as f:
            json.dump(self.intent_to_id, f, indent=2)

        print(f"✓ Model saved to {abs_output}")

    # ---------- inference ----------
    def load_model(self, model_path: str):
        """Load trained model from local dir or hub id, resolving local relative paths."""
        load_path = self._resolve_load_path(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(load_path).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(load_path)

        # Load mapping only if it's a local directory that has it
        mp = Path(load_path)
        mapping_file = mp / "intent_mapping.json" if mp.exists() and mp.is_dir() else None
        if mapping_file and mapping_file.exists():
            with open(mapping_file, "r") as f:
                self.intent_to_id = json.load(f)
            # keys are strings when dumped; normalize to ints
            self.id_to_intent = {int(v): k for k, v in self.intent_to_id.items()}
        else:
            # Fallback: keep any existing mapping (e.g., when loading a hub model)
            if not self.intent_to_id:
                raise ValueError(
                    "intent_mapping.json not found. Load a local trained model directory "
                    "or set intent_to_id before calling predict()."
                )

        self.model.eval()
        print(f"✓ Model loaded from {load_path}")

    def predict(self, text: str, return_probs: bool = False):
        if not self.model or not self.tokenizer:
            raise ValueError("Model not loaded. Call load_model() first.")

        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=128, padding=True
        ).to(self.device)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs = torch.softmax(logits, dim=1)[0]
        pred_idx = int(torch.argmax(probs))
        pred_intent = self.id_to_intent[pred_idx]
        confidence = float(probs[pred_idx])

        if return_probs:
            top_k = torch.topk(probs, k=min(3, probs.numel()))
            return {
                "intent": pred_intent,
                "confidence": confidence,
                "top_k": [
                    {"intent": self.id_to_intent[int(idx)], "score": float(score)}
                    for idx, score in zip(top_k.indices, top_k.values)
                ],
            }

        return pred_intent, confidence
