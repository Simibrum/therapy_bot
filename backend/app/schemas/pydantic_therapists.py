"""Pydantic schema for the therapists model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TherapistOut(BaseModel):
    """Pydantic schema for the therapist model."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    residence: str | None = None
    description: str | None = None
