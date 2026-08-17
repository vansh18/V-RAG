from ingest.loader import load_documents
from ingest.splitter import split_documents
from ingest.metadata import enrich_chunk_metadata


def build_vector_store():

    docs = load_documents()
    all_chunks = []

    for doc in docs:
        chunks = split_documents([doc])
        chunks = enrich_chunk_metadata(chunks)
        all_chunks.extend(chunks)

    return all_chunks

all_chunks = build_vector_store()


for i, chunk in enumerate(all_chunks[:2]):


    print("=" * 100)
    print(f"CHUNK {i + 1} of {len(all_chunks)}")
    print(chunk)
    print("\n")
