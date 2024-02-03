"""Functions to build prompts for the LLM model."""
from typing import List

from app.schemas import UserOut, TherapistOut, ChatListOut


def build_system_prompt(user: UserOut, therapist: TherapistOut) -> str:
    """Build the system prompt from Pydantic objects."""
    base_prompt = f"""
    I want you to act as a therapist. 
    
    T aim is to help people feel happier and able to reduce suffering in the world. 
    You should be kind and compassionate.

    Your name is {therapist.first_name} {therapist.last_name}. 
    You live in {therapist.residence}. Here are some details about you:
    {therapist.description}

    The user you are helping is {user.first_name} {user.last_name}. 
    They live in {user.city}, {user.country}. They are {user.age} years old.

    You should use your knowledge of recent developments in psychology and psychotherapy to help the user. 
    Ask them questions to get to know more about them and their issues. 
    You will be provided with a summary of useful information before each reply.

    Act from a holistic perspective. 
    Avoid any narcissism or naval gazing from the user. 
    Help them to be a better, more excellent person within the world.
    
    Directions from your notes will be indicated with "[...]".
    """
    base_prompt.format(user=user, therapist=therapist)
    return base_prompt


def build_past_chat_summary_prompt(past_chats: List[str]) -> str:
    """Build the past chat summary prompt."""
    return (
        "System: Here is a summary of our past chats:\n\n"
        + "\n\n".join(past_chats)
        + "\n\nUser: "
    )


def build_new_session_prompt() -> str:
    """Build the new session prompt."""
    return (
        "[This is your first therapy session. "
        "Find out about the user, their family, work, life history, problems, likes and dislikes.]"
    )


def build_first_message_prompt() -> str:
    """Build the first message prompt."""
    return "[Provide a message to the user to start the therapy session.]"


def build_recent_session_history(history: ChatListOut) -> str:
    """Build the recent session history prompt."""
    history_string = f"[Here is a summary of your recent session history:\n\n {ChatListOut.as_string}"
    return history_string


def build_next_message_prompt(user_input: str) -> str:
    """Build the next message prompt."""
    next_message_string = (
        f"[The user last said: {user_input}\n\n"
        f"Provide a next message to the user to continue the therapy session."
        f'(OMIT "Therapist: " from the start of your message.) '
        f"]"
    )
    return next_message_string
