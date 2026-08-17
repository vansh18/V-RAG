from langchain_core.documents import Document


def create_embedding_documents(chunks):

    embedding_documents = []

    for chunk in chunks:

        metadata = chunk.metadata.copy()

        metadata["original_content"] = chunk.page_content

        enriched_text = f"""
Case: {metadata.get("case_name", "")}
Citation: {metadata.get("citation", "")}
Court: {metadata.get("court", "")}
Year: {metadata.get("year", "")}
Opinion Type: {metadata.get("opinion_type", "")}
Topic: {metadata.get("topic", "")}

{chunk.page_content}
""".strip()

        embedding_documents.append(
            Document(
                page_content=enriched_text,
                metadata=metadata,
            )
        )

    return embedding_documents