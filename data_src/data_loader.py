"""Data loading and splitting."""
import json
from typing import List, Dict, Tuple
from pathlib import Path
from sklearn.model_selection import train_test_split

class DataLoader:
    @staticmethod
    def load_dialogues(filepath: str) -> List[Dict]:
        data = []
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data

    @staticmethod
    def split_data(data: List[Dict], train_ratio: float = 0.7,
                   val_ratio: float = 0.15, test_ratio: float = 0.15,
                   seed: int = 42) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        intents = [d["intent"] for d in data]
        train, temp = train_test_split(data, test_size=(val_ratio + test_ratio),
                                       stratify=intents, random_state=seed)
        temp_intents = [d["intent"] for d in temp]
        val, test = train_test_split(temp, test_size=test_ratio / (val_ratio + test_ratio),
                                     stratify=temp_intents, random_state=seed)
        return train, val, test

    @staticmethod
    def save_split(data: List[Dict], filepath: str) -> None:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            for record in data:
                f.write(json.dumps(record) + "\n")

    @staticmethod
    def check_leakage(train: List[Dict], val: List[Dict], test: List[Dict]) -> bool:
        train_texts = {d["text"] for d in train}
        val_texts = {d["text"] for d in val}
        test_texts = {d["text"] for d in test}

        if train_texts & val_texts or train_texts & test_texts or val_texts & test_texts:
            print("⚠️  Data leakage detected!")
            return False
        return True

def prepare_datasets():
    loader = DataLoader()
    print("Loading synthetic dialogues...")
    data = loader.load_dialogues("data/raw/synthetic_dialogues.jsonl")
    print(f"Total samples: {len(data)}")

    print("Splitting data...")
    train, val, test = loader.split_data(data)

    if loader.check_leakage(train, val, test):
        print("✓ No data leakage detected")

    print("Saving splits...")
    loader.save_split(train, "data/processed/intents_train.jsonl")
    loader.save_split(val, "data/processed/intents_val.jsonl")
    loader.save_split(test, "data/processed/intents_test.jsonl")

    print(f"✓ Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")

if __name__ == "__main__":
    prepare_datasets()
