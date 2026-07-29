"""Paper Evidence Card rendering for legacy and canonical records."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

LEGACY_FIELDS = [
    "title",
    "year",
    "venue_or_source",
    "paper_type",
    "url_or_identifier",
    "task",
    "dataset",
    "metric",
    "main_contribution",
    "why_relevant",
    "evidence_status",
    "evidence_role",
    "used_to_support_which_claim",
    "confidence",
]


def normalize_legacy(record: Mapping[str, Any]) -> dict[str, str]:
    return {field: str(record.get(field, "unknown")).replace("\n", " ") for field in LEGACY_FIELDS}


def to_markdown(records: Iterable[Mapping[str, Any]]) -> str:
    lines = ["# Paper Evidence Cards", ""]
    for index, record in enumerate(records, 1):
        card = normalize_legacy(record)
        lines.extend([f"## Paper {index}: {card['title']}", ""])
        for field in LEGACY_FIELDS:
            lines.append(f"- **{field.replace('_', ' ').title()}:** {card[field]}")
        lines.append("")
    return "\n".join(lines)
