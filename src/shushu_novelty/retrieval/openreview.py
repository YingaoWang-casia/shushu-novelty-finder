"""OpenReview API v2 search connector."""

from __future__ import annotations

import urllib.parse
from datetime import datetime, timezone
from typing import Any

from shushu_novelty.errors import RetrievalError
from shushu_novelty.retrieval.http import get_json
from shushu_novelty.schemas import PaperRecord, Provenance

OPENREVIEW_API = "https://api2.openreview.net/notes/search"


def _value(content: dict[str, Any], key: str, default: Any = None) -> Any:
    value = content.get(key, default)
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def record_from_note(note: dict[str, Any], retrieved_at: str | None = None) -> PaperRecord:
    content = note.get("forumContent") or note.get("content") or {}
    forum_id = str(note.get("forum") or note.get("id") or "").strip()
    if not forum_id:
        raise RetrievalError("OpenReview note is missing forum/id")
    title = str(_value(content, "title", "") or "").strip()
    if not title:
        raise RetrievalError("OpenReview note has no submission title")
    abstract = str(_value(content, "abstract", "") or "").strip() or None
    authors_value = _value(content, "authors", []) or []
    authors = authors_value if isinstance(authors_value, list) else []
    venue = str(_value(content, "venue", "") or note.get("domain") or "OpenReview")
    year = None
    cdate = note.get("cdate") or note.get("tcdate")
    if isinstance(cdate, (int, float)):
        year = datetime.fromtimestamp(cdate / 1000, tz=timezone.utc).year
    url = f"https://openreview.net/forum?id={forum_id}"
    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    return PaperRecord(
        paper_id=f"P-openreview:{forum_id}",
        title=title,
        year=year,
        venue_or_source=venue,
        paper_type="conference-submission",
        identifiers={"openreview": forum_id},
        urls=[url],
        authors=[str(author) for author in authors],
        abstract=abstract,
        main_contribution=(abstract[:500] if abstract else "unknown"),
        why_relevant=(
            "matched OpenReview concurrent-work search; venue status requires verification"
        ),
        evidence_status="candidate",
        verification_level="abstract" if abstract else "metadata",
        evidence_roles=["concurrent-work"],
        confidence=0.35 if abstract else 0.2,
        provenance=[
            Provenance(
                source="openreview",
                source_identifier=forum_id,
                retrieved_at=timestamp,
                source_url=url,
            )
        ],
    )


def parse_search_response(payload: dict[str, Any], max_results: int) -> list[PaperRecord]:
    notes = payload.get("notes")
    if not isinstance(notes, list):
        raise RetrievalError("OpenReview response is missing notes")
    records: list[PaperRecord] = []
    seen_forums: set[str] = set()
    for note in notes:
        forum = str(note.get("forum") or note.get("id") or "")
        if not forum or forum in seen_forums:
            continue
        try:
            record = record_from_note(note)
        except RetrievalError:
            continue
        seen_forums.add(forum)
        records.append(record)
        if len(records) >= max_results:
            break
    return records


def search_openreview(
    query: str, max_results: int = 10, timeout: float = 30.0
) -> list[PaperRecord]:
    params = {"term": query, "limit": str(min(max_results * 5, 100))}
    payload = get_json(
        OPENREVIEW_API + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "shushu-novelty-finder/0.2"},
        timeout=timeout,
    )
    return parse_search_response(payload, max_results)
