"""Model to define an event in the knowledge graph."""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped

from models.chats_mixin import HasChatReferences
from models.knowledge.common import Common


class Event(Common, HasChatReferences):
    __tablename__ = "events"
    # Event-specific fields
    date: Mapped[datetime] = mapped_column(DateTime)
