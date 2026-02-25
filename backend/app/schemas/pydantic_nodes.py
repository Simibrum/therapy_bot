"""Definition of Pydantic object corresponding to the Node model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class NodeOut(BaseModel):
    """Node in a graph."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    user_id: int
    type: str | None = None
    vector: list[float] | None = None
