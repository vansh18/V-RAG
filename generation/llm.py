from config import CHAT_MODEL
from langchain_openai import ChatOpenAI

def get_chat_model():
    """
    Initializes and returns an instance of ChatOpenAI with the specified model.

    Returns:
        ChatOpenAI: An instance of ChatOpenAI initialized with the specified model.
    """
    return ChatOpenAI(model=CHAT_MODEL)