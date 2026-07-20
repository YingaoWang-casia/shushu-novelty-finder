"""Live 20-topic connector reliability and deduplication benchmark."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from shushu_novelty.errors import RetrievalError
from shushu_novelty.io import write_jsonl
from shushu_novelty.retrieval.multi import search_sources
from shushu_novelty.retrieval.replay import create_search_manifest
from shushu_novelty.schemas import PaperRecord, RetrievalBenchmarkTopic


@dataclass(frozen=True)
class TopicRetrievalResult:
    topic_id: str
    source_success: dict[str, bool]
    raw_source_records: int
    deduplicated_records: int
    remaining_duplicate_records: int
    serializable_records: int


def count_remaining_duplicates(records: list[PaperRecord]) -> int:
    seen = set()
    duplicates = 0
    for record in records:
        keys = {
            f"id:{name.casefold()}:{value.casefold()}"
            for name, value in record.identifiers.items()
            if value.strip()
        }
        normalized_title = "".join(
            character for character in record.title.casefold() if character.isalnum()
        )
        if normalized_title:
            keys.add(f"title:{normalized_title}")
        if seen & keys:
            duplicates += 1
        seen.update(keys)
    return duplicates


def validate_topic_suite(topics: list[RetrievalBenchmarkTopic]) -> list[str]:
    errors = []
    if len(topics) != 20:
        errors.append(f"retrieval benchmark must contain 20 topics, found {len(topics)}")
    ids = [item.topic_id for item in topics]
    if len(ids) != len(set(ids)):
        errors.append("retrieval benchmark topic IDs must be unique")
    queries = [" ".join(item.query.casefold().split()) for item in topics]
    if len(queries) != len(set(queries)):
        errors.append("retrieval benchmark queries must be unique")
    return errors


def summarize_retrieval_results(
    results: list[TopicRetrievalResult], sources: list[str]
) -> dict[str, object]:
    attempts = len(results)
    success_rates = {
        source: (
            sum(result.source_success.get(source, False) for result in results) / attempts
            if attempts
            else 0.0
        )
        for source in sources
    }
    raw_records = sum(item.raw_source_records for item in results)
    deduplicated = sum(item.deduplicated_records for item in results)
    remaining_duplicates = sum(item.remaining_duplicate_records for item in results)
    duplicate_rate = remaining_duplicates / deduplicated if deduplicated else None
    serializable = sum(item.serializable_records for item in results)
    errors = []
    for source, rate in success_rates.items():
        if rate < 0.95:
            errors.append(f"{source} success rate is {rate:.1%}, below 95%")
    if duplicate_rate is None:
        errors.append("retrieval benchmark produced no records")
    elif duplicate_rate > 0.05:
        errors.append(f"post-dedup duplicate rate is {duplicate_rate:.1%}, above 5%")
    if serializable != deduplicated:
        errors.append("not every deduplicated record serialized successfully")
    return {
        "schema_version": "1.0",
        "topics": len(results),
        "source_success_rates": success_rates,
        "raw_source_records": raw_records,
        "deduplicated_records": deduplicated,
        "remaining_duplicate_records": remaining_duplicates,
        "post_dedup_duplicate_rate": duplicate_rate,
        "serializable_records": serializable,
        "publishable": not errors,
        "errors": errors,
    }


def run_retrieval_benchmark(
    topics: list[RetrievalBenchmarkTopic],
    sources: list[str],
    max_results: int,
    output_dir: Path,
) -> dict[str, object]:
    suite_errors = validate_topic_suite(topics)
    if suite_errors:
        return {"publishable": False, "errors": suite_errors, "topics": len(topics)}
    results = []
    for topic in topics:
        topic_dir = output_dir / topic.topic_id
        records_path = topic_dir / "papers.jsonl"
        failures_path = topic_dir / "failures.jsonl"
        manifest_path = topic_dir / "search.manifest.json"
        try:
            records, failures = search_sources(
                topic.query, sources, max_results, failures_path
            )
        except RetrievalError:
            records = []
            failures = []
            if failures_path.is_file():
                failures = [
                    json.loads(line)
                    for line in failures_path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
        if records:
            write_jsonl(records, records_path)
            create_search_manifest(
                topic.query,
                sources,
                max_results,
                records_path,
                failures_path,
                manifest_path,
                records,
                failures,
            )
        failed_sources = {item["source"] for item in failures}
        provenance_counts: Counter[str] = Counter()
        for record in records:
            provenance_counts.update({item.source for item in record.provenance})
        results.append(
            TopicRetrievalResult(
                topic_id=topic.topic_id,
                source_success={source: source not in failed_sources for source in sources},
                raw_source_records=sum(provenance_counts.values()),
                deduplicated_records=len(records),
                remaining_duplicate_records=count_remaining_duplicates(records),
                serializable_records=len(records),
            )
        )
    report = summarize_retrieval_results(results, sources)
    report["topic_results"] = [result.__dict__ for result in results]
    return report
