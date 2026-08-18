from retrieval.retriever import retrieve
from graph.workflow import app


question = (
    "Which case currently represents the controlling Supreme Court precedent on whether a university may consider race in admissions?"
)


retrieved_documents = retrieve(question, 7)


initial_state = {
    "question": question,
    "retrieved_documents": retrieved_documents,
    "responder_output": None,
    "prosecutor_output": None,
    "additional_documents": [],
    "judge_output": None,
    "revision_count": 0,
}


result = app.invoke(initial_state)


print("\n" + "=" * 80)
print("FINAL RESPONDER OUTPUT")
print("=" * 80)
print(result["responder_output"])

print("\n" + "=" * 80)
print("FINAL PROSECUTOR OUTPUT")
print("=" * 80)
print(result["prosecutor_output"])

print("\n" + "=" * 80)
print("JUDGE OUTPUT")
print("=" * 80)
print(result["judge_output"])

print("\n" + "=" * 80)
print("REVISION COUNT")
print("=" * 80)
print(result["revision_count"])

print("\n" + "=" * 80)
print("ADDITIONAL DOCUMENTS")
print("=" * 80)

for doc in result["additional_documents"]:
    print(
        f"Source: {doc.metadata.get('source', 'Unknown')}, "
        f"Chunk: {doc.metadata.get('chunk_id', 'Unknown')}"
    )