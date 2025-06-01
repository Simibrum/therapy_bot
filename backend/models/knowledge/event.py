"""Model to define an event in the knowledge graph."""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.knowledge.common import Common


class Event(Common):
    """Model to define an event in the knowledge graph."""

    __tablename__ = "events"
    # Event-specific fields
    date: Mapped[datetime] = mapped_column(DateTime)
