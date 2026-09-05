from eval.llm_judge import LLMEvalOutput, aggregate_llm_judgments


def test_aggregate_llm_judgments_reports_quality_and_risk_rates():
    judgments = [
        LLMEvalOutput(
            correctness="correct",
            faithfulness_score=1.0,
            groundedness_score=1.0,
            completeness_score=1.0,
            relevance_score=1.0,
            citation_support_score=1.0,
            hallucination_score=0.0,
            hallucination_detected=False,
            contradiction_detected=False,
            unsupported_claims=[],
            missing_expected_facts=[],
            reasoning="Fully supported.",
        ),
        LLMEvalOutput(
            correctness="partially_correct",
            faithfulness_score=0.5,
            groundedness_score=0.25,
            completeness_score=0.75,
            relevance_score=1.0,
            citation_support_score=0.5,
            hallucination_score=0.5,
            hallucination_detected=True,
            contradiction_detected=True,
            unsupported_claims=["Unsupported legal status claim."],
            missing_expected_facts=["Missing date."],
            reasoning="Partially supported.",
        ),
    ]

    metrics = aggregate_llm_judgments(judgments)

    assert metrics["count"] == 2
    assert metrics["correctness_rate"] == 0.5
    assert metrics["partial_or_correct_rate"] == 1.0
    assert metrics["hallucination_rate"] == 0.5
    assert metrics["contradiction_rate"] == 0.5
    assert metrics["average_faithfulness"] == 0.75
