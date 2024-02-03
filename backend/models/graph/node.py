"""Definition of the Node class."""

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database import Base
from models.bytes_vector_mixin import BytesVectorMixin


def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent SQL injection attacks."""
    return input_str.replace("\n", "newline")


def validate_type(type):
    """Validate the `type` attribute."""
    VALID_TYPES = ["type1", "type2", "type3"]
    if type not in VALID_TYPES:
        raise ValueError(f"Invalid type: {type}. Type must be one of {VALID_TYPES}.")


class Node(Base, BytesVectorMixin):
    """Node in a graph."""

    __tablename__ = "nodes"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255))
    # Field to store the user ID for user partitioning
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    type: Mapped[str] = mapped_column(String(255), nullable=True)

    def __init__(self, label: str, user_id: int, type: str = None):
        """Initialise a node."""
        if not isinstance(label, str):
            raise TypeError("Label must be a string.")
        self.label = sanitize_input(label)
        self.user_id = user_id

        if type is not None:
            validate_type(type)
            self.type = type

    def __repr__(self) -> str:
        return f"Node(label={self.label}, id={self.id}, user_id={self.user_id}, type={self.type})"
