import numpy as np
import pytest

from backend.llm.embeddings import compute_cosine_similarities


# Generated by CodiumAI


class TestComputeCosineSimilarities:

    #  The function returns the expected cosine similarity value for a valid query embedding and embeddings matrix.
    def test_valid_query_embedding_and_embeddings_matrix(self):
        # I have test_client and user_instance
        query_embedding = np.array([1, 2, 3])
        embeddings_matrix = np.array([[4, 5, 6], [7, 8, 9], [10, 11, 12]])
        expected_result = np.array([32, 50, 68])

        result = compute_cosine_similarities(query_embedding, embeddings_matrix)

        assert np.array_equal(result, expected_result)

    def test_multiple_query_embeddings_and_single_embeddings_matrix(self):
        # I have test_client and user_instance
        query_embeddings = np.array([[1, 2, 3], [4, 5, 6]])
        embeddings_matrix = np.array([[7, 8, 9], [10, 11, 12], [13, 14, 15]])

        with pytest.raises(ValueError):
            result = compute_cosine_similarities(query_embeddings, embeddings_matrix)

    def test_single_query_embedding_and_multiple_embeddings_matrices(self):
        # I have test_client and user_instance
        query_embedding = np.array([1, 2, 3])
        embeddings_matrix = [np.array([[4, 5, 6], [7, 8, 9], [10, 11, 12]]),
                             np.array([[13, 14, 15], [16, 17, 18], [19, 20, 21]])]

        with pytest.raises(TypeError):
            result = compute_cosine_similarities(query_embedding, embeddings_matrix)

    #  The function returns an empty array when given an empty query embedding and embeddings matrix.
    def test_empty_query_embedding_and_embeddings_matrix(self):
        # I have test_client and user_instance
        query_embedding = np.array([])
        embeddings_matrix = np.array([])

        with pytest.raises(ValueError):
            result = compute_cosine_similarities(query_embedding, embeddings_matrix)

    #  The function raises a TypeError when given a query embedding or embeddings matrix that is not a numpy array.
    def test_non_numpy_input(self):
        # I have test_client and user_instance
        query_embedding = [1, 2, 3]
        embeddings_matrix = [[4, 5, 6], [7, 8, 9], [10, 11, 12]]

        with pytest.raises(TypeError):
            compute_cosine_similarities(query_embedding, embeddings_matrix)

    #  The function raises a ValueError when given a query embedding or embeddings matrix with an incorrect shape.
    def test_incorrect_shape_input(self):
        # I have test_client and user_instance
        query_embedding = np.array([1, 2])
        embeddings_matrix = np.array([[4, 5, 6], [7, 8, 9], [10, 11, 12]])

        with pytest.raises(ValueError):
            compute_cosine_similarities(query_embedding, embeddings_matrix)
