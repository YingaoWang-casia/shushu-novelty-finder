"""Independent simulated-review and one-revision contracts."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel


class ReviewerObjection(StrictModel):
    category: Literal[
        "novelty",
        "significance",
        "technical-correctness",
        "evaluation",
        "feasibility",
        "evidence",
    ]
    severity: Literal["low", "medium", "high", "fatal"]
    objection: str = Field(min_length=1)
    evidence_claim_ids: list[str] = Field(min_length=1)
    response: str = Field(min_length=1)
    status: Literal["resolved", "mitigated", "open"]


class RevisionRecord(StrictModel):
    revision_number: Literal[1] = 1
    before_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    after_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    structural_change: str = Field(min_length=1)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def revision_must_change_the_candidate(self) -> RevisionRecord:
        if self.before_hash == self.after_hash:
            raise ValueError("structural revision must change the candidate hash")
        return self


class ReviewerAudit(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    review_id: str = Field(pattern=r"^R-[A-Za-z0-9._:-]+$")
    idea_id: str = Field(pattern=r"^I-[A-Za-z0-9._:-]+$")
    collision_audit_id: str = Field(pattern=r"^A-[A-Za-z0-9._:-]+$")
    reviewer_context_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    strongest_reason_for: str = Field(min_length=1)
    strongest_reason_against: str = Field(min_length=1)
    supporting_claim_ids: list[str] = Field(min_length=1)
    objections: list[ReviewerObjection] = Field(min_length=3)
    kill_triggers: list[str] = Field(min_length=1)
    initial_decision: Literal["pass", "revise", "abandon"]
    revision: Optional[RevisionRecord] = None
    final_decision: Literal["pass", "abandon"]
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_one_revision_and_fatal_gate(self) -> ReviewerAudit:
        if self.initial_decision == "revise" and self.revision is None:
            raise ValueError("a revise decision requires exactly one structural revision")
        if self.initial_decision != "revise" and self.revision is not None:
            raise ValueError("revision is only allowed after an initial revise decision")
        if self.initial_decision == "abandon" and self.final_decision != "abandon":
            raise ValueError("an initially abandoned idea cannot later pass")
        blocking = [
            objection
            for objection in self.objections
            if objection.status == "open" and objection.severity in {"high", "fatal"}
        ]
        if blocking and self.final_decision == "pass":
            raise ValueError("open high/fatal objections prevent a final pass")
        if any(
            objection.severity == "fatal" for objection in self.objections
        ) and self.final_decision != "abandon":
            raise ValueError("fatal reviewer objections require abandonment")
        return self


class ReviewerBatch(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    audits: list[ReviewerAudit] = Field(min_length=1)

    @model_validator(mode="after")
    def review_and_idea_ids_are_unique(self) -> ReviewerBatch:
        review_ids = [item.review_id for item in self.audits]
        idea_ids = [item.idea_id for item in self.audits]
        if len(review_ids) != len(set(review_ids)):
            raise ValueError("review IDs must be unique")
        if len(idea_ids) != len(set(idea_ids)):
            raise ValueError("each idea may have only one reviewer audit")
        return self
