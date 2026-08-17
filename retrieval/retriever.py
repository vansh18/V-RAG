from langchain_chroma import Chroma
from langchain_core.documents import Document
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

def retrieve(query, k=3):

    vector_store = load_vector_store()

    retrieved_docs = vector_store.similarity_search(
        query=query,
        k=k,
    )

    original_docs = []

    for doc in retrieved_docs:

        original_content = doc.metadata.get(
            "original_content",
            doc.page_content
        )

        metadata = doc.metadata.copy()

        metadata.pop("original_content", None)

        original_docs.append(
            Document(
                page_content=original_content,
                metadata=metadata,
            )
        )

    return original_docs