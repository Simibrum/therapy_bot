"""Module contains the Edge model."""

from database import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.bytes_vector_mixin import BytesVectorMixin


class Edge(Base, BytesVectorMixin):
    """Edge in a graph."""

    __tablename__ = "edges"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Field to store the user ID for user partitioning
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Fields to store the node IDs
    from_node_id: Mapped[int] = mapped_column(Integer, ForeignKey("nodes.id"))
    to_node_id: Mapped[int] = mapped_column(Integer, ForeignKey("nodes.id"))

    type: Mapped[str] = mapped_column(String(255))

    description: Mapped[str] = mapped_column(String)

    # Relationships
    from_node = relationship("Node", foreign_keys=[from_node_id])
    to_node = relationship("Node", foreign_keys=[to_node_id])
