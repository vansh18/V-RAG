from langchain_chroma import Chroma

from config import VECTOR_DB_DIR, COLLECTION_NAME
from ingest.embedder import get_embedding_model

def load_vector_store():
    """
    Loads the existing Chroma vector store.

    Returns:
        Chroma: The persisted vector store.
    """

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=str(VECTOR_DB_DIR),
        embedding_function=embedding_model,
        collection_name=COLLECTION_NAME,
    )

    return vector_store

def retrieve(query, k=5):
    """
    Retrieves the top-k most relevant chunks.

    Args:
        query (str): User query.
        k (int): Number of chunks to retrieve.

    Returns:
        list[Document]
    """

    vector_store = load_vector_store()
    
    return vector_store.similarity_search(
        query=query,
        k=k,
    )