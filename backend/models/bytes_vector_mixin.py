"""Defines a mixin for models that have a bytes vector field."""
import numpy as np
from sqlalchemy import LargeBinary
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from config import logger


class BytesVectorMixin:
    """Abstract class to store a vector as bytes."""

    __abstract__ = True

    # This is the vector of the text - store this as bytes - implement a loader separately
    _vector: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    @property
    def is_vectorised(self) -> bool:
        """Check if the object has a vector."""
        return self._vector is not None and len(self._vector) > 0

    @hybrid_property
    def vector(self) -> np.array:
        """Convert the bytes vector into a numpy array."""
        if self._vector is None:
            return None
        if len(self._vector) == 0:
            return None
        # Convert to numpy array
        return np.frombuffer(self._vector)

    @vector.setter
    def vector(self, vector: np.array) -> None:
        """Convert the numpy array into a bytes vector."""
        if vector is None:
            self._vector = b""
        else:
            # Validate the vector - must be a numpy array
            if not isinstance(vector, np.ndarray):
                raise TypeError(f"Vector must be a numpy array, not {type(vector)}.")
            # Validate the vector - must be 1D
            if len(vector.shape) != 1:
                raise ValueError(f"Vector must be 1D, not {len(vector.shape)}D.")
            # Validate the vector - elements should be floats or ints
            if not np.issubdtype(vector.dtype, np.number):
                raise ValueError(f"Vector elements must be numbers, not {vector.dtype}.")
            # If entries are ints convert to floats
            if np.issubdtype(vector.dtype, np.integer):
                vector = vector.astype(float)
            # Convert to bytes
            self._vector = vector.tobytes()

    def fetch_text_vector(self) -> np.array:
        """Fetch the embedding for the text."""
        logger.debug(f"Fetching embedding for object {self.__class__} {self.id}")
        raise NotImplementedError
