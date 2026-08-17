from ingest.loader import load_documents
from ingest.splitter import split_documents
from ingest.metadata import enrich_chunk_metadata
from ingest.embedding_text import create_embedding_documents
from ingest.vectorstore import create_vector_store
from config import VECTOR_DB_DIR
import shutil


def build_vector_store():
    """Load, split, enrich metadata, embed, and persist all documents."""
    print("Building vector store...")

    docs = load_documents()
    all_chunks = []

    for doc in docs:
        chunks = split_documents([doc])
        chunks = enrich_chunk_metadata(chunks)

        embedding_documents = create_embedding_documents(chunks)
        
        all_chunks.extend(embedding_documents)

    create_vector_store(all_chunks)


def main(force_rebuild=True):

    # First-time setup: create the vector store if it doesn't already exist.
    if not VECTOR_DB_DIR.exists():
        build_vector_store()

    # Skip ingestion if the vector store already exists and a rebuild wasn't requested.
    elif not force_rebuild:
        print("Vector store already exists.\nSkipping ingestion.")

    # Rebuild the vector store from scratch.
    else:
        shutil.rmtree(VECTOR_DB_DIR)
        build_vector_store()


if __name__ == "__main__":
    main()