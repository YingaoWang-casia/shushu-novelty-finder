"""Build and verify portable retrieval replay manifests."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from shushu_novelty.errors import InputError
from shushu_novelty.io import load_json, sha256_file, validate_jsonl
from shushu_novelty.schemas import PaperRecord, SearchManifest


def _portable_path(path: Path, manifest_path: Path) -> str:
    try:
        return path.resolve().relative_to(manifest_path.parent.resolve()).as_posix()
    except ValueError as exc:
        raise InputError(
            f"replay artifact {path} must be inside manifest directory {manifest_path.parent}"
        ) from exc


def create_search_manifest(
    query: str,
    sources: list[str],
    max_results: int,
    records_path: Path,
    failure_log: Path,
    manifest_path: Path,
    records: list[PaperRecord],
    failures: list[dict[str, str]],
    arxiv_start: int = 0,
    arxiv_sort_by: str = "relevance",
    arxiv_sort_order: str = "descending",
) -> SearchManifest:
    counts: Counter[str] = Counter()
    for record in records:
        counts.update({item.source for item in record.provenance})
    manifest = SearchManifest(
        query=query,
        sources=sources,
        max_results_per_source=max_results,
        arxiv_start=arxiv_start,
        arxiv_sort_by=arxiv_sort_by,
        arxiv_sort_order=arxiv_sort_order,
        records_path=_portable_path(records_path, manifest_path),
        records_sha256=sha256_file(records_path),
        records_count=len(records),
        failure_log_path=_portable_path(failure_log, manifest_path),
        failure_log_sha256=sha256_file(failure_log),
        failure_count=len(failures),
        source_record_counts=dict(sorted(counts.items())),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    manifest.write_json(manifest_path)
    return manifest


def replay_search(
    manifest_path: Path,
) -> tuple[SearchManifest, list[PaperRecord], list[dict[str, object]]]:
    manifest = SearchManifest.model_validate(load_json(manifest_path))
    records_path = manifest_path.parent / manifest.records_path
    failure_path = manifest_path.parent / manifest.failure_log_path
    if not records_path.is_file() or sha256_file(records_path) != manifest.records_sha256:
        raise InputError("retrieval records are missing or do not match replay manifest hash")
    if not failure_path.is_file() or sha256_file(failure_path) != manifest.failure_log_sha256:
        raise InputError("retrieval failure log is missing or does not match replay manifest hash")
    records = validate_jsonl(records_path, PaperRecord)
    failures = []
    for line_number, line in enumerate(failure_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InputError(
                f"invalid failure JSONL in {failure_path} at line {line_number}: {exc}"
            ) from exc
        required = {"source", "query", "error", "occurred_at"}
        if not isinstance(item, dict) or not required.issubset(item):
            raise InputError(f"invalid failure record in {failure_path} at line {line_number}")
        failures.append(item)
    if len(records) != manifest.records_count:
        raise InputError("retrieval record count does not match replay manifest")
    if len(failures) != manifest.failure_count:
        raise InputError("retrieval failure count does not match replay manifest")
    return manifest, records, failures
