"""Pydantic models for chats."""
from __future__ import annotations

import datetime

from pydantic import BaseModel, ConfigDict


class ChatOut(BaseModel):
    """Pydantic schema for the chat model."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    therapy_session_id: int
    user_id: int | None = None
    therapist_id: int | None = None
    text: str
    sender: str
    timestamp: datetime.datetime

    def as_string(self) -> str:
        """Return the Chat output as a string."""
        return f"{self.sender}: {self.text}\n({self.timestamp})"


class ChatListOut(BaseModel):
    """Wrapper for list of chats."""

    messages: list[ChatOut]

    def as_string(self) -> str:
        """Return all chats as a string."""
        return "\n\n".join([chat.as_string() for chat in self.messages])


ChatOut.model_rebuild()
ChatListOut.model_rebuild()
