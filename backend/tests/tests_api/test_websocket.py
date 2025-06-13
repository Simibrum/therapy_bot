"""Test the websocket API connection."""
import pytest
from app.main import app
from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient

client = TestClient(app)


def test_websocket_auth_connection(therapy_session_instance, user_instance):
    endpoint_string = f"/ws/session/{therapy_session_instance.id}"
    with client.websocket_connect(endpoint_string) as websocket:
        token = user_instance.create_access_token()
        websocket.send_json({"access_token": token})
        response = websocket.receive_text()
        assert response == "Valid token"

        initial_messages = websocket.receive_json()
        assert initial_messages
        assert "messages" in initial_messages
        assert len(initial_messages["messages"]) == 1


def test_websocket_no_auth_connection(therapy_session_instance):
    endpoint_string = f"/ws/session/{therapy_session_instance.id}"
    with client.websocket_connect(endpoint_string) as websocket:
        websocket.send_json({"message": "any old thing"})
        response = websocket.receive_text()
        assert response == "Invalid token"
        # Check websocket is closed
        with pytest.raises(WebSocketDisconnect):
            websocket.receive_text()
