"""Test the websocket API connection."""
import pytest
import json
import websockets
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from app.main import app

client = TestClient(app)


def test_websocket_auth_connection(therapy_session_instance, user_instance):
    endpoint_string = f"/ws/session/{therapy_session_instance.id}"
    with client.websocket_connect(endpoint_string) as websocket:
        token = user_instance.create_access_token()
        websocket.send_json({"access_token": token})
        response = websocket.receive_text()
        assert response == "Valid token"


def test_websocket_no_auth_connection(therapy_session_instance):
    endpoint_string = f"/ws/session/{therapy_session_instance.id}"
    with client.websocket_connect(endpoint_string) as websocket:
        websocket.send_json({"message": "any old thing"})
        response = websocket.receive_text()
        assert response == "Invalid token"

@pytest.mark.asyncio
async def test_async_websocket_connection(therapy_session_instance):
    endpoint_string = f"/ws/session/{therapy_session_instance.id}"
    async with websockets.connect(endpoint_string) as websocket:
        # Receive the initial data sent back after the connection is established
        initial_data = await websocket.recv()
        # Deserialize the received data to a Python data structure (assuming it's sent as JSON)
        initial_data = json.loads(initial_data)

        # data = {"query": "What is the meaning of life?"}
        # websocket.send_json(data)
        # response = websocket.receive_json()
        # expected_response = {
        #     'query': 'What is the meaning of life?',
        #     'result': None,
        #     'state': 'PROCESSING'
        # }
        # assert response == expected_response

