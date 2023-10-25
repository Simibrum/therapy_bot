from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from app.main import app

client = TestClient(app)


def test_websocket_connection():
    with client.websocket_connect("/ws") as websocket:
        data = {"query": "What is the meaning of life?"}
        websocket.send_json(data)
        response = websocket.receive_json()
        expected_response = {
            'query': 'What is the meaning of life?',
            'result': None,
            'sources': [],
            'state': 'PROCESSING'
        }
        assert response == expected_response

