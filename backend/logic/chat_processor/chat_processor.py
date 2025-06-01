"""Class to maintain a queue that asynchronously processes chat messages."""

import asyncio
from enum import Enum, auto
from typing import Any, Callable, Coroutine, List

from models import Chat


class ChatProcessingTask(Enum):
    VECTOR = auto()
    GRAPH = auto()


class ChatProcessor:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.processors: List[Callable[[Chat], Coroutine[Any, Any, None]]] = []

    def register_processor(self, processor: Callable[[Chat], Coroutine[Any, Any, None]]):
        self.processors.append(processor)

    async def add_task(self, chat: Chat):
        await self.queue.put(chat)

    async def process_queue(self):
        while True:
            chat = await self.queue.get()
            await self._process_chat(chat)
            self.queue.task_done()

    async def _process_chat(self, chat: Chat):
        for processor in self.processors:
            await processor(chat)
