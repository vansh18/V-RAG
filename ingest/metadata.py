def enrich_chunk_metadata(chunks):
    """
    Adds metadata that is only available after a document has been split.
    """

    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["total_chunks"] = total_chunks

    return chunks