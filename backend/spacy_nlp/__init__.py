"""Initialize the spacy_nlp package."""

import spacy
from config import SPACY_MODEL, USE_GPU, logger
from spacy.language import Language


def configure_pipeline(nlp: Language) -> Language:
    """Configure the spacy pipeline for the patent NLP model."""
    # All these need to be after the dependency parse
    logger.debug("Configuring NLP Pipeline and Custom Properties")
    return nlp


def load_model() -> Language:
    """Load the spacy model and configure the pipeline."""
    try:
        logger.info(f"Loading Spacy Model {SPACY_MODEL}")
        if USE_GPU:
            logger.info(f"GPU Use Flag: {USE_GPU} - Using GPU")
            try:
                spacy.require_gpu()
            except ValueError as e:
                logger.warning(e)
                logger.warning("Error: GPU Not Available")
        else:
            logger.info(f"GPU Use Flag: {USE_GPU} - GPU Off")
        nlp = spacy.load(SPACY_MODEL)
    except OSError as e:
        logger.warning(e)
        logger.warning("Spacy Model Load Error")
        nlp = spacy.load("en_core_web_sm")
    # Add custom components to the pipeline
    return configure_pipeline(nlp)


class NLPService:
    """Service class to wrap the nlp object that consumes GPU resource."""

    nlp = None

    def get_nlp(self) -> Language:
        """Get the nlp object."""
        if self.nlp is None:
            self.nlp = load_model()
        return self.nlp


nlp_service = NLPService()
