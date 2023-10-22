"""LLM embedding functions."""
from typing import List
import numpy as np
from config import openai_api_key
from llm.common import api_request


def get_embedding(
        text: str,
        model: str = "text-embedding-ada-002",
        api_key: str = openai_api_key
) -> List[List[float]]:
    """
    Get the embedding for a given text using the OpenAI Embedding API.

    Args:
        text: The input text as a list of strings.
        model: The model name or ID to use for embeddings. Default is "text-embedding-ada-002".
        api_key: The OpenAI API key to use for embeddings. Default is the value of the OPENAI_API_KEY environment
            variable.

    Returns:
        A list of embeddings corresponding to the input text, each embedding is a list of floats.
    """
    return api_request(text=text, messages=[], model=model, api_key=api_key)


def compute_cosine_similarities(query_embedding: np.array, embeddings_matrix: np.array):
    """Compute the cosine similarities between a query embedding and a matrix of embeddings."""
    result = np.dot(query_embedding.T, embeddings_matrix.T)
    return result
