"""OpenAlex Works connector."""

from __future__ import annotations

import os
import urllib.parse
from datetime import datetime, timezone
from typing import Any

from shushu_novelty.errors import RetrievalError
from shushu_novelty.retrieval.http import get_json
from shushu_novelty.schemas import PaperRecord, Provenance

OPENALEX_API = "https://api.openalex.org/works"
SELECT = (
    "id,title,doi,publication_year,type,abstract_inverted_index,authorships,"
    "primary_location,best_oa_location,ids,primary_topic"
)


def reconstruct_abstract(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None
    positions = {position: word for word, values in index.items() for position in values}
    return " ".join(positions[position] for position in sorted(positions)) or None


def _clean_identifier(value: object, prefix: str = "") -> str:
    text = str(value or "").strip()
    if prefix and text.lower().startswith(prefix.lower()):
        text = text[len(prefix) :]
    return text


def record_from_work(work: dict[str, Any], retrieved_at: str | None = None) -> PaperRecord:
    openalex_id = _clean_identifier(work.get("id")).rsplit("/", 1)[-1]
    if not openalex_id:
        raise RetrievalError("OpenAlex work is missing id")
    identifiers = {"openalex": openalex_id}
    ids = work.get("ids") or {}
    doi = _clean_identifier(work.get("doi") or ids.get("doi"), "https://doi.org/").lower()
    if doi:
        identifiers["doi"] = doi
    arxiv = _clean_identifier(ids.get("arxiv"))
    if arxiv:
        arxiv = arxiv.rsplit("/", 1)[-1].removesuffix(".pdf")
        identifiers["arxiv"] = arxiv

    primary = work.get("primary_location") or {}
    source = primary.get("source") or {}
    best_oa = work.get("best_oa_location") or {}
    raw_urls = [
        work.get("id"),
        work.get("doi"),
        primary.get("landing_page_url"),
        best_oa.get("pdf_url"),
    ]
    urls = list(dict.fromkeys(str(url) for url in raw_urls if str(url or "").startswith("http")))
    authors = [
        item.get("author", {}).get("display_name", "") for item in work.get("authorships") or []
    ]
    authors = [author for author in authors if author]
    topic = work.get("primary_topic") or {}
    task = topic.get("display_name") or "unknown"
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
    paper_type = work.get("type") or "unknown"
    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    return PaperRecord(
        paper_id=f"P-openalex:{openalex_id}",
        title=work.get("title") or "unknown",
        year=work.get("publication_year"),
        venue_or_source=source.get("display_name") or "OpenAlex",
        paper_type=paper_type,
        identifiers=identifiers,
        urls=urls,
        authors=authors,
        task=task,
        abstract=abstract,
        main_contribution=(abstract[:500] if abstract else "unknown"),
        why_relevant="matched OpenAlex full-text metadata search; verify before claim use",
        evidence_status="candidate",
        verification_level="abstract" if abstract else "metadata",
        evidence_roles=["broad-recall"],
        confidence=0.4 if abstract else 0.25,
        provenance=[
            Provenance(
                source="openalex",
                source_identifier=openalex_id,
                retrieved_at=timestamp,
                source_url=work.get("id") or f"https://openalex.org/{openalex_id}",
            )
        ],
    )


def search_openalex(
    query: str,
    max_results: int = 10,
    api_key: str | None = None,
    timeout: float = 30.0,
) -> list[PaperRecord]:
    key = api_key or os.environ.get("OPENALEX_API_KEY")
    if not key:
        raise RetrievalError("OpenAlex requires OPENALEX_API_KEY")
    params = {
        "search": query,
        "per_page": str(min(max_results, 100)),
        "sort": "relevance_score:desc",
        "select": SELECT,
        "api_key": key,
    }
    payload = get_json(
        OPENALEX_API + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "shushu-novelty-finder/0.2"},
        timeout=timeout,
    )
    results = payload.get("results")
    if not isinstance(results, list):
        raise RetrievalError("OpenAlex response is missing results")
    return [record_from_work(work) for work in results[:max_results]]
