"""Model evaluation."""
from sklearn.metrics import f1_score, precision_recall_fscore_support
from typing import List, Dict

def evaluate_model(model, test_data: List[Dict]) -> Dict:
    """Evaluate model on test set."""
    predictions = []
    ground_truth = []

    for record in test_data:
        pred, conf = model.predict(record["text"])
        predictions.append(pred)
        ground_truth.append(record["intent"])

    f1 = f1_score(ground_truth, predictions, average="weighted")
    precision, recall, _, _ = precision_recall_fscore_support(
        ground_truth, predictions, average="weighted"
    )

    return {"f1": f1, "precision": precision, "recall": recall}

def evaluate_dialogue(manager, test_scenarios: List[Dict]) -> Dict:
    """Evaluate dialogue manager."""
    success_count = 0

    for scenario in test_scenarios:
        result = manager.process_user_message(scenario["session_id"], scenario["message"])
        if result["state"] == "completion":
            success_count += 1

    success_rate = success_count / max(len(test_scenarios), 1)
    return {"success_rate": success_rate}
