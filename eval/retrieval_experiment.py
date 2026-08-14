import json
from datetime import datetime

from retrieval.retriever import retrieve
from retrieval.serializer import serialize_retrieved_documents
from config import BASELINE_QUESTIONS_PATH, BASELINE_OUTPUT_PATH


def load_questions():
    with open(BASELINE_QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieval_k7():
    questions = load_questions()
    results = []

    for sample in questions:

        question = sample["question"]

        retrieved_docs = retrieve(
            question,
            k=7
        )

        serialized_docs = serialize_retrieved_documents(retrieved_docs)

        results.append(
            {
                "question_id": sample["question_id"],
                "question": question,
                "supporting_documents": sample["supporting_documents"],
                "supporting_cases": sample["supporting_cases"],
                "supporting_citations": sample["supporting_citations"],
                "retrieved_documents": serialized_docs
            }
        )

    BASELINE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    filename = f"retrieval_k7_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file = BASELINE_OUTPUT_PATH / filename

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Retrieval experiment completed.")
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    retrieval_k7()