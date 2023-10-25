"""Therapy session class to model a therapy session."""
from typing import Tuple
import numpy as np
from models.chats import Chat
from database.db_engine import DBSessionManager
from llm.chat_completion import get_chat_completion


class TherapySession:
    def __init__(self, user, therapist):
        self.user = user
        self.therapist = therapist
        self.chat_vectors = None  # Numpy matrix to store chat vectors
        self.index_to_id = {}  # Dictionary to map chat matrix index to chat id
        self.db_session_manager = DBSessionManager()

    def load_previous_chats(self):
        """Load previous chats from the database and their vectors into memory."""
        with self.db_session_manager.get_session() as session:
            previous_chats = (
                session.query(Chat)
                .filter(
                    (Chat.user_id == self.user.id)
                    & (Chat.therapist_id == self.therapist.id)
                )
                .order_by(Chat.timestamp.asc())
                .all()
            )
            self.chat_vectors = np.vstack(
                [chat.vector for chat in previous_chats if chat.vector is not None]
            )
            self.index_to_id = {
                index: chat.id for index, chat in enumerate(previous_chats)
            }

    def add_chat_message(self, sender, text) -> int:
        """Add a new chat message to the history and update the vector matrix."""
        with self.db_session_manager.get_session() as session:
            new_chat = Chat(
                user_id=self.user.id,
                therapist_id=self.therapist.id,
                sender=sender
            )
            session.add(new_chat)
            session.commit()
            # Need to add then refresh such that the user relation works
            session.refresh(new_chat)
            # Text needs to be added separately as it employs a setter for encryption
            new_chat.text = text
            new_chat.fetch_text_vector()
            # Commit to save text and vector
            session.commit()
            if new_chat.id not in self.index_to_id.values():
                self.index_to_id[len(self.index_to_id)] = new_chat.id
                # Add to chat vector stack
                self.chat_vectors = np.vstack(
                    (self.chat_vectors, new_chat.vector)
                ) if self.chat_vectors is not None else new_chat.vector
            return new_chat.id

    def generate_response(self, user_input) -> Tuple[int, str]:
        """Generate a response using the ChatCompletion API."""
        response = get_chat_completion(user_input, self.chat_vectors)
        new_chat_id = self.add_chat_message("therapist", response)
        return new_chat_id, response

    def cosine_similarity_search(self, query_vector):
        """Perform a cosine similarity search on the chat vectors."""
        if self.chat_vectors is None:
            self.load_previous_chats()
        if self.chat_vectors is None:
            return []
        similarity_scores = (
            self.chat_vectors @ query_vector
        ) / (np.linalg.norm(self.chat_vectors, axis=1) * np.linalg.norm(query_vector))
        return similarity_scores

    def get_relevant_past_chat_ids(self, user_input_vector, threshold: int = 0.75):
        """Fetch relevant past chats based on cosine similarity."""
        similarity_scores = self.cosine_similarity_search(user_input_vector)
        relevant_chat_ids = []
        for index, score in enumerate(similarity_scores):
            if score > threshold:
                relevant_chat_ids.append((self.index_to_id[index], score))
        return relevant_chat_ids

# Usage
# Assume user_instance and therapist_instance are SQLAlchemy model instances
# therapy_session = TherapySession(user_instance, therapist_instance)
# therapy_session.load_previous_chats()
# ...
