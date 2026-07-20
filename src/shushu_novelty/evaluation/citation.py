"""Cross-record Claim-Evidence Ledger validation."""

from __future__ import annotations

import re
from dataclasses import dataclass

from shushu_novelty.schemas import ClaimEvidence, FullTextDocument, PaperRecord


@dataclass(frozen=True)
class CitationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _page_number(locator: str) -> int | None:
    match = re.search(r"(?i)\bpage\s*[:#]?\s*(\d+)\b", locator)
    return int(match.group(1)) if match else None


def validate_ledger(
    papers: list[PaperRecord],
    documents: list[FullTextDocument],
    claims: list[ClaimEvidence],
) -> CitationResult:
    paper_by_id = {paper.paper_id: paper for paper in papers}
    document_by_id = {document.paper_id: document for document in documents}
    errors = []
    warnings = []
    for claim in claims:
        if not claim.evidence:
            warnings.append(f"{claim.claim_id} has no evidence")
        for index, evidence in enumerate(claim.evidence, 1):
            prefix = f"{claim.claim_id} evidence {index}"
            paper = paper_by_id.get(evidence.paper_id)
            if paper is None:
                errors.append(f"{prefix} references unknown paper {evidence.paper_id}")
                continue
            if evidence.verification == "abstract" and not paper.abstract:
                errors.append(f"{prefix} claims abstract verification but paper has no abstract")
            if evidence.verification != "full-text":
                continue
            document = document_by_id.get(evidence.paper_id)
            if document is None:
                errors.append(f"{prefix} has no FullTextDocument")
                continue
            page_number = _page_number(evidence.locator or "")
            if page_number is None:
                errors.append(f"{prefix} locator must contain page number")
                continue
            if not 1 <= page_number <= document.page_count:
                errors.append(f"{prefix} points outside the PDF: page {page_number}")
                continue
            page = document.pages[page_number - 1]
            if evidence.passage_hash != page.text_sha256:
                errors.append(f"{prefix} passage hash does not match extracted page {page_number}")
            if evidence.section and page.section_hint and evidence.section != page.section_hint:
                warnings.append(
                    f"{prefix} section {evidence.section!r} differs from hint {page.section_hint!r}"
                )
    return CitationResult(errors=errors, warnings=warnings)
