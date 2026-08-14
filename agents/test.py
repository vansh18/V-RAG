from dotenv import load_dotenv

from retrieval.retriever import retrieve
from agents.responder import responder
from agents.prosecutor import prosecutor


load_dotenv()


question = (
    "Which case currently represents the controlling Supreme Court "
    "precedent on whether a university may consider race in admissions?"
)


retrieved_docs = retrieve(question)

responder_output = responder(
    question,
    retrieved_docs
)

print("\n" + "=" * 80)
print("RESPONDER OUTPUT")
print("=" * 80)
print(responder_output)


prosecutor_output = prosecutor(
    question,
    responder_output,
    retrieved_docs
)

print("\n" + "=" * 80)
print("PROSECUTOR OUTPUT")
print("=" * 80)
print(prosecutor_output)