"""Tests on the therapy session logic module using live requests to the OpenAI API."""
import pytest
from unittest.mock import patch
import numpy as np

from tests import custom_create
from logic.therapy_session_logic import TherapySessionLogic
from models.chats import Chat


@pytest.fixture
def therapy_session_logic_instance(user_instance, therapist_instance):
    """Generate a therapy session logic instance."""
    return TherapySessionLogic(user_instance.id, therapist_instance.id)


def test_generate_response(therapy_session_logic_instance, db_session_manager):
    """Test generating a response."""
    # Use the custom create function to use the gpt3.5 model
    with patch('llm.common.chat_completion_wrapper', custom_create):
        new_chat_id, response = therapy_session_logic_instance.generate_response("Hello, therapist!")
        assert response
        assert len(response) > 5
        assert isinstance(response, str)
        with db_session_manager.get_session() as session:
            chat = session.query(Chat).filter(Chat.id == new_chat_id).first()
            assert chat is not None
            assert chat.sender == "therapist"
            assert chat.text == response
            assert chat.vector is not None
            # Check the length of the vector is 300 with at least one non-0 value
            assert len(chat.vector) == 1536
            assert np.any(chat.vector != 0)
