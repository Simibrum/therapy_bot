"""Pydantic models for therapy sessions."""
import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TherapySessionOut(BaseModel):
    """Output pydantic model for a therapy session."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    therapist_id: int
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None


class TherapySessionListOut(BaseModel):
    """List of TherapySessionOut models."""
    sessions: list[TherapySessionOut]
