"""Semantic Scholar Academic Graph connector."""

from __future__ import annotations

import os
import urllib.parse
from datetime import datetime, timezone
from typing import Any

from shushu_novelty.errors import RetrievalError
from shushu_novelty.retrieval.http import get_json
from shushu_novelty.schemas import PaperRecord, Provenance

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_BULK_API = SEMANTIC_SCHOLAR_API + "/bulk"
FIELDS = ",".join(
    [
        "paperId",
        "externalIds",
        "title",
        "abstract",
        "venue",
        "year",
        "publicationVenue",
        "publicationTypes",
        "openAccessPdf",
        "authors",
    ]
)


def _relaxed_bulk_query(query: str) -> str:
    """Relax an over-constrained natural-language query once, without an unbounded OR."""
    terms = query.split()
    if len(terms) < 4:
        return query
    return " ".join(terms[: (len(terms) + 1) // 2])


def record_from_paper(paper: dict[str, Any], retrieved_at: str | None = None) -> PaperRecord:
    semantic_id = str(paper.get("paperId") or "").strip()
    if not semantic_id:
        raise RetrievalError("Semantic Scholar paper is missing paperId")
    external = paper.get("externalIds") or {}
    identifiers = {"semantic_scholar": semantic_id}
    mapping = {"DOI": "doi", "ArXiv": "arxiv", "DBLP": "dblp", "CorpusId": "corpus_id"}
    for source_key, target_key in mapping.items():
        value = external.get(source_key)
        if value:
            identifiers[target_key] = str(value).lower() if target_key == "doi" else str(value)
    publication_venue = paper.get("publicationVenue") or {}
    venue = paper.get("venue") or publication_venue.get("name") or "Semantic Scholar"
    publication_types = paper.get("publicationTypes") or []
    paper_type = publication_types[0] if publication_types else "unknown"
    abstract = paper.get("abstract") or None
    authors = [item.get("name", "") for item in paper.get("authors") or []]
    authors = [author for author in authors if author]
    open_pdf = paper.get("openAccessPdf") or {}
    semantic_url = f"https://www.semanticscholar.org/paper/{semantic_id}"
    urls = [semantic_url]
    if str(open_pdf.get("url") or "").startswith("http"):
        urls.append(open_pdf["url"])
    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    return PaperRecord(
        paper_id=f"P-semanticscholar:{semantic_id}",
        title=paper.get("title") or "unknown",
        year=paper.get("year"),
        venue_or_source=venue,
        paper_type=paper_type,
        identifiers=identifiers,
        urls=urls,
        authors=authors,
        abstract=abstract,
        main_contribution=(abstract[:500] if abstract else "unknown"),
        why_relevant="matched Semantic Scholar paper search; verify before claim use",
        evidence_status="candidate",
        verification_level="abstract" if abstract else "metadata",
        evidence_roles=["cs-recall"],
        confidence=0.4 if abstract else 0.25,
        provenance=[
            Provenance(
                source="semantic-scholar",
                source_identifier=semantic_id,
                retrieved_at=timestamp,
                source_url=semantic_url,
            )
        ],
    )


def search_semantic_scholar(
    query: str,
    max_results: int = 10,
    api_key: str | None = None,
    timeout: float = 30.0,
) -> list[PaperRecord]:
    key = api_key or os.environ.get("SEMANTICSCHOLAR_API_KEY")
    params = {
        "query": query.replace("-", " "),
        "fields": FIELDS,
    }
    endpoint = SEMANTIC_SCHOLAR_API
    if key:
        params["limit"] = str(min(max_results, 100))
    else:
        # Semantic Scholar recommends the less resource-intensive bulk endpoint for
        # most keyword searches. Anonymous relevance-search traffic shares a heavily
        # throttled pool; bulk remains a real API search and avoids turning an
        # optional credential into a functional requirement. Its default paper-ID
        # ordering is not useful for discovery, so prefer highly cited matches.
        endpoint = SEMANTIC_SCHOLAR_BULK_API
        params["sort"] = "citationCount:desc"
    headers = {"User-Agent": "shushu-novelty-finder/0.2"}
    if key:
        headers["x-api-key"] = key
    request_kwargs: dict[str, Any] = {"headers": headers, "timeout": timeout}
    if not key:
        # The anonymous pool is shared. A slightly wider bounded retry window covers
        # transient bulk throttles while still surfacing durable failures.
        request_kwargs["retries"] = 4
    payload = get_json(endpoint + "?" + urllib.parse.urlencode(params), **request_kwargs)
    results = payload.get("data")
    if not isinstance(results, list):
        raise RetrievalError("Semantic Scholar response is missing data")
    if not results and not key:
        relaxed_query = _relaxed_bulk_query(params["query"])
        if relaxed_query != params["query"]:
            params["query"] = relaxed_query
            payload = get_json(
                endpoint + "?" + urllib.parse.urlencode(params), **request_kwargs
            )
            results = payload.get("data")
            if not isinstance(results, list):
                raise RetrievalError("Semantic Scholar response is missing data")
    return [record_from_paper(paper) for paper in results[:max_results]]
