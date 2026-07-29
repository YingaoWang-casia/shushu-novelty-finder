"""Cross-record research-gap evidence checks."""

from __future__ import annotations

from dataclasses import dataclass

from shushu_novelty.schemas import ClaimEvidence, GapRecord, PaperRecord


@dataclass(frozen=True)
class GapValidation:
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_gaps(
    gaps: list[GapRecord], papers: list[PaperRecord], claims: list[ClaimEvidence]
) -> GapValidation:
    errors = []
    gap_ids = [item.gap_id for item in gaps]
    if len(gap_ids) != len(set(gap_ids)):
        errors.append("gap IDs must be unique")
    paper_ids = {item.paper_id for item in papers}
    claim_by_id = {item.claim_id: item for item in claims}
    for gap in gaps:
        unknown_claims = set(gap.evidence_claim_ids) - claim_by_id.keys()
        if unknown_claims:
            errors.append(
                f"gap {gap.gap_id} references unknown claims: "
                + ", ".join(sorted(unknown_claims))
            )
        unknown_papers = set(gap.blocked_by_paper_ids) - paper_ids
        if unknown_papers:
            errors.append(
                f"gap {gap.gap_id} references unknown blocking papers: "
                + ", ".join(sorted(unknown_papers))
            )
        evidence_papers = set()
        for claim_id in gap.evidence_claim_ids:
            claim = claim_by_id.get(claim_id)
            if claim is not None:
                evidence_papers.update(reference.paper_id for reference in claim.evidence)
        uncovered = set(gap.blocked_by_paper_ids) - evidence_papers
        if uncovered:
            errors.append(
                f"gap {gap.gap_id} has blocking papers without claim evidence: "
                + ", ".join(sorted(uncovered))
            )
    return GapValidation(errors=errors)
