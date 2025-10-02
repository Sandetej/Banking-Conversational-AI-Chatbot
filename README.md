# Banking Conversational AI Chatbot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready conversational AI chatbot for banking customer support powered by DistilBERT, spaCy, and FastAPI. Handles 77 banking intents with multi-turn dialogue, entity extraction, and comprehensive safety features.

---

## 🎯 Overview

This project implements an end-to-end banking chatbot system that:

- **Classifies 77 banking intents** using DistilBERT transformer model (~90% F1 score)
- **Extracts entities** (accounts, cards, dates, amounts) using spaCy NER
- **Manages multi-turn dialogues** with context retention and slot filling
- **Redacts PII** for data privacy and security
- **Serves via FastAPI** with interactive Swagger documentation
- **Provides both CLI and API interfaces** for maximum flexibility

### Key Features

✅ **Intent Classification** - 77 banking intents with confidence scoring  
✅ **Entity Extraction** - 12+ entity types (card, account, amount, date, etc.)  
✅ **Multi-Turn Dialogue** - Context management, slot filling, clarification  
✅ **Safety Features** - PII redaction, fallback handling, input validation  
✅ **Interactive Demo** - Command-line chatbot for local testing  
✅ **Data Augmentation** - Synthetic data generation for training  
✅ **Model Evaluation** - Comprehensive metrics and performance tracking  

---

## 📊 Architecture

```
User Input
    ↓
NLU Pipeline (Intent Classification + NER)
    ↓
Dialogue Manager (State Machine)
    ↓
Slot Filling & Policy Selection
    ↓
Backend Query / Response Generation
    ↓
PII Redaction
    ↓
Response to User
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Train the Model (5-10 minutes)
```bash
python scripts/train_all.py
```

### 3. Run the Chatbot

**Option A: Interactive Demo**
```bash
python scripts/demo.py
```

**Option B: API Server**
```bash
python api/main.py
# Then visit: http://localhost:8000/docs
```

---

## 💬 How to Chat

### 1. **Interactive Terminal Demo** (Easiest)
```bash
python scripts/demo.py

You: What's my balance?
Bot: Your checking account balance is $2,450.32
[Intent: get_balance (confidence: 0.95)]
```

### 2. **Web API with Swagger UI** (Best for Testing)
```
http://localhost:8000/docs
```
- Click POST /chat
- Click "Try it out"
- Send: `{"session_id": "user_123", "message": "What is my balance?"}`
- See response!

### 3. **Python Code** (Programmatic)
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"session_id": "user_123", "message": "What is my balance?"}
)
print(response.json())
```

---

## 📚 Supported Banking Intents (77 Total)

### Card Management
- activate_my_card, lost_or_stolen_card, card_not_working, compromised_card, pin_reset, ...

### Account & Balance
- balance_inquiry, pending_top_up, account_verification, account_details, ...

### Transfers & Payments
- transfer_money, cancel_transfer, pending_transfer, declined_transfer, exchange_rate, ...

### Disputes & Issues
- dispute_transaction, fraudulent_transaction, wrong_amount_transferred, ...

### General Support
- contact_customer_support, branch_locator, atm_locator, service_status, ...

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Root info |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger documentation |
| POST | `/chat` | Chat with chatbot |
| GET | `/metrics` | Get statistics |
| GET | `/sessions` | List active sessions |

### Example: Chat Endpoint

**Request:**
```json
{
  "session_id": "user_123",
  "message": "What is my balance?"
}
```

**Response:**
```json
{
  "session_id": "user_123",
  "response": "Your checking account balance is $2,450.32",
  "intent": "get_balance",
  "confidence": 0.95,
  "state": "completion",
  "timestamp": "2025-11-02T14:40:00"
}
```

---

## 📁 Project Structure

