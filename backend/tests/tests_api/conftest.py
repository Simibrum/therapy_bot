"""Fixtures for tests_api."""

import pytest


@pytest.fixture()
def test_client():
    """Get the test client."""
    from app.main import app
    from fastapi.testclient import TestClient

    return TestClient(app)


@pytest.fixture()
def authenticated_test_client(test_client, user_instance):
    """Get the test client with an authenticated user."""
    token = user_instance.create_access_token()
    test_client.headers.update({"Authorization": f"Bearer {token}"})
    return test_client
