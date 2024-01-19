"""Tests on the therapy session logic module using live requests to the OpenAI API."""
from unittest.mock import patch

import numpy as np
import pytest

from logic.therapy_session_logic import TherapySessionLogic
from models.chats import Chat
from tests import custom_chat_completion as custom_create


@pytest.fixture
def therapy_session_logic_instance(user_instance, therapist_instance):
    """Generate a therapy session logic instance."""
    return TherapySessionLogic(user_instance.id, therapist_instance.id)


def test_generate_response(therapy_session_logic_instance, db_session_manager):
    """Test generating a response."""
    # Use the custom create function to use the gpt3.5 model
    with patch('llm.common.chat_completion_wrapper', custom_create):
        chat_list_out = therapy_session_logic_instance.generate_response("Hello, therapist!")
        assert chat_list_out
        chat_out = chat_list_out.messages[0]
        assert len(chat_out.text) > 5
        assert isinstance(chat_out.text, str)
        with db_session_manager.get_session() as session:
            chat = session.query(Chat).filter(Chat.id == chat_out.id).first()
            assert chat is not None
            assert chat.sender == "therapist"
            assert chat.text
            assert chat.vector is not None
            # Check the length of the vector is 300 with at least one non-0 value
            assert len(chat.vector) == 1536
            assert np.any(chat.vector != 0)
