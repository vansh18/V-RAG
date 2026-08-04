from config import EMBEDDING_MODEL
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_embedding_model():
    """
    Initializes and returns an instance of OpenAIEmbeddings with the specified model.

    Returns:
        OpenAIEmbeddings: An instance of OpenAIEmbeddings initialized with the specified model.
    """
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)