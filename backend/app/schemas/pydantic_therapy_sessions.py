"""Pydantic models for therapy sessions."""
from __future__ import annotations

import datetime

from pydantic import BaseModel, ConfigDict


class TherapySessionOut(BaseModel):
    """Output pydantic model for a therapy session."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    therapist_id: int
    start_time: datetime.datetime
    end_time: datetime.datetime | None = None


class TherapySessionListOut(BaseModel):
    """List of TherapySessionOut models."""

    sessions: list[TherapySessionOut]


TherapySessionOut.model_rebuild()
TherapySessionListOut.model_rebuild()
