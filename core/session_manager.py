from typing import Dict, Optional

class SessionManager:
    """Manage user sessions."""

    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id: str, user_id: Optional[str] = None) -> Dict:
        """Create new session."""
        self.sessions[session_id] = {
            "user_id": user_id,
            "context": {},
        }
        return self.sessions[session_id]

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session."""
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        """Delete session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
