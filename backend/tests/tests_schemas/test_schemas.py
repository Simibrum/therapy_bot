"""Test schema objects."""
import pytest
import datetime
from app.schemas.pydantic_chats import ChatOut, ChatListOut


@pytest.fixture
def chat_out_instance():
    """Fixture to create a ChatOut instance."""
    return ChatOut(
        id=1,
        therapy_session_id=1,
        user_id=1,
        therapist_id=None,
        message="Hello!",
        sender="user",
        timestamp=datetime.datetime(2023, 11, 3, 10, 0, 0)
    )


@pytest.fixture
def chat_list_out_instance(chat_out_instance):
    """Fixture to create a ChatListOut instance."""
    return ChatListOut(chats=[chat_out_instance, chat_out_instance])


def test_chat_out_as_string(chat_out_instance):
    """Test the as_string method of ChatOut."""
    expected_string = "user: Hello!\n(2023-11-03 10:00:00)"
    assert chat_out_instance.as_string() == expected_string


def test_chat_list_out_as_string(chat_list_out_instance):
    """Test the as_string method of ChatListOut."""
    expected_string = "user: Hello!\n(2023-11-03 10:00:00)\n\nuser: Hello!\n(2023-11-03 10:00:00)"
    assert chat_list_out_instance.as_string() == expected_string
