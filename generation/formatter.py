def format_documents(documents):

    formatted_documents = []

    for i, doc in enumerate(documents, start=1):

        formatted_doc = f"""==== Document {i} ====
        Source: {doc.metadata.get("source", "Unknown")}
        Chunk ID: {doc.metadata.get("chunk_id", "Unknown")}

        {doc.page_content}
        """

        formatted_documents.append(formatted_doc)
    return "\n\n".join(formatted_documents)