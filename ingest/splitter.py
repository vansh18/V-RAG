from collections import Counter
from config import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(docs):
    """
    Splits the provided documents into smaller chunks.

    Args:
        docs (list): List of documents to be split.
        chunk_size (int): The maximum size of each chunk.
        overlap_percentage (float): The percentage of overlap between chunks.

    Returns:
        list: A list of document chunks.
    """
    print("Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    return splitter.split_documents(docs)
