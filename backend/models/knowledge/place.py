"""Model to define a place in the knowledge graph."""


from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from models.common import LocationMixin
from models.knowledge.common import Common


class Place(Common, LocationMixin):
    """Model to define a place in the knowledge graph."""

    __tablename__ = "places"

    # Place-specific fields
    latitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)  # Up to 6 decimal places of precision
    longitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)  # Up to 6 decimal places of precision
    elevation: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)  # Up to 6 decimal places of precision

    # Address, City, and Country are inherited from LocationMixin
