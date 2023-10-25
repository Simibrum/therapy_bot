"""Functions to build prompts for the LLM model."""
from typing import List
from models import User


def build_system_prompt(user: User) -> str:
    """Build the system prompt."""
    return "System: Hello, I'm a therapist. What's on your mind?\n\nUser: "


def build_past_chat_summary_prompt(past_chats: List[str]) -> str:
    """Build the past chat summary prompt."""
    return "System: Here is a summary of our past chats:\n\n" + "\n\n".join(
        past_chats
    ) + "\n\nUser: "