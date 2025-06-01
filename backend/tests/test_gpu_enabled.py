"""File to test whether the GPU is enabled and working properly."""

import spacy
from config import USE_GPU, logger


def test_gpu_enabled() -> None:
    """Test whether the GPU is enabled."""
    if USE_GPU:
        logger.info("Testing use of GPU")
        spacy.require_gpu()
    else:
        logger.info("Testing use of CPU")
        spacy.require_cpu()
