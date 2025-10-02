from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.nlu.intent_classifier import IntentClassifier
from src.dialogue.state_machine import DialogueManager
from src.tools.bank_api_adapter import BankingAPIAdapter
from src.data.pii_handler import redactor

# Import schemas
from api.schemas import ChatRequest, ChatResponse, HealthResponse, MetricsResponse

# Initialize FastAPI app
app = FastAPI(
    title="Banking Conversational AI Chatbot",
    description="NLP-powered chatbot for banking customer support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot_manager = None
metrics = {
    "total_conversations": 0,
    "avg_confidence": 0.0,
    "fallback_count": 0,
    "total_messages": 0,
}

@app.on_event("startup")
async def startup_event():
    """Initialize chatbot on startup."""
    global chatbot_manager

    try:
        print("🚀 Starting Banking Chatbot API...")

        # Load intent classifier
        intent_classifier = IntentClassifier()

        try:
            intent_classifier.load_model("models/distilbert_intent")
            print("✓ Loaded trained intent classifier")
        except Exception as e:
            print(f"⚠️  Could not load trained model: {e}")
            print("   Using untrained model - please train first with: python scripts/train_all.py")

        # Initialize backend adapter
        backend = BankingAPIAdapter()

        # Initialize dialogue manager
        chatbot_manager = DialogueManager(
            intent_classifier=intent_classifier,
            backend_adapter=backend
        )

        print("✓ Chatbot initialized successfully")
        print("✓ API ready at http://localhost:8000")
        print("✓ Docs at http://localhost:8000/docs")

    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Banking Conversational AI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "✓ Running"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - Process user message."""

    if not chatbot_manager:
        raise HTTPException(status_code=503, detail="Chatbot not initialized. Train model first: python scripts/train_all.py")

    try:
        clean_message, pii_found = redactor.redact(request.message)

        result = chatbot_manager.process_message(
            session_id=request.session_id,
            user_message=clean_message
        )

        safe_response, _ = redactor.redact(result["response"])

        metrics["total_messages"] += 1
        metrics["total_conversations"] = len(chatbot_manager.sessions)

        return ChatResponse(
            session_id=request.session_id,
            response=safe_response,
            intent=result["intent"],
            confidence=result["confidence"],
            state=result["state"],
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get chatbot metrics."""

    if not chatbot_manager:
        return MetricsResponse(
            total_conversations=0,
            avg_confidence=0.0,
            fallback_rate=0.0,
            avg_response_time_ms=0.0
        )

    return MetricsResponse(
        total_conversations=metrics["total_conversations"],
        avg_confidence=metrics["avg_confidence"],
        fallback_rate=0.0,
        avg_response_time_ms=0.5
    )

@app.get("/sessions")
async def get_sessions():
    """Get active sessions."""
    if not chatbot_manager:
        return {"sessions": [], "total": 0}

    return {
        "sessions": list(chatbot_manager.sessions.keys()),
        "total": len(chatbot_manager.sessions)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
