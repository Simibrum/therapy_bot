"""Tests for common llm functions."""

import pytest
from unittest.mock import MagicMock, patch
from llm.common import api_request  # Import your function from your actual module


# Mocking the necessary methods and classes
@patch("openai.Embedding.create")
@patch("llm.common.chat_completion_wrapper")
def test_api_request(mock_chat_completion, mock_openai, monkeypatch):
    # Mocking the openai response for text-embedding model
    mock_openai.return_value = {"data": [{"embedding": [[0.1, 0.2], [0.3, 0.4]]}]}
    # Mocking the chat_completion_wrapper response for other models
    mock_chat_completion.return_value = {"some_key": "some_value"}

    # Testing text-embedding model case
    text_embedding_model = "text-embedding-1234"
    response = api_request(text=["some text"], model=text_embedding_model)
    assert response == [[0.1, 0.2], [0.3, 0.4]]
    mock_openai.assert_called_once()
    mock_chat_completion.assert_not_called()

    # Resetting mocks for next test
    mock_openai.reset_mock()
    mock_chat_completion.reset_mock()

    # Testing other model case
    other_model = "gpt-3.5-turbo"
    response = api_request(messages=[{"role": "system", "content": "You are a helpful assistant."}], model=other_model)
    assert response == {"some_key": "some_value"}
    mock_chat_completion.assert_called_once()
    mock_openai.assert_not_called()

# Usage
# Save this test in a file named test_your_module.py
# Run the test using the command: pytest test_your_module.py
