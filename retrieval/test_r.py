from retrieval.retriever import retrieve

chunks = retrieve(
    "What did the Supreme Court hold in Bakke?",
    k=3
)

for i, chunk in enumerate(chunks, start=1):
        print(f"==== Document {i} ====\n")
        print(f"Source: {chunk.metadata['source']}")
        print(f"Case Name: {chunk.metadata['case_name']}")
        print(f"Citation: {chunk.metadata['citation']}")
        print(f"Decision date: {chunk.metadata['decision_date']}")
        print(f"Court: {chunk.metadata['court']}")
        print(f"Chunk id: {chunk.metadata['chunk_id']}")
        print(f"Total chunks : {chunk.metadata['total_chunks']}")