"""Common model for specific node types in the knowledge graph."""

from database import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Common(Base):
    """Model providing common fields for specific node types in the knowledge graph."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    node_id: Mapped[int] = mapped_column(Integer, ForeignKey("nodes.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    @declared_attr
    def node(cls):  # noqa: ANN201, N805 - No return type for declared_attr to avoid error
        """Relationship to the Node model."""
        return relationship("Node", foreign_keys=[cls.node_id], viewonly=True)
