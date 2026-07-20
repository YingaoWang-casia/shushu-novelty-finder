import json

import pytest

from shushu_novelty.errors import RetrievalError
from shushu_novelty.retrieval import multi
from shushu_novelty.schemas import PaperRecord, Provenance


def record(source: str) -> PaperRecord:
    return PaperRecord(
        paper_id=f"P-{source}:1",
        title=f"Paper from {source}",
        identifiers={source: "1"},
        provenance=[
            Provenance(source=source, source_identifier="1", retrieved_at="2026-07-16T00:00:00Z")
        ],
    )


def test_partial_failure_is_durable(monkeypatch, tmp_path):
    monkeypatch.setattr(
        multi,
        "SOURCE_FUNCTIONS",
        {
            "good": lambda query, limit: [record("good")],
            "bad": lambda query, limit: (_ for _ in ()).throw(RetrievalError("rate limited")),
        },
    )
    failure_log = tmp_path / "failures.jsonl"
    records, failures = multi.search_sources("query", ["good", "bad"], 5, failure_log)
    assert len(records) == 1
    assert failures[0]["source"] == "bad"
    assert json.loads(failure_log.read_text())["error"] == "rate limited"


def test_all_failures_raise_after_writing_log(monkeypatch, tmp_path):
    monkeypatch.setattr(
        multi,
        "SOURCE_FUNCTIONS",
        {"bad": lambda query, limit: (_ for _ in ()).throw(RetrievalError("offline"))},
    )
    failure_log = tmp_path / "failures.jsonl"
    with pytest.raises(RetrievalError, match="all retrieval sources failed"):
        multi.search_sources("query", ["bad"], 5, failure_log)
    assert failure_log.exists()


def test_arxiv_pagination_and_sort_options_are_forwarded(monkeypatch):
    captured = {}

    def fake_arxiv(query, limit, start, sort_by, sort_order):
        captured.update(
            query=query,
            limit=limit,
            start=start,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return [record("arxiv")]

    monkeypatch.setattr(multi, "search_arxiv", fake_arxiv)
    monkeypatch.setitem(multi.SOURCE_FUNCTIONS, "arxiv", fake_arxiv)

    records, failures = multi.search_sources(
        "query",
        ["arxiv"],
        7,
        arxiv_start=20,
        arxiv_sort_by="submittedDate",
        arxiv_sort_order="ascending",
    )

    assert len(records) == 1
    assert failures == []
    assert captured == {
        "query": "query",
        "limit": 7,
        "start": 20,
        "sort_by": "submittedDate",
        "sort_order": "ascending",
    }
