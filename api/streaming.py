from fastapi import WebSocket
import json

class StreamingHandler:
    """Handle WebSocket connections for real-time streaming."""

    async def handle_connection(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_json()
                response = await self.process_message(data)
                await websocket.send_json(response)
        except Exception as e:
            await websocket.close(code=1000)

    async def process_message(self, data: dict) -> dict:
        """Process incoming message."""
        return {
            "status": "success",
            "response": "Message received"
        }
