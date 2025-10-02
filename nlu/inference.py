"""Batch and streaming inference for high-throughput scenarios."""
import torch
from typing import List, Dict
import asyncio

class Inferencer:
    """High-performance inference engine."""

    def __init__(self, model, tokenizer, device="cpu", batch_size=32):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.batch_size = batch_size

    def batch_predict(self, texts: List[str]) -> List[Dict]:
        """Batch inference for multiple texts."""
        results = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_results = self._inference_batch(batch)
            results.extend(batch_results)
        return results

    def _inference_batch(self, batch: List[str]) -> List[Dict]:
        """Internal batch processing."""
        inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs
