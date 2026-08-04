from retrieval.retriever import retrieve

chunks = retrieve(
    "affirmative action in medical school admissions",
    k=3
)

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}")
    print(chunk.metadata)
    print(chunk.page_content[:300])