def serialize_retrieved_documents(retrieved_docs):

    serialized_documents = []

    for doc in retrieved_docs:
        metadata = doc.metadata.copy()
        serialized_documents.append(metadata)

    return serialized_documents
