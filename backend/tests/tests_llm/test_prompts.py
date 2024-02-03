"""Testing out the prompts."""

from app.schemas import UserOut, TherapistOut
from llm.prompt_builder import (
    build_first_message_prompt,
    build_new_session_prompt,
    build_system_prompt,
)


def test_system_prompt(user_instance, therapist_instance):
    """Test building the system prompt."""
    user_out = UserOut.model_validate(user_instance)
    therapist_out = TherapistOut.model_validate(therapist_instance)
    system_prompt = build_system_prompt(user_out, therapist_out)
    assert system_prompt is not None
    assert len(system_prompt) > 0
    assert user_out.first_name in system_prompt
    assert user_out.last_name in system_prompt
    assert user_out.city in system_prompt
    assert user_out.country in system_prompt
    assert str(user_out.age) in system_prompt
    assert therapist_out.first_name in system_prompt
    assert therapist_out.last_name in system_prompt
    assert therapist_out.residence in system_prompt
    assert therapist_out.description in system_prompt


def test_new_session_prompt():
    """Test building the new session prompt."""
    new_session_prompt = build_new_session_prompt()
    assert new_session_prompt is not None
    assert len(new_session_prompt) > 0
    assert "first therapy session" in new_session_prompt


def test_first_message_prompt():
    """Test building the first message prompt."""
    first_message_prompt = build_first_message_prompt()
    assert first_message_prompt is not None
    assert len(first_message_prompt) > 0
    assert "Provide a message" in first_message_prompt
