"""Fixtures for tests_api."""

import pytest
import pytest_asyncio


# Synchronous fixtures
@pytest.fixture(scope="function")
def test_client():
    """Get the test client."""
    from app.main import app
    from fastapi.testclient import TestClient

    return TestClient(app)


@pytest.fixture(scope="function")
def authenticated_test_client(test_client, user_instance):
    """Get the test client with an authenticated user."""
    token = user_instance.create_access_token()
    test_client.headers.update({"Authorization": f"Bearer {token}"})
    return test_client


# Asynchronous fixtures
@pytest_asyncio.fixture(scope="function")
async def async_test_client():
    """Get the async test client."""
    from app.main import app
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_authenticated_test_client(async_test_client, async_user_instance):
    """Get the async test client with an authenticated user."""
    token = async_user_instance.create_access_token()
    async_test_client.headers.update({"Authorization": f"Bearer {token}"})
    return async_test_client
