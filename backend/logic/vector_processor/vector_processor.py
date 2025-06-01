"""Provide vector processing functionality."""
import numpy as np

from models import Chat

class VectorProcessor:
    """Class to handle vector processing."""

    def __init__(self):
        self.chat_vectors = None
        self.index_to_id = {}

    async def process_chat_vector(self, chat: Chat):
        if chat.id not in self.index_to_id.values():
            self.index_to_id[len(self.index_to_id)] = chat.id
            self.chat_vectors = (
                np.vstack((self.chat_vectors, chat.vector))
                if self.chat_vectors is not None
                else chat.vector
            )

    async def get_relevant_chats(self, query_vector, threshold: float = 0.75):
# Implementation (unchanged)
