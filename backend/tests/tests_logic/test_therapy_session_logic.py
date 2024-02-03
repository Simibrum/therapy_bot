"""Test the therapy session class."""

import math

import numpy as np
import pytest
from pytest_mock import MockerFixture

from logic.therapy_session_logic import TherapySessionLogic
from models.chats import Chat


def mock_get_embedding(*args, **kwargs):
    # Create a random array of floats
    random_vector = np.random.rand(300)  # Assuming a 300-dimensional vector
    # Normalize the vector to have a unit length
    normalized_vector = random_vector / np.linalg.norm(random_vector)
    return normalized_vector


@pytest.fixture
def therapy_session_instance(user_instance, therapist_instance, mocker: MockerFixture):
    # Mock the OpenAI API embedding function
    mocker.patch("models.chats.get_embedding", side_effect=mock_get_embedding)
    return TherapySessionLogic(user_instance.id, therapist_instance.id)


@pytest.fixture
def chat_instance_with_vector(shared_session, chat_instance):
    """Create a chat instance with a vector."""
    chat_instance.vector = chat_instance.fetch_text_vector()
    shared_session.commit()
    return chat_instance


@pytest.fixture
def therapy_session_instance_with_chat(therapy_session_instance):
    """Create a therapy session instance with a chat."""
    therapy_session_instance.add_chat_message("user", "Hello there, therapist!")
    return therapy_session_instance


def test_add_chat_message(db_session_manager, therapy_session_instance):
    chat_out = therapy_session_instance.add_chat_message("user", "Hello, therapist!")
    with db_session_manager.get_session() as session:
        chat = session.query(Chat).filter(Chat.id == chat_out.id).first()
        assert chat is not None
        assert chat.sender == "user"
        assert chat.text == "Hello, therapist!"
        assert chat.vector is not None
        # Check the length of the vector is 300 with at least one non-0 value
        assert len(chat.vector) == 300
        assert np.any(chat.vector != 0)


def test_generate_response(mocker, therapy_session_instance, db_session_manager):
    mocker.patch(
        "logic.therapy_session_logic.get_chat_completion", return_value="Hello, user!"
    )
    chat_list_out = therapy_session_instance.generate_response("Hello, therapist!")
    chat_out = chat_list_out.messages[0]
    with db_session_manager.get_session() as session:
        chat = session.query(Chat).filter(Chat.id == chat_out.id).first()
        assert chat is not None
        assert chat.sender == "therapist"
        assert chat.text == "Hello, user!"
        assert chat.vector is not None
        # Check the length of the vector is 300 with at least one non-0 value
        assert len(chat.vector) == 300
        assert np.any(chat.vector != 0)


def test_load_previous_chats(therapy_session_instance_with_chat):
    """Test loading previous chats from the database."""
    therapy_session_instance_with_chat.load_all_session_previous_chats()
    assert len(therapy_session_instance_with_chat.chat_vectors) == 1
    assert therapy_session_instance_with_chat.chat_vectors is not None
    # The size of the chat vectors matrix should be 1 x 300
    assert therapy_session_instance_with_chat.chat_vectors.shape == (1, 300)


def test_cosine_similarity_search(therapy_session_instance_with_chat):
    therapy_session_instance_with_chat.load_all_session_previous_chats()
    query_vector = therapy_session_instance_with_chat.chat_vectors[0]
    similarity_scores = therapy_session_instance_with_chat.cosine_similarity_search(
        query_vector
    )
    assert len(similarity_scores) == 1
    assert math.isclose(
        similarity_scores[0], 1.0, rel_tol=1e-4
    )  # Assuming the vector is compared with itself


def test_get_relevant_past_chats(therapy_session_instance_with_chat):
    therapy_session_instance_with_chat.load_all_session_previous_chats()
    query_vector = therapy_session_instance_with_chat.chat_vectors[0]
    relevant_chat_ids = therapy_session_instance_with_chat.get_relevant_past_chat_ids(
        query_vector
    )
    assert len(relevant_chat_ids) == 1
    assert relevant_chat_ids[0][0] == 1
    assert math.isclose(relevant_chat_ids[0][1], 1.0, rel_tol=1e-4)
