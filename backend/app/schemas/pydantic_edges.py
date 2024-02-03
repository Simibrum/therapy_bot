"""Definition of Pydantic object corresponding to the Edge model."""

from typing import Optional

from pydantic import BaseModel


class EdgeOut(BaseModel):
    """Edge in a graph."""
    id: int
    user_id: int
    from_node_id: int
    to_node_id: int
    type: Optional[str] = None
    description: Optional[str] = None
    vector: Optional[list[float]] = None
