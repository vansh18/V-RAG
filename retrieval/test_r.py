from retrieval.retriever import load_vector_store
from ingest.embedder import get_embedding_model


QUERY = (
    "Harmon v. Board of Trustees of Ashworth University 2023 "
    "Supreme Court holding race admissions Whitfield overrule "
    "controlling precedent"
)

TARGET_SOURCE = "harmon_v_ashworth_university_majority_2023.txt"
TARGET_CHUNK_ID = 15


def cosine_distance(a, b):
    """
    Returns cosine distance = 1 - cosine similarity.
    Lower is better.
    """
    dot_product = sum(x * y for x, y in zip(a, b))

    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5

    cosine_similarity = dot_product / (norm_a * norm_b)

    return 1 - cosine_similarity


def main():

    vector_store = load_vector_store()
    embedding_model = get_embedding_model()

    # ---------------------------------------------------------
    # 1. Find the target chunk
    # ---------------------------------------------------------

    results = vector_store.similarity_search_with_score(
        query=QUERY,
        k=50,
    )

    target_doc = None
    original_chroma_score = None
    original_rank = None

    for rank, (doc, score) in enumerate(results, start=1):

        if (
            doc.metadata.get("source") == TARGET_SOURCE
            and doc.metadata.get("chunk_id") == TARGET_CHUNK_ID
        ):
            target_doc = doc
            original_chroma_score = score
            original_rank = rank
            break

    if target_doc is None:
        raise ValueError(
            "Target chunk was not found in the top 50 results."
        )

    # ---------------------------------------------------------
    # 2. Current chunk text
    # ---------------------------------------------------------

    current_text = target_doc.page_content

    # ---------------------------------------------------------
    # 3. Enriched embedding text
    # ---------------------------------------------------------

    enriched_text = f"""
Case: {target_doc.metadata.get("case_name", "")}
Citation: {target_doc.metadata.get("citation", "")}
Court: {target_doc.metadata.get("court", "")}
Year: {target_doc.metadata.get("year", "")}
Opinion Type: {target_doc.metadata.get("opinion_type", "")}
Topic: {target_doc.metadata.get("topic", "")}
Section: Holding

{current_text}
""".strip()

    # ---------------------------------------------------------
    # 4. Generate embeddings
    # ---------------------------------------------------------

    query_embedding = embedding_model.embed_query(QUERY)

    current_embedding = embedding_model.embed_query(
        current_text
    )

    enriched_embedding = embedding_model.embed_query(
        enriched_text
    )

    # ---------------------------------------------------------
    # 5. Calculate distances
    # ---------------------------------------------------------

    current_distance = cosine_distance(
        query_embedding,
        current_embedding,
    )

    enriched_distance = cosine_distance(
        query_embedding,
        enriched_embedding,
    )

    # ---------------------------------------------------------
    # 6. Print results
    # ---------------------------------------------------------

    print("=" * 80)
    print("RETRIEVAL / EMBEDDING COMPARISON")
    print("=" * 80)

    print(f"\nSource: {TARGET_SOURCE}")
    print(f"Chunk ID: {TARGET_CHUNK_ID}")

    print("\nOriginal Chroma result:")
    print(f"  Rank: {original_rank}")
    print(f"  Chroma distance: {original_chroma_score}")

    print("\nManual cosine distance:")
    print(f"  Current chunk:   {current_distance:.6f}")
    print(f"  Enriched chunk:  {enriched_distance:.6f}")

    print("\nImprovement:")

    if enriched_distance < current_distance:
        improvement = current_distance - enriched_distance

        print(
            f"  Enriched representation is "
            f"{improvement:.6f} closer to the query."
        )

    elif enriched_distance > current_distance:
        degradation = enriched_distance - current_distance

        print(
            f"  Enriched representation is "
            f"{degradation:.6f} farther from the query."
        )

    else:
        print("  No change.")

    print("\n" + "=" * 80)
    print("CURRENT CHUNK")
    print("=" * 80)
    print(current_text)

    print("\n" + "=" * 80)
    print("ENRICHED EMBEDDING TEXT")
    print("=" * 80)
    print(enriched_text)


if __name__ == "__main__":
    main()