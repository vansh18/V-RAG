import pytest

from eval.metrics import (
    calculate_average_precision,
    calculate_document_recall,
    calculate_reciprocal_rank,
    evaluate_retrieval_at_ks,
    evaluate_retrieval_metrics,
    evaluate_retrieval_slices,
)


def test_document_recall_counts_unique_expected_documents():
    retrieved_documents = [
        {"source": "unrelated.txt"},
        {"source": "alpha.txt"},
        {"source": "alpha.txt"},
        {"source": "beta.txt"},
    ]

    assert calculate_document_recall(
        ["alpha.txt", "beta.txt"],
        retrieved_documents,
        k=3,
    ) == 0.5


def test_reciprocal_rank_uses_first_relevant_result():
    retrieved_documents = [
        {"source": "unrelated.txt"},
        {"source": "alpha.txt"},
        {"source": "beta.txt"},
    ]

    assert calculate_reciprocal_rank(
        ["alpha.txt", "beta.txt"],
        retrieved_documents,
        ("source",),
        k=3,
    ) == 0.5


def test_average_precision_rewards_multiple_relevant_hits_by_rank():
    retrieved_documents = [
        {"source": "unrelated.txt"},
        {"source": "alpha.txt"},
        {"source": "beta.txt"},
    ]

    assert calculate_average_precision(
        ["alpha.txt", "beta.txt"],
        retrieved_documents,
        ("source",),
        k=3,
    ) == pytest.approx((1 / 2 + 2 / 3) / 2)


def test_evaluate_retrieval_metrics_aggregates_document_case_and_citation():
    results = [
        {
            "supporting_documents": ["alpha.txt", "beta.txt"],
            "supporting_cases": ["Alpha", "Beta"],
            "supporting_citations": ["1 U.S. 1", "2 U.S. 2"],
            "retrieved_documents": [
                {
                    "source": "unrelated.txt",
                    "case_name": "Unrelated",
                    "citation": "9 U.S. 9",
                },
                {
                    "source": "alpha.txt",
                    "case_name": "Alpha",
                    "citation": "1 U.S. 1",
                },
            ],
        },
        {
            "supporting_documents": ["gamma.txt"],
            "supporting_cases": ["Gamma"],
            "supporting_citations": ["3 U.S. 3"],
            "retrieved_documents": [
                {
                    "source": "gamma.txt",
                    "case_name": "Gamma",
                    "citation": "3 U.S. 3",
                },
            ],
        },
    ]

    metrics = evaluate_retrieval_metrics(results, k=2)

    assert metrics["document_recall"] == pytest.approx(0.75)
    assert metrics["case_recall"] == pytest.approx(0.75)
    assert metrics["citation_recall"] == pytest.approx(0.75)
    assert metrics["document_mrr"] == pytest.approx(0.75)
    assert metrics["document_hit_rate"] == pytest.approx(1.0)


def test_evaluate_retrieval_at_ks_and_slices():
    results = [
        {
            "category": "Fact Retrieval",
            "difficulty": "Easy",
            "requires_multi_hop_reasoning": False,
            "requires_temporal_reasoning": False,
            "contains_contradictory_evidence": False,
            "supporting_documents": ["alpha.txt"],
            "supporting_cases": ["Alpha"],
            "supporting_citations": ["1 U.S. 1"],
            "retrieved_documents": [
                {
                    "source": "alpha.txt",
                    "case_name": "Alpha",
                    "citation": "1 U.S. 1",
                },
            ],
        }
    ]

    by_k = evaluate_retrieval_at_ks(results, k_values=(1,))
    slices = evaluate_retrieval_slices(results, k=1)

    assert by_k["k_1"]["document_recall"] == 1.0
    assert slices["all"]["count"] == 1
    assert slices["category:Fact Retrieval"]["metrics"]["document_mrr"] == 1.0
