from shushu_novelty.evaluation.retrieval_benchmark import (
    TopicRetrievalResult,
    count_remaining_duplicates,
    summarize_retrieval_results,
    validate_topic_suite,
)
from shushu_novelty.schemas import PaperRecord, Provenance, RetrievalBenchmarkTopic


def topics():
    return [
        RetrievalBenchmarkTopic(
            topic_id=f"RT-{index:03d}",
            query=f"unique retrieval query {index}",
            domain="fixture",
        )
        for index in range(1, 21)
    ]


def result(index: int, second_source_success: bool = True) -> TopicRetrievalResult:
    return TopicRetrievalResult(
        topic_id=f"RT-{index:03d}",
        source_success={"arxiv": True, "openalex": second_source_success},
        raw_source_records=8,
        deduplicated_records=5,
        remaining_duplicate_records=0,
        serializable_records=5,
    )


def test_fixed_retrieval_topic_suite_has_twenty_unique_queries():
    assert validate_topic_suite(topics()) == []


def test_connector_success_threshold_is_per_source():
    results = [result(index, second_source_success=index != 1) for index in range(1, 21)]

    report = summarize_retrieval_results(results, ["arxiv", "openalex"])

    assert report["publishable"]
    assert report["source_success_rates"]["openalex"] == 0.95


def test_connector_below_ninety_five_percent_fails():
    results = [result(index, second_source_success=index > 2) for index in range(1, 21)]

    report = summarize_retrieval_results(results, ["arxiv", "openalex"])

    assert not report["publishable"]
    assert any("below 95%" in error for error in report["errors"])


def test_remaining_duplicate_detection_is_independent_of_identifiers():
    provenance = [
        Provenance(source="fixture", source_identifier="1", retrieved_at="now")
    ]
    records = [
        PaperRecord(
            paper_id="P-fixture:1",
            title="Same Paper Title",
            identifiers={"fixture": "1"},
            provenance=provenance,
        ),
        PaperRecord(
            paper_id="P-fixture:2",
            title="Same paper-title!",
            identifiers={"fixture": "2"},
            provenance=provenance,
        ),
    ]

    assert count_remaining_duplicates(records) == 1
