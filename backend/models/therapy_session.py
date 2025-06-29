"""Model for a therapy session."""

from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship


class TherapySession(Base):
    __tablename__ = "therapy_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    therapist_id = Column(Integer, ForeignKey("therapists.id"), nullable=False)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="therapy_sessions")
    therapist = relationship("Therapist", back_populates="therapy_sessions")
    chats = relationship("Chat", back_populates="therapy_session")
