"""Test embedding functions."""
import numpy as np
from numpy.testing import assert_array_equal

from llm.embeddings import get_embedding


def test_get_embedding(mocked_embedding_client):
    """Test the get_embedding function."""
    # Call the get_embedding function
    embedding = get_embedding("Some text")

    # Check the result
    assert_array_equal(embedding, np.array([0.1, 0.2, 0.3]))
