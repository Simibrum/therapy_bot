"""Fixtures that work for both sync and async tests."""
from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import pytest
from spacy_nlp import NLPService

if TYPE_CHECKING:
    from unittest.mock import AsyncMock, MagicMock, NonCallableMagicMock

    from pytest_mock import MockerFixture
    from spacy import Language


@pytest.fixture()
def mocked_embedding_client(mocker: MockerFixture) -> MagicMock | NonCallableMagicMock | AsyncMock:
    """Mock the embedding client."""

    class EmbeddingResponse(NamedTuple):
        data: list[NamedTuple]

    class EmbeddingData(NamedTuple):
        embedding: list[float]

    # Create an instance of the EmbeddingData named tuple
    embedding_data = EmbeddingData(embedding=[0.1, 0.2, 0.3])

    # Wrap it in the EmbeddingResponse named tuple
    mock_response = EmbeddingResponse(data=[embedding_data])

    mocked_client = mocker.patch("llm.common.client")
    mocked_client.embeddings.create.return_value = mock_response
    return mocked_client


@pytest.fixture()
def mocked_chat_completion(mocker: MockerFixture) -> MagicMock | NonCallableMagicMock | AsyncMock:
    """Mock the chat completion function."""
    # Mock the get_chat_completion function
    return mocker.patch(
        "logic.therapy_session_logic.get_chat_completion",
        return_value="Welcome to your therapy session!",
    )


@pytest.fixture(scope="session")
def test_nlp() -> Language:
    """Create a test spaCy NLP object."""
    return NLPService().get_nlp()
