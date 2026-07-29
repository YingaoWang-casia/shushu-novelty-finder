"""Structural report validation retained from the v0.1 script."""

from __future__ import annotations

import re
from dataclasses import dataclass

REQUIRED_PATTERNS = {
    "mode": r"(?i)\b(mode|input mode)\b",
    "scope": r"(?i)\b(research scope card|scope card|scope)\b",
    "papers": r"(?i)\b(representative papers|paper evidence|literature timeline|papers)\b",
    "trend": r"(?i)\b(trend matrix|timeline|trend)\b",
    "gap": r"(?i)\b(gap audit|gap type|research gap|gap)\b",
    "novelty": r"(?i)\b(weak|medium|strong)\b.*\b(novelty|idea|candidate)\b",
    "risk": r"(?i)\b(risk|failure|threat)\b",
    "experiment": r"(?i)\b(minimum experiment|experiment card|baseline|ablation)\b",
}

PAPER_MODE_PATTERNS = {
    "paper_thesis": r"(?i)\b(paper thesis|core claim|working title)\b",
    "baseline": r"(?i)\b(baseline|ablation)\b",
    "readiness": (
        r"(?i)\b(paper-readiness|readiness verdict|workshop-ready|main-track|pilot-ready)\b"
    ),
}

BAD_PATTERNS = {
    "unsupported_no_one": r"(?i)(no one has|nobody has|has not been studied|never been explored)",
    "vague_novel": r"(?i)\b(novel framework|novel method)\b",
}

NEGATED_WARNING_MARKERS = (
    "must not be claimed",
    "do not claim",
    "never claim",
    "no casual claim",
    "unsafe:",
    "unsafe wording",
)


@dataclass(frozen=True)
class StructuralResult:
    missing: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.missing


def _missing(text: str, patterns: dict[str, str]) -> list[str]:
    return [name for name, pattern in patterns.items() if not re.search(pattern, text, re.DOTALL)]


def _has_unnegated_match(text: str, pattern: str) -> bool:
    for match in re.finditer(pattern, text):
        context = text[max(0, match.start() - 100) : match.start()].casefold()
        if not any(marker in context for marker in NEGATED_WARNING_MARKERS):
            return True
    return False


def validate_report(
    text: str,
    paper_mode: bool = False,
    workflow_mode: str | None = None,
) -> StructuralResult:
    required = dict(REQUIRED_PATTERNS)
    if workflow_mode == "lineage":
        required.pop("novelty")
        required.pop("experiment")
    elif workflow_mode == "idea":
        required.pop("trend")
    missing = _missing(text, required)
    if paper_mode:
        missing.extend(_missing(text, PAPER_MODE_PATTERNS))
    warnings = [
        name for name, pattern in BAD_PATTERNS.items() if _has_unnegated_match(text, pattern)
    ]
    return StructuralResult(missing=missing, warnings=warnings)
