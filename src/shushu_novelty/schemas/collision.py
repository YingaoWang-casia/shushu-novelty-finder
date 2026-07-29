"""Independent novelty-collision audit schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel

CollisionAxis = Literal[
    "task",
    "mechanism",
    "supervision-data",
    "assumption",
    "evaluation",
    "application",
]
ALL_COLLISION_AXES = {
    "task",
    "mechanism",
    "supervision-data",
    "assumption",
    "evaluation",
    "application",
}


class CollisionQueries(StrictModel):
    problem: list[str] = Field(min_length=1)
    mechanism_signature: list[str] = Field(min_length=1)
    escape_mechanism: list[str] = Field(min_length=1)


class AxisOverlap(StrictModel):
    axis: CollisionAxis
    overlap: Literal["none", "partial", "full"]
    rationale: str = Field(min_length=1)
    evidence_claim_ids: list[str] = Field(min_length=1)


class PriorComparison(StrictModel):
    paper_id: str = Field(pattern=r"^P-[A-Za-z0-9._:-]+$")
    axes: list[AxisOverlap] = Field(min_length=6, max_length=6)
    collision_risk: Literal["low", "medium", "high"]

    @model_validator(mode="after")
    def every_axis_exactly_once(self) -> PriorComparison:
        axes = [item.axis for item in self.axes]
        if len(axes) != len(set(axes)) or set(axes) != ALL_COLLISION_AXES:
            raise ValueError("comparison must contain every collision axis exactly once")
        return self


class CollisionAudit(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    audit_id: str = Field(pattern=r"^A-[A-Za-z0-9._:-]+$")
    idea_id: str = Field(pattern=r"^I-[A-Za-z0-9._:-]+$")
    generator_context_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    auditor_context_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    queries: CollisionQueries
    comparisons: list[PriorComparison] = Field(min_length=3, max_length=7)
    decision: Literal["pass", "revise", "downgrade", "abandon"]
    rationale: str = Field(min_length=1)
    structural_rewrite_count: int = Field(default=0, ge=0, le=1)

    @model_validator(mode="after")
    def independent_context_and_decision(self) -> CollisionAudit:
        if self.generator_context_hash == self.auditor_context_hash:
            raise ValueError("generator and auditor contexts must be isolated")
        paper_ids = [comparison.paper_id for comparison in self.comparisons]
        if len(paper_ids) != len(set(paper_ids)):
            raise ValueError("collision comparisons must use distinct prior papers")
        if self.decision == "pass" and any(
            comparison.collision_risk == "high" for comparison in self.comparisons
        ):
            raise ValueError("an audit with high collision risk cannot pass")
        return self


class CollisionBatch(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    audits: list[CollisionAudit] = Field(min_length=1)

    @model_validator(mode="after")
    def audit_and_idea_ids_are_unique(self) -> CollisionBatch:
        audit_ids = [item.audit_id for item in self.audits]
        idea_ids = [item.idea_id for item in self.audits]
        if len(audit_ids) != len(set(audit_ids)):
            raise ValueError("collision audit IDs must be unique")
        if len(idea_ids) != len(set(idea_ids)):
            raise ValueError("each idea may have only one collision audit")
        return self
