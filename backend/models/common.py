"""File to define shared functions and mixins."""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from zoneinfo import ZoneInfo


class LocationMixin:
    """Contains location data for a user."""

    address: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    # This can be a postal code or ZIP code
    location_code: Mapped[str] = mapped_column(String(255), nullable=True)


class PersonNameMixin:
    """Contains name data for a person."""

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(255), nullable=True)


class LifeDatesMixin:
    """Contains life date data for a person."""

    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    date_of_death: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    @property
    def age(self) -> int:
        """
        Returns the age of the user based on the date of birth.

        Returns
        -------
            int: The age of the user in years.

        """
        if self.date_of_birth:
            today = datetime.now(tz=ZoneInfo("UTC"))
            return (
                today.year
                - self.date_of_birth.year
                - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            )  # Return the age in years
        return -1


class ObjectMixin:
    """Contains object data for a user."""

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    # This can be a barcode or QR code or something else
    code: Mapped[str] = mapped_column(String(255), nullable=True)


class OrganisationMixin:
    """Contains organization-specific data."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=True)  # e.g., "Corporation", "Non-profit", "Government"
    industry: Mapped[str] = mapped_column(String(255), nullable=True)
    founded_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    website: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
