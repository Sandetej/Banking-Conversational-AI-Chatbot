from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session ID")
    message: str = Field(..., description="User message")
    stream: bool = Field(default=False, description="Stream response?")

class ChatResponse(BaseModel):
    session_id: str
    response: str
    intent: str
    confidence: float
    state: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

class MetricsResponse(BaseModel):
    total_conversations: int
    avg_confidence: float
    fallback_rate: float
    avg_response_time_ms: float
