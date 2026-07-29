"""Cross-artifact checks for independent simulated review."""

from __future__ import annotations

from dataclasses import dataclass

from shushu_novelty.schemas import (
    ClaimEvidence,
    CollisionBatch,
    IdeaCandidate,
    ReviewerBatch,
)


@dataclass(frozen=True)
class ReviewerResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_reviewer_batch(
    batch: ReviewerBatch,
    ideas: list[IdeaCandidate],
    collisions: CollisionBatch,
    claims: list[ClaimEvidence],
) -> ReviewerResult:
    idea_by_id = {item.idea_id: item for item in ideas}
    collision_by_id = {item.audit_id: item for item in collisions.audits}
    claim_ids = {item.claim_id for item in claims}
    errors = []
    warnings = []
    seen_ideas = set()
    for audit in batch.audits:
        if audit.idea_id in seen_ideas:
            errors.append(f"idea {audit.idea_id} has more than one reviewer audit")
        seen_ideas.add(audit.idea_id)
        idea = idea_by_id.get(audit.idea_id)
        if idea is None:
            errors.append(f"review {audit.review_id} references unknown idea {audit.idea_id}")
        collision = collision_by_id.get(audit.collision_audit_id)
        if collision is None:
            errors.append(
                f"review {audit.review_id} references unknown collision audit "
                f"{audit.collision_audit_id}"
            )
        else:
            if collision.idea_id != audit.idea_id:
                errors.append(
                    f"review {audit.review_id} and collision {collision.audit_id} "
                    "refer to different ideas"
                )
            if audit.reviewer_context_hash in {
                collision.generator_context_hash,
                collision.auditor_context_hash,
            }:
                errors.append(
                    f"review {audit.review_id} must use a context isolated from generation "
                    "and collision audit"
                )
            if collision.decision == "abandon" and audit.final_decision == "pass":
                errors.append(
                    f"review {audit.review_id} cannot pass an idea abandoned by collision audit"
                )
        referenced_claims = set(audit.supporting_claim_ids)
        for objection in audit.objections:
            referenced_claims.update(objection.evidence_claim_ids)
        unknown_claims = referenced_claims - claim_ids
        if unknown_claims:
            errors.append(
                f"review {audit.review_id} references unknown claims: "
                + ", ".join(sorted(unknown_claims))
            )
        if idea is not None and idea.status == "abandon" and audit.final_decision == "pass":
            errors.append(f"review {audit.review_id} passes an already abandoned idea")
        if audit.final_decision == "abandon" and audit.revision is not None:
            warnings.append(
                f"review {audit.review_id} abandoned the idea after consuming its one revision"
            )
    missing_reviews = idea_by_id.keys() - seen_ideas
    if missing_reviews:
        errors.append(
            "ideas missing reviewer audits: " + ", ".join(sorted(missing_reviews))
        )
    return ReviewerResult(errors=errors, warnings=warnings)
