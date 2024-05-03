"""Model for the chat_reference table."""
from __future__ import annotations

from typing import TYPE_CHECKING

from database import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.chat import Chat
    from models.graph.node import Node


class ChatReference(Base):
    """Association object to link chats and nodes.

    See: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object
    """

    __tablename__ = "chat_references"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), nullable=False)

    character_idx_start: Mapped[int] = mapped_column(Integer, nullable=True)
    character_idx_end: Mapped[int] = mapped_column(Integer, nullable=True)

    span_idx_start: Mapped[int] = mapped_column(Integer, nullable=True)
    span_idx_end: Mapped[int] = mapped_column(Integer, nullable=True)

    sentence_idx: Mapped[int] = mapped_column(Integer, nullable=True)
    doc_index: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    # Relationships
    chat: Mapped[Chat] = relationship(back_populates="nodes")
    node: Mapped[Node] = relationship(back_populates="chats")
