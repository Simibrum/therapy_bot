"""Test therapy session API endpoints."""


def test_new_session_unauthenticated(test_client, user_instance):
    """Test generating a new therapy session."""
    # Try without authentication
    response = test_client.post("/sessions/new")
    assert response.status_code == 401


def test_new_session_authenticated(authenticated_test_client, therapist_instance, user_instance):
    """Test generating a new therapy session."""
    # Try with authentication
    response = authenticated_test_client.post("/sessions/new")
    assert response.status_code == 200
    assert response.json()["session_id"]


def test_get_sessions_unauthenticated(test_client, user_instance):
    """Test getting all therapy sessions for logged-in user."""
    # Try without authentication
    response = test_client.get("/sessions")
    assert response.status_code == 401


def test_get_sessions_authenticated(authenticated_test_client, therapy_session_instance):
    """Test getting all therapy sessions for logged-in user."""
    # Try with authentication
    response = authenticated_test_client.get("/sessions")
    assert response.status_code == 200
    assert response.json()["sessions"]
    assert len(response.json()["sessions"]) == 1
    assert response.json()["sessions"][0]["id"] == therapy_session_instance.id
