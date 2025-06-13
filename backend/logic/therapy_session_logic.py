"""Therapy session class to model a therapy session."""
from typing import Optional

import numpy as np
from app.schemas import ChatListOut, ChatOut, TherapistOut, UserOut
from config import logger
from database.db_engine import DBSessionManager
from llm import prompt_builder
from llm.chat_completion import get_chat_completion
from models import Chat, Therapist, TherapySession, User
from spacy_nlp import nlp_service

from logic.process_chat_create_nodes import process_text_and_create_references


# Define exceptions
class TherapySessionDoesNotExistError(Exception):
    """Exception raised when a therapy session does not exist."""


class UserIdMismatchError(Exception):
    """Exception raised when a user id does not match."""


class TherapistIdMismatchError(Exception):
    """Exception raised when a therapist id does not match."""


class TherapistDoesNotExistError(Exception):
    """Exception raised when a therapy session does not exist."""


class TherapySessionLogic:
    def __init__(
        self,
        user_id: Optional[int] = None,
        therapist_id: Optional[int] = None,
        pre_existing_session_id: Optional[int] = None,
        db_session_manager: DBSessionManager = None,
    ) -> None:
        """Initialise the therapy session."""
        self.db_session_manager = db_session_manager or DBSessionManager()
        self.chat_vectors = None
        self.index_to_id = {}
        if pre_existing_session_id:
            logger.debug("Using pre-existing therapy session")
            therapy_session = self.get_therapy_session(pre_existing_session_id)
            if not therapy_session:
                msg = "Therapy session does not exist"
                raise TherapySessionDoesNotExistError(msg)
            if user_id and therapy_session.user_id != user_id:
                msg = "User id does not match"
                raise UserIdMismatchError(msg)
            if therapist_id and therapy_session.therapist_id != therapist_id:
                msg = "Therapist id does not match"
                raise TherapistIdMismatchError(msg)
            self.user_id = therapy_session.user_id
            self.therapist_id = therapy_session.therapist_id
            self.therapy_session_id = pre_existing_session_id
        elif user_id:
            self.user_id = user_id
            if therapist_id:
                self.therapist_id = therapist_id
            else:
                logger.debug("Creating new therapy session with default user therapist")
                self.therapist_id = self.get_therapist_id()
            logger.debug("Creating new therapy session")
            self.therapy_session_id = self.create_therapy_session()
        else:
            msg = "Must provide either a user id or a pre-existing session id"
            raise ValueError(msg)
        self.system_prompt = self.build_system_prompt()
        # Initialise Spacy
        try:
            self.nlp = nlp_service.get_nlp()
        except OSError:
            logger.warning("Could not load NLP service")
            self.nlp = None

    @property
    def first_chat(self) -> bool:
        """Check if this is the first chat in the session."""
        with self.db_session_manager.get_session() as session:
            first_chat = session.query(Chat).filter(Chat.therapy_session_id == self.therapy_session_id).first()
            return first_chat is None

    def get_therapy_session(self, therapy_session_id: Optional[int] = None) -> TherapySession:
        """Check if the therapy session exists in the database."""
        if not therapy_session_id:
            if not self.therapy_session_id:
                msg = "Must provide a therapy session id"
                raise ValueError(msg)
            therapy_session_id = self.therapy_session_id
        with self.db_session_manager.get_session() as session:
            return session.query(TherapySession).filter(TherapySession.id == therapy_session_id).first()

    def create_therapy_session(self):
        """Create a new therapy session."""
        with self.db_session_manager.get_session() as session:
            new_therapy_session = TherapySession(user_id=self.user_id, therapist_id=self.therapist_id)
            session.add(new_therapy_session)
            session.commit()
            session.refresh(new_therapy_session)
            return new_therapy_session.id

    def get_therapist_id(self) -> Optional[int]:
        """Get the therapist id."""
        with self.db_session_manager.get_session() as session:
            therapist = session.query(Therapist).filter(Therapist.user_id == self.user_id).first()
            if not therapist:
                msg = "Therapist does not exist"
                raise TherapistDoesNotExistError(msg)
            return therapist.id

    def load_all_session_previous_chats(self) -> None:
        """Load previous chats from the database and their vectors into memory."""
        with self.db_session_manager.get_session() as session:
            previous_chats = (
                session.query(Chat)
                .filter((Chat.user_id == self.user_id) & (Chat.therapist_id == self.therapist_id))
                .order_by(Chat.timestamp.asc())
                .all()
            )
            self.chat_vectors = np.vstack([chat.vector for chat in previous_chats if chat.vector is not None])
            self.index_to_id = {index: chat.id for index, chat in enumerate(previous_chats)}

    def add_chat_message(self, sender, text) -> ChatOut:
        """Add a new chat message to the history and update the vector matrix."""
        with self.db_session_manager.get_session() as session:
            new_chat = Chat(
                user_id=self.user_id,
                therapist_id=self.therapist_id,
                sender=sender,
                therapy_session_id=self.therapy_session_id,
            )
            session.add(new_chat)
            session.commit()
            # Need to add then refresh such that the user relation works
            session.refresh(new_chat)
            # Text needs to be added separately as it employs a setter for encryption
            new_chat.text = text
            # TODO - split here to return message first?
            new_chat.fetch_text_vector()
            # Commit to save text and vector
            session.commit()
            # NEW: Extract entities only from user messages
            if sender == "user" and self.nlp is not None:
                try:
                    process_text_and_create_references(
                        text=text, chat_id=new_chat.id, user_id=self.user_id, db=session, nlp=self.nlp
                    )
                except Exception as e:
                    logger.error(f"Entity extraction failed: {e}")
                    # Don't let entity extraction break the chat flow
            chat_out = ChatOut.model_validate(new_chat)
            if new_chat.id not in self.index_to_id.values():
                self.index_to_id[len(self.index_to_id)] = new_chat.id
                # Add to chat vector stack
                self.chat_vectors = (
                    np.vstack((self.chat_vectors, new_chat.vector))
                    if self.chat_vectors is not None
                    else new_chat.vector
                )
            return chat_out

    def cosine_similarity_search(self, query_vector):
        """Perform a cosine similarity search on the chat vectors."""
        if self.chat_vectors is None:
            self.load_all_session_previous_chats()
        if self.chat_vectors is None:
            return []
        return (self.chat_vectors @ query_vector) / (
            np.linalg.norm(self.chat_vectors, axis=1) * np.linalg.norm(query_vector)
        )

    def get_relevant_past_chat_ids(self, user_input_vector, threshold: int = 0.75):
        """Fetch relevant past chats based on cosine similarity."""
        similarity_scores = self.cosine_similarity_search(user_input_vector)
        relevant_chat_ids = []
        for index, score in enumerate(similarity_scores):
            if score > threshold:
                relevant_chat_ids.append((self.index_to_id[index], score))
        return relevant_chat_ids

    def build_system_prompt(self):
        """Build the system prompt."""
        with self.db_session_manager.get_session() as session:
            user = session.query(User).filter(User.id == self.user_id).first()
            therapist = session.query(Therapist).filter(Therapist.id == self.therapist_id).first()
            user_out = UserOut.model_validate(user)
            therapist_out = TherapistOut.model_validate(therapist)
        return prompt_builder.build_system_prompt(user_out, therapist_out)

    def get_therapy_session_messages(self) -> ChatListOut:
        """Get all messages in the therapy session."""
        with self.db_session_manager.get_session() as session:
            messages = session.query(Chat).filter(Chat.therapy_session_id == self.therapy_session_id).all()
            return ChatListOut(messages=messages)

    def start_session(self) -> ChatListOut:
        """Start a new therapy session and return initial messages."""
        # Build briefing messages for first session
        briefing_messages = [
            prompt_builder.build_new_session_prompt(),
        ]
        first_message = prompt_builder.build_first_message_prompt()
        # Get the first message from the therapist
        response = get_chat_completion(first_message, self.system_prompt, briefing_messages=briefing_messages)
        self.add_chat_message("therapist", response)
        return self.get_therapy_session_messages()

    def generate_response(self, user_input) -> ChatListOut:
        """Generate a response using the ChatCompletion API."""
        # Get the history
        history = prompt_builder.build_recent_session_history(self.get_therapy_session_messages())
        # Add the user input to the chat history
        self.add_chat_message("user", user_input)
        next_message_prompt = prompt_builder.build_next_message_prompt(user_input)
        # This needs to use the history to prevent "Hello [User]" being repeated
        response = get_chat_completion(next_message_prompt, self.system_prompt, history=history)
        chat_out = self.add_chat_message("therapist", response)
        return ChatListOut(messages=[chat_out])

    def get_messages(self) -> ChatListOut:
        """Get existing messages or start a new session."""
        if self.first_chat:
            return self.start_session()
        else:
            return self.get_therapy_session_messages()
