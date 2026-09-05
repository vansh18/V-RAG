import argparse
import json
from collections import defaultdict
from statistics import mean

from config import BASELINE_OUTPUT_PATH


FIELD_SPECS = {
    "document": {
        "expected_key": "supporting_documents",
        "retrieved_keys": ("source", "filename"),
    },
    "case": {
        "expected_key": "supporting_cases",
        "retrieved_keys": ("case_name",),
    },
    "citation": {
        "expected_key": "supporting_citations",
        "retrieved_keys": ("citation",),
    },
}


def _normalize(value):
    return str(value).strip().casefold()


def _expected_values(values):
    return {_normalize(value) for value in values if value}


def _retrieved_values(document, keys):
    return {
        _normalize(document[key])
        for key in keys
        if document.get(key)
    }


def _retrieved_sequence(retrieved_documents, keys, k):
    return [
        _retrieved_values(document, keys)
        for document in retrieved_documents[:k]
    ]


def calculate_recall(expected_values, retrieved_documents, retrieved_keys, k):
    expected = _expected_values(expected_values)

    if not expected:
        return 0.0

    retrieved = set()
    for values in _retrieved_sequence(retrieved_documents, retrieved_keys, k):
        retrieved.update(values)

    return len(expected & retrieved) / len(expected)


def calculate_precision(expected_values, retrieved_documents, retrieved_keys, k):
    expected = _expected_values(expected_values)

    if not expected or k <= 0:
        return 0.0

    relevant_count = 0
    for values in _retrieved_sequence(retrieved_documents, retrieved_keys, k):
        if expected & values:
            relevant_count += 1

    return relevant_count / k


def calculate_reciprocal_rank(expected_values, retrieved_documents, retrieved_keys, k):
    expected = _expected_values(expected_values)

    if not expected:
        return 0.0

    for rank, values in enumerate(
        _retrieved_sequence(retrieved_documents, retrieved_keys, k),
        start=1,
    ):
        if expected & values:
            return 1.0 / rank

    return 0.0


def calculate_average_precision(expected_values, retrieved_documents, retrieved_keys, k):
    expected = _expected_values(expected_values)

    if not expected:
        return 0.0

    seen_matches = set()
    precision_sum = 0.0
    relevant_seen = 0

    for rank, values in enumerate(
        _retrieved_sequence(retrieved_documents, retrieved_keys, k),
        start=1,
    ):
        new_matches = (expected & values) - seen_matches
        if not new_matches:
            continue

        seen_matches.update(new_matches)
        relevant_seen += 1
        precision_sum += relevant_seen / rank

    return precision_sum / len(expected)


def calculate_document_recall(supporting_documents, retrieved_documents, k):
    return calculate_recall(
        supporting_documents,
        retrieved_documents,
        FIELD_SPECS["document"]["retrieved_keys"],
        k,
    )


def calculate_case_recall(supporting_cases, retrieved_documents, k):
    return calculate_recall(
        supporting_cases,
        retrieved_documents,
        FIELD_SPECS["case"]["retrieved_keys"],
        k,
    )


def calculate_citation_recall(supporting_citations, retrieved_documents, k):
    return calculate_recall(
        supporting_citations,
        retrieved_documents,
        FIELD_SPECS["citation"]["retrieved_keys"],
        k,
    )


def calculate_overall_recall(recall_scores):
    if not recall_scores:
        return 0.0

    return sum(recall_scores) / len(recall_scores)


def evaluate_retrieval_metrics(results, k):
    """
    Calculate aggregate retrieval metrics across an evaluation dataset.

    The returned keys keep the original recall names and add standard retrieval
    metrics used in RAG evaluations: hit rate, MRR, MAP, and precision.
    """

    metric_scores = defaultdict(list)

    for result in results:
        retrieved_documents = result.get("retrieved_documents", [])

        for label, spec in FIELD_SPECS.items():
            expected = result.get(spec["expected_key"], [])
            retrieved_keys = spec["retrieved_keys"]

            metric_scores[f"{label}_recall"].append(
                calculate_recall(expected, retrieved_documents, retrieved_keys, k)
            )
            metric_scores[f"{label}_precision"].append(
                calculate_precision(expected, retrieved_documents, retrieved_keys, k)
            )
            metric_scores[f"{label}_hit_rate"].append(
                1.0
                if calculate_reciprocal_rank(
                    expected,
                    retrieved_documents,
                    retrieved_keys,
                    k,
                )
                else 0.0
            )
            metric_scores[f"{label}_mrr"].append(
                calculate_reciprocal_rank(
                    expected,
                    retrieved_documents,
                    retrieved_keys,
                    k,
                )
            )
            metric_scores[f"{label}_map"].append(
                calculate_average_precision(
                    expected,
                    retrieved_documents,
                    retrieved_keys,
                    k,
                )
            )

    return {
        metric: mean(scores) if scores else 0.0
        for metric, scores in sorted(metric_scores.items())
    }


def evaluate_retrieval_at_ks(results, k_values=(1, 3, 5, 7)):
    return {
        f"k_{k}": evaluate_retrieval_metrics(results, k)
        for k in k_values
    }


def evaluate_retrieval_slices(results, k=7):
    """
    Compute the same aggregate metrics over common testset slices.
    """

    slices = {
        "all": results,
        "multi_hop": [
            result for result in results
            if result.get("requires_multi_hop_reasoning")
        ],
        "temporal": [
            result for result in results
            if result.get("requires_temporal_reasoning")
        ],
        "contradictory_evidence": [
            result for result in results
            if result.get("contains_contradictory_evidence")
        ],
    }

    for field in ("category", "difficulty"):
        values = sorted({result.get(field) for result in results if result.get(field)})
        for value in values:
            key = f"{field}:{value}"
            slices[key] = [
                result for result in results
                if result.get(field) == value
            ]

    return {
        slice_name: {
            "count": len(slice_results),
            "metrics": evaluate_retrieval_metrics(slice_results, k),
        }
        for slice_name, slice_results in slices.items()
        if slice_results
    }


def load_results(filename):
    path = BASELINE_OUTPUT_PATH / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description="Report retrieval eval metrics.")
    parser.add_argument("filename", help="JSON filename inside eval/outputs")
    parser.add_argument("--ks", nargs="+", type=int, default=[1, 3, 5, 7])
    parser.add_argument("--slice-k", type=int, default=7)
    args = parser.parse_args()

    results = load_results(args.filename)

    print(json.dumps(
        {
            "count": len(results),
            "by_k": evaluate_retrieval_at_ks(results, args.ks),
            "slices": evaluate_retrieval_slices(results, args.slice_k),
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
