import json
import time
from datetime import datetime
from config import BASELINE_QUESTIONS_PATH, BASELINE_OUTPUT_PATH
from retrieval.retriever import retrieve
from retrieval.serializer import serialize_retrieved_documents
from generation.baseline import generate_answer

def load_questions():
    with open(BASELINE_QUESTIONS_PATH, 'r', encoding="utf-8") as f:
        return json.load(f)

def evaluate():
    questions = load_questions()
    results = []
    success_count = 0
    failed_count = 0

    for sample in questions:
        try:            
            question = sample["question"]
            print(f"[{sample['question_id']}] {question}")

            start = time.perf_counter()

            retrieved_docs = retrieve(question)
            answer = generate_answer(question, retrieved_docs)

            latency = time.perf_counter() - start

            serialized_docs = serialize_retrieved_documents(retrieved_docs)

            success_count += 1

            results.append(
                {
                    "question_id": sample["question_id"],
                    "category": sample["category"],
                    "difficulty": sample["difficulty"],
                    "question": sample["question"],

                    "expected_answer": sample["expected_answer"],
                    "explanation": sample["explanation"],
                    "supporting_documents": sample["supporting_documents"],
                    "supporting_cases": sample["supporting_cases"],
                    "supporting_citations": sample["supporting_citations"],

                    "expected_retrieval_count": sample["expected_retrieval_count"],
                    "requires_temporal_reasoning": sample["requires_temporal_reasoning"],
                    "requires_multi_hop_reasoning": sample["requires_multi_hop_reasoning"],
                    "contains_contradictory_evidence": sample["contains_contradictory_evidence"],

                    "answer": answer,
                    "retrieved_documents": serialized_docs,
                    "latency_seconds": round(latency, 3)
                }
            )

        except Exception as e:
            print(f"❌ [{sample['question_id']}] {e}")
            failed_count += 1
            results.append(
                {
                    "question_id": sample["question_id"],
                    "category": sample["category"],
                    "difficulty": sample["difficulty"],
                    "question": sample["question"],

                    "expected_answer": sample["expected_answer"],
                    "explanation": sample["explanation"],
                    "supporting_documents": sample["supporting_documents"],
                    "supporting_cases": sample["supporting_cases"],
                    "supporting_citations": sample["supporting_citations"],

                    "expected_retrieval_count": sample["expected_retrieval_count"],
                    "requires_temporal_reasoning": sample["requires_temporal_reasoning"],
                    "requires_multi_hop_reasoning": sample["requires_multi_hop_reasoning"],
                    "contains_contradictory_evidence": sample["contains_contradictory_evidence"],

                    "answer": None,
                    "retrieved_documents": [],
                    "latency_seconds": None,
                    "error": str(e),
                }
            )

    BASELINE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    filename = f"baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file = BASELINE_OUTPUT_PATH / filename

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            results, 
            f, 
            indent=4,
            ensure_ascii=False
        )

    print(f"Evaluation completed. {success_count} questions processed successfully, {failed_count} failed.")
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    evaluate()