"""A manager for DB functions relating to therapy sessions."""
from typing import Optional

from models import TherapySession


class DatabaseManager:
    """Class to manage database functions for therapy sessions."""

    async def get_therapy_session(self, session_id: int) -> Optional[TherapySession]:
        """Get a therapy session by ID."""
        # Implementation

    async def create_therapy_session(self, user_id: int, therapist_id: int) -> int:
        """Create a new therapy session."""
        # Implementation
