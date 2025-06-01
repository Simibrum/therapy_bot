"""Definition of Pydantic object corresponding to the Node model."""

from typing import Optional

from pydantic import BaseModel


class NodeOut(BaseModel):
    """Node in a graph."""

    id: int
    label: str
    user_id: int
    type: Optional[str] = None
    vector: Optional[list[float]] = None
