from retrieval.retriever import retrieve

query = (
    "Harmon v. Board of Trustees of Ashworth University 2023 "
    "Supreme Court holding race admissions Whitfield overrule "
    "controlling precedent"
)

docs = retrieve(query, k=3)

for i, doc in enumerate(docs, start=1):

    print("=" * 100)
    print(f"RANK: {i}")
    print(f"SOURCE: {doc.metadata.get('source')}")
    print(f"CHUNK: {doc.metadata.get('chunk_id')}")
    print("=" * 100)
    print(doc.page_content)