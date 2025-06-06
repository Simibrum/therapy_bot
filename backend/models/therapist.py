"""Class model for a therapist."""

from database import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Therapist(Base):
    __tablename__ = "therapists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    residence: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="therapist")
    chats = relationship("Chat", back_populates="therapist")
    therapy_sessions = relationship("TherapySession", back_populates="therapist")
