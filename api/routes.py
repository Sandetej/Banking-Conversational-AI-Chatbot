from fastapi import APIRouter, HTTPException, Depends
from api.schemas import ChatRequest, ChatResponse, HealthResponse
from datetime import datetime

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint."""
    try:
        # Process message through chatbot
        return ChatResponse(
            session_id=request.session_id,
            response="Response from chatbot",
            intent="balance_inquiry",
            confidence=0.95,
            state="completion",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
