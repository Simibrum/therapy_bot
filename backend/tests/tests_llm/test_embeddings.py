"""Test embedding functions."""
from llm.embeddings import get_embedding


def test_get_embedding(mocker):
    # Mock the Embedding.create API call
    mock_response = {
        'data': {"embedding": [0.1, 0.2, 0.3]},
    }
    mocker.patch('openai.Embedding.create', return_value=mock_response)

    # Call the get_embedding function
    embedding = get_embedding("Some text")

    # Check the result
    assert embedding == [0.1, 0.2, 0.3]
