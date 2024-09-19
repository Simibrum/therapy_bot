"""Module to define nodes in a graph model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.bytes_vector_mixin import BytesVectorMixin

if TYPE_CHECKING:
    from models.chat_reference import ChatReference

VALID_TYPES = [None, "event", "person", "place", "object"]


def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent SQL injection attacks."""
    return input_str.replace("\n", "newline")


def validate_type(node_type: str) -> None:
    """Validate the `type` attribute."""
    if node_type not in VALID_TYPES:
        error_message = f"Invalid type: {node_type}. Type must be one of {VALID_TYPES}."
        raise ValueError(error_message)


class Node(Base, BytesVectorMixin):
    """Node in a graph."""

    __tablename__ = "nodes"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255))
    # Field to store the user ID for user partitioning
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    type: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    chats: Mapped[list[ChatReference]] = relationship(back_populates="node")

    def __init__(self, label: str, user_id: int, node_type: str | None = None) -> None:
        """Initialise a node."""
        if not isinstance(label, str):
            error_message = "Label must be a string."
            raise TypeError(error_message)
        self.label = sanitize_input(label)
        self.user_id = user_id

        if type is not None:
            validate_type(node_type)
            self.type = node_type

    def __repr__(self) -> str:
        """Return a string representation of the node."""
        return f"Node(label={self.label}, id={self.id}, user_id={self.user_id}, type={self.type})"
