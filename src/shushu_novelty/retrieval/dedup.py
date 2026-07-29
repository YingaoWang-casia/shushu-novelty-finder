"""Cross-source paper identity resolution."""

from __future__ import annotations

import re
import unicodedata

from shushu_novelty.schemas import PaperRecord

IDENTIFIER_PRIORITY = ["doi", "arxiv", "openreview", "dblp", "semantic_scholar", "openalex"]
GENERIC_VENUES = {"arxiv", "openalex", "semantic scholar", "openreview", "unknown"}


def normalize_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title).casefold()
    return re.sub(r"[^a-z0-9]+", " ", normalized).strip()


def identity_keys(record: PaperRecord) -> list[str]:
    keys = []
    for name in IDENTIFIER_PRIORITY:
        value = record.identifiers.get(name)
        if value:
            keys.append(f"{name}:{value.casefold().strip()}")
    title = normalize_title(record.title)
    if title:
        keys.append(f"title:{record.year or 'unknown'}:{title}")
        keys.append(f"title-only:{title}")
    return keys


def _paper_type_score(value: str) -> int:
    lowered = value.casefold()
    if "journal" in lowered or "conference" in lowered:
        return 3
    if "article" in lowered or "proceedings" in lowered:
        return 2
    if "preprint" in lowered or "posted" in lowered or "submission" in lowered:
        return 1
    return 0


def merge_records(left: PaperRecord, right: PaperRecord) -> PaperRecord:
    preferred, other = (
        (right, left)
        if (_paper_type_score(right.paper_type), right.confidence)
        > (_paper_type_score(left.paper_type), left.confidence)
        else (left, right)
    )
    data = preferred.model_dump(mode="json")
    identifiers = dict(left.identifiers)
    identifiers.update(
        {key: value for key, value in right.identifiers.items() if key not in identifiers}
    )
    data["identifiers"] = identifiers
    data["urls"] = list(
        dict.fromkeys([*(str(url) for url in left.urls), *(str(url) for url in right.urls)])
    )
    data["authors"] = list(dict.fromkeys([*preferred.authors, *other.authors]))
    data["datasets"] = list(dict.fromkeys([*left.datasets, *right.datasets]))
    data["metrics"] = list(dict.fromkeys([*left.metrics, *right.metrics]))
    data["evidence_roles"] = list(dict.fromkeys([*left.evidence_roles, *right.evidence_roles]))
    data["supported_claim_ids"] = list(
        dict.fromkeys([*left.supported_claim_ids, *right.supported_claim_ids])
    )
    provenance = [*left.provenance, *right.provenance]
    seen_provenance: set[tuple[str, str]] = set()
    data["provenance"] = []
    for item in provenance:
        key = (item.source, item.source_identifier)
        if key not in seen_provenance:
            data["provenance"].append(item.model_dump(mode="json"))
            seen_provenance.add(key)
    if len(other.abstract or "") > len(preferred.abstract or ""):
        data["abstract"] = other.abstract
        data["main_contribution"] = other.main_contribution
        data["verification_level"] = other.verification_level
    if preferred.venue_or_source.casefold() in GENERIC_VENUES:
        data["venue_or_source"] = other.venue_or_source
    data["confidence"] = max(left.confidence, right.confidence)
    return PaperRecord.model_validate(data)


def deduplicate(records: list[PaperRecord]) -> list[PaperRecord]:
    merged: list[PaperRecord] = []
    key_to_index: dict[str, int] = {}
    for record in records:
        matching = {key_to_index[key] for key in identity_keys(record) if key in key_to_index}
        if not matching:
            index = len(merged)
            merged.append(record)
        else:
            index = min(matching)
            merged[index] = merge_records(merged[index], record)
            for duplicate_index in sorted(matching - {index}, reverse=True):
                merged[index] = merge_records(merged[index], merged[duplicate_index])
                del merged[duplicate_index]
                key_to_index = {
                    key: (value - 1 if value > duplicate_index else value)
                    for key, value in key_to_index.items()
                    if value != duplicate_index
                }
        for key in identity_keys(merged[index]):
            key_to_index[key] = index
    return merged
