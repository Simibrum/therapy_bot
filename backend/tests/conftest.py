"""Configuration for testing."""
from __future__ import annotations

import os

import pytest

# Import fixtures
from .fixtures import *


@pytest.fixture(scope="session", autouse=True)
def _setup_testing_environment() -> None:
    """Set up the testing environment."""
    print("Setting up testing environment")
    existing_env = os.environ.get("CONFIG_ENV")
    os.environ["CONFIG_ENV"] = "testing"
    yield  # This will return control to the test function
    if existing_env:
        os.environ["CONFIG_ENV"] = existing_env  # Revert env var in teardown
    print("Tearing down testing environment")
