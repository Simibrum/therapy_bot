"""Definition of Pydantic object corresponding to the Node model."""

from __future__ import annotations

from pydantic import BaseModel


class NodeOut(BaseModel):
    """Node in a graph."""

    id: int
    label: str
    user_id: int
    type: str | None = None
    vector: list[float] | None = None
