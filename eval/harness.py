import argparse
import json
import time
from datetime import datetime

from config import BASELINE_OUTPUT_PATH, BASELINE_QUESTIONS_PATH
from eval.llm_judge import aggregate_llm_judgments, evaluate_answer_with_llm
from eval.metrics import evaluate_retrieval_at_ks, evaluate_retrieval_slices
from retrieval.serializer import serialize_retrieved_documents


def load_environment():
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv()


def _model_dump(value):
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    return value


def _answer_text(value):
    if value is None:
        return None
    if hasattr(value, "answer"):
        return value.answer
    return str(value)


def load_questions():
    with open(BASELINE_QUESTIONS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_results(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict) and "results" in data:
        return data["results"]

    return data


def base_result(sample, retrieved_docs, latency_seconds=None, error=None):
    result = {
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
        "retrieved_documents": serialize_retrieved_documents(retrieved_docs),
        "latency_seconds": round(latency_seconds, 3) if latency_seconds else None,
    }

    if error:
        result["error"] = error

    return result


def run_retrieval_sample(sample, k):
    from retrieval.retriever import retrieve

    start = time.perf_counter()
    retrieved_docs = retrieve(sample["question"], k=k)
    latency = time.perf_counter() - start
    result = base_result(sample, retrieved_docs, latency_seconds=latency)
    return result, retrieved_docs


def run_baseline_sample(sample, k):
    from generation.baseline import generate_answer
    from retrieval.retriever import retrieve

    start = time.perf_counter()
    retrieved_docs = retrieve(sample["question"], k=k)
    answer = generate_answer(sample["question"], retrieved_docs)
    latency = time.perf_counter() - start

    result = base_result(sample, retrieved_docs, latency_seconds=latency)
    result["answer"] = answer
    return result, retrieved_docs


def run_vrag_sample(sample, k):
    from graph.workflow import app as vrag_app
    from retrieval.retriever import retrieve

    start = time.perf_counter()
    retrieved_docs = retrieve(sample["question"], k=k)

    state = {
        "question": sample["question"],
        "retrieved_documents": retrieved_docs,
        "responder_output": None,
        "prosecutor_output": None,
        "additional_documents": [],
        "judge_output": None,
        "revision_count": 0,
    }
    output = vrag_app.invoke(state)
    latency = time.perf_counter() - start

    result = base_result(sample, retrieved_docs, latency_seconds=latency)
    result["answer"] = _answer_text(output["responder_output"])
    result["responder_output"] = _model_dump(output["responder_output"])
    result["prosecutor_output"] = _model_dump(output["prosecutor_output"])
    result["judge_output"] = _model_dump(output["judge_output"])
    result["revision_count"] = output["revision_count"]
    result["additional_documents"] = serialize_retrieved_documents(
        output["additional_documents"]
    )
    return result, retrieved_docs + output["additional_documents"]


def run_samples(mode, questions, k, judge=False):
    runners = {
        "retrieval": run_retrieval_sample,
        "baseline": run_baseline_sample,
        "vrag": run_vrag_sample,
    }
    run_sample = runners[mode]

    results = []
    judgments = []

    for sample in questions:
        try:
            print(f"[{sample['question_id']}] {sample['question']}")
            result, eval_evidence = run_sample(sample, k)

            if judge and result.get("answer") is not None:
                judgment = evaluate_answer_with_llm(
                    sample,
                    result["answer"],
                    eval_evidence,
                )
                result["llm_judgment"] = _model_dump(judgment)
                judgments.append(judgment)

            results.append(result)

        except Exception as exc:
            results.append(base_result(sample, [], error=str(exc)))
            print(f"[{sample['question_id']}] ERROR: {exc}")

    return results, judgments


def judge_existing_results(results):
    judgments = []

    for result in results:
        if not result.get("answer"):
            continue

        print(f"[{result['question_id']}] judging saved answer")
        judgment = evaluate_answer_with_llm(
            result,
            result["answer"],
            result.get("retrieved_documents", []),
        )
        result["llm_judgment"] = _model_dump(judgment)
        judgments.append(judgment)

    return results, judgments


def build_report(mode, results, judgments, k, k_values):
    report = {
        "metadata": {
            "mode": mode,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "count": len(results),
            "retrieval_k": k,
        },
        "retrieval_metrics": {
            "by_k": evaluate_retrieval_at_ks(results, k_values),
            "slices_at_k": evaluate_retrieval_slices(results, k=k),
        },
        "llm_eval_metrics": aggregate_llm_judgments(judgments),
        "results": results,
    }

    return report


def write_report(report, prefix):
    BASELINE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = BASELINE_OUTPUT_PATH / filename

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    return output_path


def main():
    load_environment()

    parser = argparse.ArgumentParser(description="Run V-RAG evaluation harness.")
    parser.add_argument(
        "--mode",
        choices=["retrieval", "baseline", "vrag", "score-file"],
        default="retrieval",
    )
    parser.add_argument("--input", help="Existing JSON output to judge.")
    parser.add_argument("--limit", type=int, help="Limit question count.")
    parser.add_argument("--k", type=int, default=7)
    parser.add_argument("--ks", nargs="+", type=int, default=[1, 3, 5, 7])
    parser.add_argument("--judge", action="store_true", help="Run LLM-as-judge.")
    args = parser.parse_args()

    if args.mode == "score-file":
        if not args.input:
            raise ValueError("--input is required for --mode score-file")
        results = load_results(args.input)
        if args.limit:
            results = results[:args.limit]
        results, judgments = judge_existing_results(results)
    else:
        questions = load_questions()
        if args.limit:
            questions = questions[:args.limit]
        results, judgments = run_samples(args.mode, questions, args.k, args.judge)

    report = build_report(args.mode, results, judgments, args.k, args.ks)
    output_path = write_report(report, f"{args.mode}_eval")

    print(f"Evaluation complete: {output_path}")
    print(json.dumps(report["retrieval_metrics"]["by_k"], indent=2))
    if judgments:
        print(json.dumps(report["llm_eval_metrics"], indent=2))


if __name__ == "__main__":
    main()
