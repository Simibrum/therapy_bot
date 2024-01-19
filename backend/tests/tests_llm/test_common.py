"""Tests for common llm functions."""

from unittest.mock import patch

from llm.common import api_request  # Import your function from your actual module


# Mocking the necessary methods and classes
@patch("llm.common.chat_completion_wrapper")
def test_api_request(mock_chat_completion, monkeypatch, mocked_embedding_client):
    """Test the api_request function."""
    # Mocking the chat_completion_wrapper response for other models
    mock_chat_completion.return_value = "Some value"

    # Testing text-embedding model case
    text_embedding_model = "text-embedding-1234"
    response = api_request(text=["some text"], model=text_embedding_model)
    assert response == [0.1, 0.2, 0.3]
    mocked_embedding_client.embeddings.create.assert_called_once()
    mock_chat_completion.assert_not_called()

    # Resetting mocks for next test
    mocked_embedding_client.reset_mock()
    mock_chat_completion.reset_mock()

    # Testing other model case
    other_model = "gpt-3.5-turbo"
    response = api_request(messages=[{"role": "system", "content": "You are a helpful assistant."}], model=other_model)
    assert response == "Some value"
    mock_chat_completion.assert_called_once()
    mocked_embedding_client.embeddings.create.assert_not_called()

# Usage
# Save this test in a file named test_your_module.py
# Run the test using the command: pytest test_your_module.py
