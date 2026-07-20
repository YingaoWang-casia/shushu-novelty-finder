"""arXiv connector producing canonical PaperRecord objects."""

from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from datetime import datetime, timezone
from typing import List

from shushu_novelty.errors import RetrievalError
from shushu_novelty.schemas import PaperRecord, Provenance

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"


def _text(parent: ET.Element, tag: str, default: str = "") -> str:
    node = parent.find(tag)
    if node is None or node.text is None:
        return default
    return " ".join(node.text.split())


def _year(entry: ET.Element) -> int | None:
    published = _text(entry, ATOM_NS + "published")
    match = re.search(r"\b(19|20)\d{2}\b", published)
    return int(match.group(0)) if match else None


def _arxiv_id(entry: ET.Element) -> str:
    entry_id = _text(entry, ATOM_NS + "id")
    identifier = entry_id.rsplit("/", 1)[-1]
    return re.sub(r"v\d+$", "", identifier)


def record_from_entry(entry: ET.Element, retrieved_at: str | None = None) -> PaperRecord:
    arxiv_id = _arxiv_id(entry)
    if not arxiv_id:
        raise RetrievalError("arXiv entry is missing an identifier")
    primary_category = entry.find(ARXIV_NS + "primary_category")
    task = (
        primary_category.attrib.get("term", "unknown")
        if primary_category is not None
        else "unknown"
    )
    authors = [_text(author, ATOM_NS + "name") for author in entry.findall(ATOM_NS + "author")]
    authors = [author for author in authors if author]
    url = f"https://arxiv.org/abs/{arxiv_id}"
    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    abstract = _text(entry, ATOM_NS + "summary") or None
    contribution = abstract or "unknown"
    if len(contribution) > 500:
        contribution = contribution[:497].rstrip() + "..."
    return PaperRecord(
        paper_id=f"P-arxiv:{arxiv_id}",
        title=_text(entry, ATOM_NS + "title", "unknown"),
        year=_year(entry),
        venue_or_source="arXiv",
        paper_type="preprint",
        identifiers={"arxiv": arxiv_id},
        urls=[url],
        authors=authors,
        task=task,
        abstract=abstract,
        main_contribution=contribution,
        why_relevant="matched arXiv query; verify before using as claim evidence",
        evidence_status="candidate",
        verification_level="abstract" if abstract else "metadata",
        evidence_roles=["task-anchor"],
        confidence=0.35 if abstract else 0.2,
        provenance=[
            Provenance(
                source="arxiv",
                source_identifier=arxiv_id,
                retrieved_at=timestamp,
                source_url=url,
            )
        ],
    )


def parse_feed(payload: bytes, retrieved_at: str | None = None) -> List[PaperRecord]:
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise RetrievalError(f"arXiv returned invalid XML: {exc}") from exc
    return [record_from_entry(entry, retrieved_at) for entry in root.findall(ATOM_NS + "entry")]


def build_url(
    query: str,
    max_results: int = 10,
    start: int = 0,
    sort_by: str = "relevance",
    sort_order: str = "descending",
) -> str:
    params = {
        "search_query": "all:" + query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    return ARXIV_API + "?" + urllib.parse.urlencode(params)


def search_arxiv(
    query: str,
    max_results: int = 10,
    start: int = 0,
    sort_by: str = "relevance",
    sort_order: str = "descending",
    timeout: float = 30.0,
) -> List[PaperRecord]:
    url = build_url(query, max_results, start, sort_by, sort_order)
    request = urllib.request.Request(url, headers={"User-Agent": "shushu-novelty-finder/0.2"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
    except Exception as exc:
        raise RetrievalError(f"arXiv request failed: {exc}") from exc
    return parse_feed(payload)


def as_legacy_records(records: Iterable[PaperRecord]) -> list[dict[str, object]]:
    """Preserve the v0.1 script contract during package migration."""

    result = []
    for record in records:
        result.append(
            {
                "title": record.title,
                "year": str(record.year) if record.year else "unknown",
                "venue_or_source": record.venue_or_source,
                "paper_type": record.paper_type,
                "url_or_identifier": next(iter(record.identifiers.values())),
                "task": record.task,
                "dataset": record.datasets[0] if record.datasets else "unknown",
                "metric": record.metrics[0] if record.metrics else "unknown",
                "main_contribution": record.main_contribution,
                "why_relevant": record.why_relevant,
                "evidence_status": record.evidence_status,
                "evidence_role": ", ".join(record.evidence_roles) or "unknown",
                "used_to_support_which_claim": ", ".join(record.supported_claim_ids)
                or "candidate only; do not use until verified",
                "confidence": "weak" if record.confidence < 0.5 else "moderate",
            }
        )
    return result
