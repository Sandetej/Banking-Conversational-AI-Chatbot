from collections import defaultdict
import numpy as np
from typing import Dict

class MetricsCollector:
    """Collect telemetry metrics."""

    def __init__(self):
        self.intent_counts = defaultdict(int)
        self.confidence_scores = []
        self.response_times = []
        self.fallback_count = 0
        self.dialogue_success_count = 0

    def record_intent(self, intent: str, confidence: float):
        self.intent_counts[intent] += 1
        self.confidence_scores.append(confidence)

    def record_latency(self, latency_ms: float):
        self.response_times.append(latency_ms)

    def record_fallback(self):
        self.fallback_count += 1

    def record_dialogue_completion(self, success: bool):
        if success:
            self.dialogue_success_count += 1

    def get_summary(self) -> Dict:
        return {
            "avg_confidence": np.mean(self.confidence_scores) if self.confidence_scores else 0,
            "p95_latency": np.percentile(self.response_times, 95) if self.response_times else 0,
            "fallback_rate": self.fallback_count / max(sum(self.intent_counts.values()), 1),
        }
