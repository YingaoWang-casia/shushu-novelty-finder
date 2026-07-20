import json

import pytest

from shushu_novelty.errors import InputError
from shushu_novelty.io import write_jsonl
from shushu_novelty.retrieval.replay import create_search_manifest, replay_search
from shushu_novelty.schemas import PaperRecord, Provenance


def paper() -> PaperRecord:
    return PaperRecord(
        paper_id="P-arxiv:1234.56789",
        title="Replay Fixture",
        identifiers={"arxiv": "1234.56789"},
        abstract="Serializable fixture.",
        provenance=[
            Provenance(
                source="arxiv",
                source_identifier="1234.56789",
                retrieved_at="2026-07-16T00:00:00+00:00",
            )
        ],
    )


def test_retrieval_manifest_replays_exact_hashed_artifacts(tmp_path):
    records_path = tmp_path / "papers.jsonl"
    failures_path = tmp_path / "failures.jsonl"
    manifest_path = tmp_path / "search.manifest.json"
    write_jsonl([paper()], records_path)
    failure = {
        "source": "openalex",
        "query": "fixture",
        "error": "missing key",
        "occurred_at": "2026-07-16T00:00:00+00:00",
    }
    failures_path.write_text(json.dumps(failure) + "\n", encoding="utf-8")
    create_search_manifest(
        "fixture",
        ["arxiv", "openalex"],
        10,
        records_path,
        failures_path,
        manifest_path,
        [paper()],
        [failure],
    )

    manifest, records, failures = replay_search(manifest_path)

    assert manifest.records_path == "papers.jsonl"
    assert records[0].paper_id == "P-arxiv:1234.56789"
    assert failures[0]["source"] == "openalex"


def test_replay_rejects_tampered_records(tmp_path):
    records_path = tmp_path / "papers.jsonl"
    failures_path = tmp_path / "failures.jsonl"
    manifest_path = tmp_path / "search.manifest.json"
    write_jsonl([paper()], records_path)
    failures_path.write_text("", encoding="utf-8")
    create_search_manifest(
        "fixture",
        ["arxiv"],
        10,
        records_path,
        failures_path,
        manifest_path,
        [paper()],
        [],
    )
    records_path.write_text("{}\n", encoding="utf-8")

    with pytest.raises(InputError, match="do not match replay manifest hash"):
        replay_search(manifest_path)
