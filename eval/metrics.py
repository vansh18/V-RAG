import json

from config import BASELINE_OUTPUT_PATH


def calculate_document_recall(supporting_documents, retrieved_documents, k):

    expected_documents = set(supporting_documents)

    retrieved_sources = {
        document["source"]
        for document in retrieved_documents[:k]
    }

    if not expected_documents:
        return 0.0

    matched_documents = expected_documents & retrieved_sources

    return len(matched_documents) / len(expected_documents)


def calculate_case_recall(supporting_cases, retrieved_documents, k):

    expected_cases = set(supporting_cases)

    retrieved_cases = {
        document["case_name"]
        for document in retrieved_documents[:k]
    }

    if not expected_cases:
        return 0.0

    matched_cases = expected_cases & retrieved_cases

    return len(matched_cases) / len(expected_cases)


def calculate_citation_recall(supporting_citations, retrieved_documents, k):
    """Calculate citation-level Recall@k for one question."""

    expected_citations = set(supporting_citations)

    retrieved_citations = {
        document["citation"]
        for document in retrieved_documents[:k]
    }

    if not expected_citations:
        return 0.0

    matched_citations = expected_citations & retrieved_citations

    return len(matched_citations) / len(expected_citations)


def calculate_overall_recall(recall_scores):

    if not recall_scores:
        return 0.0

    return sum(recall_scores) / len(recall_scores)


def evaluate_retrieval_metrics(results, k):
    """
    Calculate retrieval metrics across an evaluation dataset.

    Returns:
        dict: Overall document, case, and citation recall.
    """

    document_scores = []
    case_scores = []
    citation_scores = []

    for result in results:

        retrieved_documents = result["retrieved_documents"]

        document_scores.append(
            calculate_document_recall(
                result["supporting_documents"],
                retrieved_documents,
                k
            )
        )

        case_scores.append(
            calculate_case_recall(
                result["supporting_cases"],
                retrieved_documents,
                k
            )
        )

        citation_scores.append(
            calculate_citation_recall(
                result["supporting_citations"],
                retrieved_documents,
                k
            )
        )

    return {
        "document_recall": calculate_overall_recall(document_scores),
        "case_recall": calculate_overall_recall(case_scores),
        "citation_recall": calculate_overall_recall(citation_scores),
    }


def load_results(filename):
    """Load a retrieval experiment JSON file."""

    path = BASELINE_OUTPUT_PATH / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":

    filename = "retrieval_k7_20260809_125520.json"

    results = load_results(filename)

    for k in [3, 5, 7]:

        metrics = evaluate_retrieval_metrics(results, k)

        print(f"\nRecall@{k}")
        print(f"Document Recall: {metrics['document_recall']:.3f}")
        print(f"Case Recall:     {metrics['case_recall']:.3f}")
        print(f"Citation Recall: {metrics['citation_recall']:.3f}")