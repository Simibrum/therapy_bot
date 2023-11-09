"""Test therapy session API endpoints."""


def test_new_session(test_client, authenticated_test_client):
    """Test generating a new therapy session."""
    # Try without authentication
    response = test_client.post("/session/new")
    assert response.status_code == 401
    # Try with authentication
    response = authenticated_test_client.post("/session/new")
    assert response.status_code == 200
    assert response.json()['session_id']


def test_get_sessions(test_client, authenticated_test_client, therapy_session_instance):
    """Test getting all therapy sessions for logged-in user."""
    # Try without authentication
    response = test_client.get("/sessions")
    assert response.status_code == 401
    # Try with authentication
    response = authenticated_test_client.get("/sessions")
    assert response.status_code == 200
    assert response.json()['sessions']
    assert len(response.json()['sessions']) == 1
    assert response.json()['sessions'][0]['id'] == therapy_session_instance.id
