"""Tests for the chats models."""
from unittest.mock import patch

import numpy as np
from models import Chat, Therapist, User
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker


def test_chat_model(db_setup: Engine, user_instance: User, therapist_instance: Therapist, chat_instance: Chat) -> None:
    """Test the chat model."""
    test_engine = db_setup
    session_factory = sessionmaker(bind=test_engine)
    session = session_factory()

    # Retrieve the chat from the database
    retrieved_chat = session.query(Chat).filter_by(id=chat_instance.id).one()

    assert retrieved_chat.text == "Hello, how are you?"
    assert retrieved_chat.sender == "user"
    assert retrieved_chat.user_id == user_instance.id
    assert retrieved_chat.therapist_id == therapist_instance.id

    # Test vector property
    dummy_vector = np.array([1.0, 2.0, 3.0])
    retrieved_chat.vector = dummy_vector
    session.commit()

    # Ensure vector is saved and retrieved correctly
    assert np.array_equal(retrieved_chat.vector, dummy_vector)

    session.close()


@patch("models.chat.get_embedding", return_value=np.array([0.1, 0.2, 0.3]))
def test_fetch_text_vector(
    mock_get_embedding: MockerFixture,
    db_setup: Engine,
    user_instance: User,
    therapist_instance: Therapist,
    chat_instance: Chat,
) -> None:
    """Test fetching the text vector."""
    assert therapist_instance
    test_engine = db_setup
    session_factory = sessionmaker(bind=test_engine)
    session = session_factory()

    # Retrieve the chat from the database
    retrieved_chat = session.query(Chat).filter_by(id=chat_instance.id).one()

    # Check the user instance is available on chat
    assert retrieved_chat.user.encryption_key == user_instance.encryption_key

    # Check we have encrypted text
    assert retrieved_chat._encrypted_text

    # Call fetch_text_vector
    retrieved_chat.fetch_text_vector()
    session.commit()

    # Ensure get_embedding was called with the correct text
    mock_get_embedding.assert_called_once_with("Hello, how are you?")

    # Ensure vector is updated correctly
    assert np.array_equal(retrieved_chat.vector, np.array([0.1, 0.2, 0.3]))

    session.close()
