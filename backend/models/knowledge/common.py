"""Common model for specific node types in the knowledge graph."""

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Common(Base):
    """Model providing common fields for specific node types in the knowledge graph."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    node_id: Mapped[int] = mapped_column(Integer, ForeignKey("nodes.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # node = relationship("Node", foreign_keys=[node_id], backref="associated_entities")

    @declared_attr
    def node(cls):
        return relationship("Node", foreign_keys=[cls.node_id], viewonly=True)
