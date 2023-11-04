"""Pydantic schema for the therapists model."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class TherapistOut(BaseModel):
    """Pydantic schema for the therapist model."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    residence: Optional[str] = None
    description: Optional[str] = None
