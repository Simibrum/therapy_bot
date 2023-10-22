"""Class model for chats between a user and a therapist."""
import datetime

import numpy as np
from sqlalchemy import ForeignKey, Integer, String, DateTime, func, LargeBinary
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, mapped_column, Mapped
from database import Base
from crypto_utils import encrypt_string, decrypt_string
from config import logger
from llm.embeddings import get_embedding


class Chat(Base):
    __tablename__ = 'chats'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    therapist_id: Mapped[int] = mapped_column(ForeignKey('therapists.id'), nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    # Sender is "user" or "therapist"
    sender: Mapped[str] = mapped_column(String(10), nullable=False)
    # This is the text of the chat, to be encrypted with the user's encryption key as below
    _encrypted_text: Mapped[str] = mapped_column(String, nullable=True)
    # Vector of the text - store this as bytes - implement a loader separately
    _vector: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    # Relationships
    user = relationship("User", back_populates="chats")
    therapist = relationship("Therapist", back_populates="chats")

    @hybrid_property
    def text(self) -> str:
        """
        Decrypts and returns the stored text.

        Returns:
            str: The decrypted string.
        """
        if self._encrypted_text:
            plaintext = decrypt_string(self.user.encryption_key.encode(), self._encrypted_text)
            return plaintext
        return ""

    @text.setter
    def text(self, plaintext: str) -> None:
        """
        Encrypts and stores the given plaintext string.

        Parameters:
            plaintext (str): The string to be encrypted.
        """
        self._encrypted_text = encrypt_string(self.user.encryption_key.encode(), plaintext)

    @hybrid_property
    def vector(self) -> np.array:
        """Convert the bytes vector into a numpy array."""
        if self._vector is None:
            return None
        # Convert to numpy array
        return np.frombuffer(self._vector)

    @vector.setter
    def vector(self, vector: np.array) -> None:
        """Convert the numpy array into a bytes vector."""
        if vector is None:
            self._vector = b""
        else:
            # Convert to bytes
            self._vector = vector.tobytes()

    def fetch_text_vector(self):
        """Fetch the embedding for the text."""
        logger.debug(f"Fetching embedding for chat {self.id}")
        if self._encrypted_text:
            self._vector = get_embedding(self.text)
