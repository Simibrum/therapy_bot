"""Fixtures for tests_api."""

import pytest


@pytest.fixture(scope="session")
def test_client():
    """Get the test client."""
    from app.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)

