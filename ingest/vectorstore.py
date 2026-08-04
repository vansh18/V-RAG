from config import VECTOR_DB_DIR
from langchain_chroma import Chroma
from ingest.embedder import get_embedding_model, COLLECTION_NAME

def create_vector_store(chunks):
    """
    Creates and persists a Chroma vector store.

    Args:
        chunks (list[Document]): The document chunks to index.

    Returns:
        Chroma: The created vector store.
    """

    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(VECTOR_DB_DIR),
        collection_name=COLLECTION_NAME,
    )
    print("Vector store created successfully.")

    return vector_store