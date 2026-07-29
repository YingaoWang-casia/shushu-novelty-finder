"""Contracts that keep system identity out of human-rating files."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel
from shushu_novelty.schemas.evaluation import (
    CalibrationAssessment,
    EvaluationSystem,
    EvidenceAssessment,
    IdeaQualityAssessment,
    LineageAssessment,
    RetrievalAssessment,
)


class BlindOutputAssignment(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    assignment_id: str = Field(pattern=r"^BA-[A-Za-z0-9._:-]+$")
    rater_id: str = Field(min_length=1)
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    output_id: str = Field(pattern=r"^O-[a-f0-9]{16}$")
    output_path: str = Field(min_length=1)
    output_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class BlindPairwiseAssignment(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    assignment_id: str = Field(pattern=r"^BPA-[A-Za-z0-9._:-]+$")
    rater_id: str = Field(min_length=1)
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    output_left: str = Field(pattern=r"^O-[a-f0-9]{16}$")
    output_right: str = Field(pattern=r"^O-[a-f0-9]{16}$")
    path_left: str = Field(min_length=1)
    path_right: str = Field(min_length=1)
    sha256_left: str = Field(pattern=r"^[a-f0-9]{64}$")
    sha256_right: str = Field(pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def outputs_are_distinct(self) -> BlindPairwiseAssignment:
        if self.output_left == self.output_right:
            raise ValueError("blind pairwise outputs must be distinct")
        return self


class BlindOutputKey(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    rater_id: str = Field(min_length=1)
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    output_id: str = Field(pattern=r"^O-[a-f0-9]{16}$")
    system: EvaluationSystem
    source_output_path: str = Field(min_length=1)
    output_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class BlindScalarResponse(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    assignment_id: str = Field(pattern=r"^BA-[A-Za-z0-9._:-]+$")
    rater_id: str = Field(min_length=1)
    research_experience_years: float = Field(ge=0)
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    output_id: str = Field(pattern=r"^O-[a-f0-9]{16}$")
    retrieval: RetrievalAssessment
    evidence: EvidenceAssessment
    lineage: LineageAssessment
    idea: IdeaQualityAssessment
    calibration: CalibrationAssessment
    notes: str = ""


class BlindPairwiseResponse(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    assignment_id: str = Field(pattern=r"^BPA-[A-Za-z0-9._:-]+$")
    rater_id: str = Field(min_length=1)
    research_experience_years: float = Field(ge=0)
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    output_left: str = Field(pattern=r"^O-[a-f0-9]{16}$")
    output_right: str = Field(pattern=r"^O-[a-f0-9]{16}$")
    preference: Literal["left", "right", "tie"]
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def outputs_are_distinct(self) -> BlindPairwiseResponse:
        if self.output_left == self.output_right:
            raise ValueError("blind pairwise response outputs must be distinct")
        return self


class BlindResponseLock(StrictModel):
    """Rater-side commitment created before any identity mapping is revealed."""

    schema_version: Literal["1.0"] = "1.0"
    rater_id: str = Field(min_length=1)
    research_experience_years: float = Field(ge=0)
    locked_at: str = Field(min_length=1)
    blind_manifest_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    scalar_assignments_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    pairwise_assignments_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    scalar_response_filename: str = Field(pattern=r"^[^/\\]+$")
    scalar_responses: int = Field(ge=1)
    scalar_responses_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    pairwise_response_filename: str = Field(pattern=r"^[^/\\]+$")
    pairwise_responses: int = Field(ge=1)
    pairwise_responses_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
