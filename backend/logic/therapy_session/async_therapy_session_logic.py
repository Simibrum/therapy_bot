"""Logic to run a therapy session asynchronously."""
from enum import Enum, auto
from typing import Optional


class TherapySessionState(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    ENDED = auto()


class AsyncTherapySessionLogic:
    def __init__(
        self,
        user_id: Optional[int],
        therapist_id: Optional[int],
        pre_existing_session_id: Optional[int],
        db_manager: DatabaseManager,
        chat_processor: ChatProcessor,
        prompt_builder: PromptBuilder,
    ):
        self.user_id = user_id
        self.therapist_id = therapist_id
        self.therapy_session_id = pre_existing_session_id
        self.db_manager = db_manager
        self.chat_processor = chat_processor
        self.prompt_builder = prompt_builder
        self.state = TherapySessionState.NOT_STARTED

    async def initialize(self):
        if self.therapy_session_id:
            await self.load_existing_session()
        elif self.user_id:
            await self.create_new_session()
        else:
            raise ValueError("Must provide either a user id or a pre-existing session id")

        self.system_prompt = await self.prompt_builder.build_system_prompt(self.user, self.therapist)
        asyncio.create_task(self.chat_processor.process_queue())
        self.state = TherapySessionState.IN_PROGRESS

    async def add_chat_message(self, sender: str, text: str) -> ChatOut:
        new_chat = await self.db_manager.add_chat(
            self.user_id, self.therapist_id, self.therapy_session_id, sender, text
        )
        await self.chat_processor.add_task(new_chat)
        return ChatOut.model_validate(new_chat)
