"""Custom middleware for FastAPI."""
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from typing import Dict
import time

class RateLimiter:
    """Simple rate limiter middleware."""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}

    async def check_limit(self, request: Request) -> bool:
        client_ip = request.client.host
        now = datetime.now()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Remove old requests (> 1 minute ago)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < timedelta(minutes=1)
        ]

        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        self.requests[client_ip].append(now)
        return True

async def auth_required(request: Request) -> bool:
    """Placeholder authentication middleware."""
    # In production, validate API key, JWT, etc.
    return True

class LoggingMiddleware:
    """Log all requests and responses."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
