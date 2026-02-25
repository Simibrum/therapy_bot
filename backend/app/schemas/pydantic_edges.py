"""Definition of Pydantic object corresponding to the Edge model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class EdgeOut(BaseModel):
    """Edge in a graph."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    from_node_id: int
    to_node_id: int
    type: str | None = None
    description: str | None = None
    vector: list[float] | None = None
