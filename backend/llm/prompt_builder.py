"""Functions to build prompts for the LLM model."""
from models import User

def build_system_prompt(user: User) -> str:
    """Build the system prompt."""
    return "System: Hello, I'm a therapist. What's on your mind?\n\nUser: "