```
banking-conversational-ai-chatbot/
│
|── nlu/                     # Intent classification & NER
│   ├── intent_classifier.py # DistilBERT model
│   ├── ner_extractor.py     # Entity extraction
│   ├── tokenizer.py         # Tokenization
│   ├── validators.py        # Entity validators
│   └── inference.py         # Batch inference
├── dialogue/                # Dialogue management
│   ├── state_machine.py     # Dialogue manager & FSM
│   ├── slot_filler.py       # Slot extraction
│   ├── context_manager.py   # Multi-turn context
│   ├── policy.py            # Action selection
│   ├── fallback_handler.py  # Fallback recovery
│   └── response_generator.py# Response generation
│   │
├── data/                    # Data generation & loading
│   ├── data_generator.py    # Synthetic data
│   ├── data_loader.py       # Dataset loading
│   ├── augmentation.py      # Data augmentation
│   ├── dialogue_templates.py# Intent templates
│   └── pii_handler.py       # PII detection
│
├── tools/                   # Utilities
|   ├── bank_api_adapter.py  # Mock backend
│   ├── faq_retriever.py     # FAQ retrieval
│   ├── knowledge_graph.py   # Knowledge base
│   └── pii_redactor.py      # PII redaction
│
├── models/                  # Model training
│   ├── train_intent.py      # Intent training
│   ├── train_ner.py         # NER training
│   ├── evaluate.py          # Evaluation
│   └── export_model.py      # Model export
│
└── core/                    # Core components
│  ├── chatbot.py           # Main orchestrator
│  ├── session_manager.py   # Session management
│  └── metrics_collector.py # Telemetry
│
├── api/
│   ├── main.py                  # FastAPI app
│   ├── schemas.py               # Pydantic models
│   ├── middleware.py            # Middleware
│   ├── routes.py                # Routes
│   └── streaming.py             # WebSocket
│
├── scripts/
│   ├── train_all.py             # Training pipeline
│   └── demo.py                  # Interactive demo
│
├── config/
│   ├── config.yaml              # Configuration
│   ├── intents.yaml             # Banking intents
│   └── entities.yaml            # Entity definitions
│
├── data/                        # Dataset directory
│   ├── raw/                     # Raw data (generated)
│   └── processed/               # Processed splits (generated)
│
├── models/                      # Trained models (generated)
│   └── distilbert_intent/       # Intent classifier
│
├── README.md                    # This file
├── requirements.txt             # Dependencies
└── Exit
```

---

## 🧠 Model Details

### Intent Classifier
- **Architecture:** DistilBERT (66M parameters)
- **Training Data:** 2,450 synthetic examples
- **Performance:** ~90% F1 score
- **Inference:** <500ms per request
- **Intents:** 77 banking categories

### NER Extractor
- **Model:** spaCy en_core_web_sm + fine-tuning
- **Entities:** 12 types (card, account, amount, date, merchant, etc.)
- **Performance:** ~85% F1 score

### Dialogue System
- **Type:** Finite State Machine (FSM)
- **States:** idle, greeting, intent_classification, slot_filling, execution, completion, fallback, escalation
- **Context:** Multi-turn memory (20 recent turns)
- **Features:** Slot filling, policy selection, fallback handling

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Intent F1 Score | ~90% |
| Entity F1 Score | ~85% |
| Dialogue Success | ~85% |
| Response Time | <500ms |
| Fallback Rate | ~5% |
| PII Detection | 99%+ |

---

## 🛠️ Configuration

Edit `config/config.yaml` to customize:

```yaml
training:
  intent:
    epochs: 5
    batch_size: 32
    learning_rate: 2.0e-5

api:
  host: 0.0.0.0
  port: 8000
  log_level: info

dialogue:
  confidence_threshold: 0.6
  fallback_threshold: 0.5
```

---

## 🔄 Customizing Intents

1. Edit `config/intents.yaml` - Add new intent names
2. Add templates to `src/data/dialogue_templates.py` - Add dialogue examples
3. Retrain: `python scripts/train_all.py`

---

## ❌ Troubleshooting

### API Not Responding
```bash
# 1. Verify training completed
ls -la models/distilbert_intent/

# 2. Check if server is running
curl http://localhost:8000/health

# 3. Try different port
python -m uvicorn api.main:app --port 9000
```

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Verify imports
python -c "from src.nlu.intent_classifier import IntentClassifier; print('OK')"
```

### Model Training Issues
```bash
# Ensure spaCy model is installed
python -m spacy download en_core_web_sm

# Check Python version
python --version  # Should be 3.10+
```

---

## 📖 Documentation

- **README.md** - Full documentation (this file)
- **QUICKSTART.md** - 5-minute setup guide
- **API_QUICK_START.txt** - API getting started
- **http://localhost:8000/docs** - Interactive API docs (when server running)

---

## 🙏 Acknowledgments

- BANKING77 Dataset by PolyAI
- Transformers by Hugging Face
- spaCy by Explosion AI
- FastAPI by Sebastián Ramírez

---

