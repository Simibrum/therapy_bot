"""Test the login."""

from fastapi.testclient import TestClient


def test_login(test_client, user_instance):
    """Test the login."""
    response = test_client.post("/login", json={"username": "testuser", "password": "hashedpassword"})
    assert response.status_code == 200
    # Check that an access token is returned
    assert response.json()['access_token']
