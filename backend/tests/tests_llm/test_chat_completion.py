"""Tests for the chat completion."""
import pytest
from unittest.mock import Mock
from config import openai_api_key
from llm.chat_completion import get_chat_completion


@pytest.fixture
def mock_api_request(mocker):
    """Fixture to mock the api_request function."""
    mock = mocker.patch('llm.chat_completion.api_request', autospec=True)
    mock.return_value = {"choices": [{"message": {"content": "Hello, how can I help you?"}}]}
    return mock


def test_get_chat_completion_basic(mock_api_request):
    """Test the get_chat_completion function with basic inputs."""
    next_message_prompt = "Tell me a joke."
    system_prompt = "You are a helpful assistant."

    result = get_chat_completion(next_message_prompt, system_prompt)

    # Check the result
    assert result == "Hello, how can I help you?"

    # Check that api_request was called with the expected arguments
    mock_api_request.assert_called_once_with(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a joke."}
        ],
        model="gpt-3.5-turbo",
        temperature=0.3,
        api_key=openai_api_key  # Replace with the actual variable or value for your API key
    )


def test_get_chat_completion_with_history_and_briefing(mock_api_request):
    """Test the get_chat_completion function with history and briefing messages."""
    next_message_prompt = "Tell me a joke."
    system_prompt = "You are a helpful assistant."
    history = "What's your name?"
    briefing_messages = ["Please be funny."]

    result = get_chat_completion(next_message_prompt, system_prompt, history=history,
                                 briefing_messages=briefing_messages)

    # Check the result
    assert result == "Hello, how can I help you?"

    # Check that api_request was called with the expected arguments
    mock_api_request.assert_called_once_with(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's your name?"},
            {"role": "user", "content": "Please be funny."},
            {"role": "user", "content": "Tell me a joke."}
        ],
        model="gpt-3.5-turbo",
        temperature=0.3,
        api_key=openai_api_key  # Replace with the actual variable or value for your API key
    )
