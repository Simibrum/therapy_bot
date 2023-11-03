"""Model for a therapy session."""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref
from database import Base


class TherapySession(Base):
    __tablename__ = 'therapy_sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    therapist_id = Column(Integer, ForeignKey('therapists.id'), nullable=False)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="therapy_sessions")
    therapist = relationship("Therapist", back_populates="therapy_sessions")
    chats = relationship("Chat", back_populates="therapy_session")
