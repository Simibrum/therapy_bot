"""Code for backend API."""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from starlette.websockets import WebSocketState
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from config import logger
from app.routes.login import router as login_router

app = FastAPI()

executor = ThreadPoolExecutor()

# Add the login router
app.include_router(login_router)


def slow_function(query: str) -> str:
    import time
    time.sleep(0.25)  # Simulate slow logic
    return "test_output"


async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received data: {data}")
            query_data = json.loads(data)  # Assume you're receiving JSON and it contains a 'query' field
            query = query_data.get('query')
            logger.debug(f"Received query: {query}")

            # Prepare preliminary response
            response = {
                "query": query,
                "result": None,
                "state": "PROCESSING"
            }
            logger.debug(f"Sending initial response: {response}")
            await websocket.send_json(response)

            # Run the slow function asynchronously
            task = asyncio.create_task(run_in_executor(slow_function, query))

            # Wait for it to complete and get the result
            result = await task

            logger.info(f"Sending final response: {result}")

            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    finally:
        if websocket.application_state == WebSocketState.CONNECTED \
                and websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

