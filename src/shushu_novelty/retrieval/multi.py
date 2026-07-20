"""Concurrent multi-source retrieval with durable failure records."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from shushu_novelty.errors import RetrievalError
from shushu_novelty.retrieval.arxiv import search_arxiv
from shushu_novelty.retrieval.dedup import deduplicate
from shushu_novelty.retrieval.openalex import search_openalex
from shushu_novelty.retrieval.openreview import search_openreview
from shushu_novelty.retrieval.semantic_scholar import search_semantic_scholar
from shushu_novelty.schemas import PaperRecord

SearchFunction = Callable[[str, int], list[PaperRecord]]
SOURCE_FUNCTIONS: dict[str, SearchFunction] = {
    "arxiv": search_arxiv,
    "openalex": search_openalex,
    "semantic-scholar": search_semantic_scholar,
    "openreview": search_openreview,
}


def _failure(source: str, query: str, error: str) -> dict[str, str]:
    return {
        "schema_version": "1.0",
        "source": source,
        "query": query,
        "error": error,
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }


def write_failures(failures: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in failures)
    path.write_text(text, encoding="utf-8")


def search_sources(
    query: str,
    sources: list[str],
    max_results: int = 10,
    failure_log: Path | None = None,
    *,
    arxiv_start: int = 0,
    arxiv_sort_by: str = "relevance",
    arxiv_sort_order: str = "descending",
) -> tuple[list[PaperRecord], list[dict[str, str]]]:
    unknown = sorted(set(sources) - SOURCE_FUNCTIONS.keys())
    if unknown:
        raise RetrievalError(f"unknown retrieval sources: {', '.join(unknown)}")
    records_by_source: dict[str, list[PaperRecord]] = {}
    failures: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=min(len(sources), 4)) as executor:
        futures = {}
        for source in sources:
            if source == "arxiv" and SOURCE_FUNCTIONS[source] is search_arxiv:
                future = executor.submit(
                    search_arxiv,
                    query,
                    max_results,
                    arxiv_start,
                    arxiv_sort_by,
                    arxiv_sort_order,
                )
            else:
                future = executor.submit(SOURCE_FUNCTIONS[source], query, max_results)
            futures[future] = source
        for future in as_completed(futures):
            source = futures[future]
            try:
                records = future.result()
                if not records:
                    failures.append(_failure(source, query, "source returned zero results"))
                else:
                    records_by_source[source] = records
            except Exception as exc:
                failures.append(_failure(source, query, str(exc)))
    failures.sort(key=lambda item: item["source"])
    if failure_log is not None:
        write_failures(failures, failure_log)
    ordered_records = [record for source in sources for record in records_by_source.get(source, [])]
    if not ordered_records:
        details = "; ".join(f"{item['source']}: {item['error']}" for item in failures)
        raise RetrievalError(f"all retrieval sources failed or returned empty: {details}")
    return deduplicate(ordered_records), failures
