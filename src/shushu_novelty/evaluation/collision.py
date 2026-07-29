"""Cross-record novelty collision checks."""

from __future__ import annotations

from dataclasses import dataclass

from shushu_novelty.schemas import (
    ClaimEvidence,
    CollisionAudit,
    CollisionBatch,
    IdeaCandidate,
    PaperRecord,
)


@dataclass(frozen=True)
class CollisionResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_collision_batch(
    batch: CollisionBatch,
    ideas: list[IdeaCandidate],
    papers: list[PaperRecord],
    claims: list[ClaimEvidence],
) -> CollisionResult:
    idea_by_id = {item.idea_id: item for item in ideas}
    errors = []
    warnings = []
    for audit in batch.audits:
        idea = idea_by_id.get(audit.idea_id)
        if idea is None:
            errors.append(f"audit {audit.audit_id} references unknown idea {audit.idea_id}")
            continue
        result = validate_collision(audit, idea, papers, claims)
        errors.extend(result.errors)
        warnings.extend(result.warnings)
    missing_audits = idea_by_id.keys() - {audit.idea_id for audit in batch.audits}
    if missing_audits:
        errors.append("ideas missing collision audits: " + ", ".join(sorted(missing_audits)))
    return CollisionResult(errors=errors, warnings=warnings)


def validate_collision(
    audit: CollisionAudit,
    idea: IdeaCandidate,
    papers: list[PaperRecord],
    claims: list[ClaimEvidence],
) -> CollisionResult:
    paper_ids = {paper.paper_id for paper in papers}
    claim_by_id = {claim.claim_id: claim for claim in claims}
    errors = []
    warnings = []
    if audit.idea_id != idea.idea_id:
        errors.append(f"audit {audit.audit_id} does not match idea {idea.idea_id}")
    decision_status = {
        "pass": "pass",
        "revise": "revise",
        "downgrade": "downgrade",
        "abandon": "abandon",
    }
    if idea.status != "proposed" and idea.status != decision_status[audit.decision]:
        errors.append(f"idea status {idea.status} conflicts with audit decision {audit.decision}")

    for comparison in audit.comparisons:
        if comparison.paper_id not in paper_ids:
            errors.append(f"audit comparison references unknown paper {comparison.paper_id}")
        covered_claims = set()
        for axis in comparison.axes:
            for claim_id in axis.evidence_claim_ids:
                claim = claim_by_id.get(claim_id)
                if claim is None:
                    message = (
                        f"comparison {comparison.paper_id}/{axis.axis} "
                        f"references unknown claim {claim_id}"
                    )
                    errors.append(message)
                    continue
                if any(ref.paper_id == comparison.paper_id for ref in claim.evidence):
                    covered_claims.add(claim_id)
                else:
                    errors.append(
                        f"claim {claim_id} does not cover compared paper {comparison.paper_id}"
                    )
        if not covered_claims:
            errors.append(f"comparison {comparison.paper_id} has no paper-grounded claims")

        overlaps = {item.axis: item.overlap for item in comparison.axes}
        full_axes = {axis for axis, overlap in overlaps.items() if overlap == "full"}
        scooped = {"task", "mechanism"}.issubset(full_axes) and len(full_axes) >= 4
        application_only = full_axes == {
            "task",
            "mechanism",
            "supervision-data",
            "assumption",
            "evaluation",
        }
        if scooped and audit.decision == "pass":
            errors.append(
                f"audit passes idea despite scoop-level overlap with {comparison.paper_id}"
            )
        if application_only and idea.novelty_level == "strong" and audit.decision == "pass":
            errors.append(
                f"strong idea differs from {comparison.paper_id} only by application "
                "and cannot pass"
            )
    if audit.decision == "abandon" and audit.structural_rewrite_count == 1:
        warnings.append("abandoned idea has consumed its one allowed structural rewrite")
    return CollisionResult(errors=errors, warnings=warnings)
