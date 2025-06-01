"""Test therapy session API endpoints."""
import pytest


@pytest.mark.asyncio()
async def test_new_session_unauthenticated(async_test_client, async_user_instance):
    """Test generating a new therapy session."""
    assert async_user_instance
    # Try without authentication
    response = await async_test_client.post("/sessions/new")
    assert response.status_code == 401


@pytest.mark.asyncio()
async def test_new_session_authenticated(
    async_authenticated_test_client, async_therapist_instance, async_user_instance
):
    """Test generating a new therapy session."""
    assert async_therapist_instance
    assert async_user_instance
    # Try with authentication
    response = await async_authenticated_test_client.post("/sessions/new")
    assert response.status_code == 200
    assert response.json()["session_id"]


@pytest.mark.asyncio()
async def test_get_sessions_unauthenticated(async_test_client, async_user_instance):
    """Test getting all therapy sessions for logged-in user."""
    assert async_user_instance
    # Try without authentication
    response = await async_test_client.get("/sessions")
    assert response.status_code == 401


@pytest.mark.asyncio()
async def test_get_sessions_authenticated(async_authenticated_test_client, async_therapy_session_instance):
    """Test getting all therapy sessions for logged-in user."""
    # Try with authentication
    response = await async_authenticated_test_client.get("/sessions")
    assert response.status_code == 200
    assert response.json()["sessions"]
    assert len(response.json()["sessions"]) == 1
    assert response.json()["sessions"][0]["id"] == async_therapy_session_instance.id
