"""Class model for chats between a user and a therapist."""
import datetime

import numpy as np
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, mapped_column, Mapped

from config import logger
from database import Base
from llm.embeddings import get_embedding
from models.bytes_vector_mixin import BytesVectorMixin
from utils.text_crypto import encrypt_string, decrypt_string


class Chat(Base, BytesVectorMixin):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    therapist_id: Mapped[int] = mapped_column(
        ForeignKey("therapists.id"), nullable=False
    )
    therapy_session_id: Mapped[int] = mapped_column(
        ForeignKey("therapy_sessions.id"), nullable=False
    )
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    # Sender is "user" or "therapist"
    sender: Mapped[str] = mapped_column(String(10), nullable=False)
    # This is the text of the chat, to be encrypted with the user's encryption key as below
    _encrypted_text: Mapped[str] = mapped_column(String, nullable=True)
    # Vector field provided by BytesVectorMixin as _vector

    # Relationships
    user = relationship("User", back_populates="chats")
    therapist = relationship("Therapist", back_populates="chats")
    therapy_session = relationship("TherapySession", back_populates="chats")

    @hybrid_property
    def text(self) -> str:
        """
        Decrypts and returns the stored text.

        Returns:
            str: The decrypted string.
        """
        if self._encrypted_text:
            plaintext = decrypt_string(
                self.user.encryption_key.encode(), self._encrypted_text
            )
            return plaintext
        return ""

    @text.setter
    def text(self, plaintext: str) -> None:
        """
        Encrypts and stores the given plaintext string.

        Parameters:
            plaintext (str): The string to be encrypted.
        """
        self._encrypted_text = encrypt_string(
            self.user.encryption_key.encode(), plaintext
        )

    def fetch_text_vector(self) -> np.array:
        """Fetch the embedding for the text."""
        logger.debug(f"Fetching embedding for chat {self.id}")
        if self._encrypted_text:
            self.vector = get_embedding(self.text)
        else:
            self.vector = None
        return self.vector
