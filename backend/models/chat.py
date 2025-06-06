"""Class model for chats between a user and a therapist."""
import datetime

import numpy as np
from config import logger
from database import Base
from llm.embeddings import get_embedding
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.text_crypto import decrypt_string, encrypt_string

from models.bytes_vector_mixin import BytesVectorMixin


class Chat(Base, BytesVectorMixin):
    """Class model for chats between a user and a therapist."""

    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Links to other tables
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    therapist_id: Mapped[int] = mapped_column(ForeignKey("therapists.id"), nullable=False)
    therapy_session_id: Mapped[int] = mapped_column(ForeignKey("therapy_sessions.id"), nullable=False)
    # Fields
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    # Sender is "user" or "therapist"
    sender: Mapped[str] = mapped_column(String(10), nullable=False)
    # This is the text of the chat, to be encrypted with the user's encryption key as below
    _encrypted_text: Mapped[str] = mapped_column(String, nullable=True)
    # Vector field provided by BytesVectorMixin as _vector

    # Relationships
    user = relationship("User", back_populates="chats")
    therapist = relationship("Therapist", back_populates="chats")
    therapy_session = relationship("TherapySession", back_populates="chats")
    nodes = relationship("ChatReference", back_populates="chat")

    @hybrid_property
    def text(self) -> str:
        """
        Decrypts and returns the stored text.

        Returns
        -------
            str: The decrypted string.

        """
        if self._encrypted_text:
            return decrypt_string(self.user.encryption_key.encode(), self._encrypted_text)
        return ""

    @text.setter
    def text(self, plaintext: str) -> None:
        """
        Encrypts and stores the given plaintext string.

        Parameters
        ----------
            plaintext (str): The string to be encrypted.

        """
        self._encrypted_text = encrypt_string(self.user.encryption_key.encode(), plaintext)

    def fetch_text_vector(self) -> np.array:
        """Fetch the embedding for the text."""
        logger.debug(f"Fetching embedding for chat {self.id}")
        if self._encrypted_text:
            self.vector = get_embedding(self.text)
        else:
            self.vector = None
        return self.vector
