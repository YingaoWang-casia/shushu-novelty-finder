"""Human/LLM evaluation judgment schemas."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel
from shushu_novelty.schemas.lineage import RelationType

EvaluationSystem = Literal[
    "bare",
    "self-reflection",
    "shushu-v0.1",
    "shushu-v0.2",
    "researchstudio",
]


class RetrievalAssessment(StrictModel):
    known_prior_total: int = Field(ge=0)
    known_prior_retrieved_at_k: int = Field(ge=0)
    retrieved_records: int = Field(ge=0)
    duplicate_records: int = Field(ge=0)
    metadata_fields_total: int = Field(ge=0)
    metadata_fields_present: int = Field(ge=0)
    publication_labels_total: int = Field(ge=0)
    publication_labels_correct: int = Field(ge=0)

    @model_validator(mode="after")
    def counts_have_valid_denominators(self) -> RetrievalAssessment:
        pairs = [
            (self.known_prior_retrieved_at_k, self.known_prior_total, "known prior"),
            (self.duplicate_records, self.retrieved_records, "duplicate"),
            (self.metadata_fields_present, self.metadata_fields_total, "metadata"),
            (self.publication_labels_correct, self.publication_labels_total, "publication label"),
        ]
        for numerator, denominator, label in pairs:
            if numerator > denominator:
                raise ValueError(f"{label} numerator cannot exceed denominator")
        return self


class EvidenceAssessment(StrictModel):
    citations_total: int = Field(ge=0)
    citations_existing: int = Field(ge=0)
    claims_total: int = Field(ge=0)
    claims_entailed: int = Field(ge=0)
    unsupported_claims: int = Field(ge=0)
    strong_claims: int = Field(ge=0)
    full_text_verified_claims: int = Field(ge=0)

    @model_validator(mode="after")
    def evidence_counts_are_consistent(self) -> EvidenceAssessment:
        if self.citations_existing > self.citations_total:
            raise ValueError("existing citations cannot exceed citations_total")
        if self.claims_entailed > self.claims_total:
            raise ValueError("entailed claims cannot exceed claims_total")
        if self.unsupported_claims > self.claims_total:
            raise ValueError("unsupported claims cannot exceed claims_total")
        if self.full_text_verified_claims > self.strong_claims:
            raise ValueError("full-text verified claims cannot exceed strong_claims")
        return self


class IdeaQualityAssessment(StrictModel):
    problem_significance: int = Field(ge=1, le=5)
    novelty: int = Field(ge=1, le=5)
    method_specificity: int = Field(ge=1, le=5)
    feasibility: int = Field(ge=1, le=5)
    falsifiability: int = Field(ge=1, le=5)
    baseline_completeness: int = Field(ge=1, le=5)
    reviewer_defensibility: int = Field(ge=1, le=5)
    novelty_verdict: Literal["weak", "medium", "strong"]


class CalibrationAssessment(StrictModel):
    confidence: float = Field(ge=0.0, le=1.0)
    prediction_correct: bool
    is_scoop_case: bool
    scoop_detected: bool
    kill_recommended: bool
    kill_correct: bool


class RelationClassificationAssessment(StrictModel):
    relation: RelationType
    true_positive: int = Field(ge=0)
    false_positive: int = Field(ge=0)
    false_negative: int = Field(ge=0)


class LineageAssessment(StrictModel):
    relations: list[RelationClassificationAssessment] = Field(min_length=7, max_length=7)
    closest_prior_total: int = Field(ge=0)
    closest_prior_retrieved_at_5: int = Field(ge=0)
    saturated_contributions_predicted: int = Field(ge=0)
    saturated_contributions_correct: int = Field(ge=0)
    lineage_edges_total: int = Field(ge=0)
    unsupported_lineage_edges: int = Field(ge=0)

    @model_validator(mode="after")
    def lineage_counts_and_relation_coverage_are_valid(self) -> LineageAssessment:
        required_relations = {
            "ancestor",
            "closest-prior",
            "sibling",
            "follow-up",
            "benchmark",
            "contrary-evidence",
            "mechanism-transfer",
        }
        observed = [item.relation for item in self.relations]
        if len(observed) != len(set(observed)) or set(observed) != required_relations:
            raise ValueError("lineage assessment must contain every relation exactly once")
        pairs = [
            (self.closest_prior_retrieved_at_5, self.closest_prior_total, "closest prior"),
            (
                self.saturated_contributions_correct,
                self.saturated_contributions_predicted,
                "saturation",
            ),
            (self.unsupported_lineage_edges, self.lineage_edges_total, "unsupported edge"),
        ]
        for numerator, denominator, label in pairs:
            if numerator > denominator:
                raise ValueError(f"{label} numerator cannot exceed denominator")
        return self


class EvaluationJudgment(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    judgment_id: str = Field(pattern=r"^J-[A-Za-z0-9._:-]+$")
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    system: EvaluationSystem
    rater_id: str = Field(min_length=1)
    rater_type: Literal["human", "llm"]
    blind: bool
    research_experience_years: Optional[float] = Field(default=None, ge=0)
    retrieval: RetrievalAssessment
    evidence: EvidenceAssessment
    lineage: LineageAssessment
    idea: IdeaQualityAssessment
    calibration: CalibrationAssessment
    notes: str = ""

    @model_validator(mode="after")
    def human_raters_need_experience(self) -> EvaluationJudgment:
        if not self.blind:
            raise ValueError("benchmark judgments must be blind")
        if self.rater_type == "human" and self.research_experience_years is None:
            raise ValueError("human raters must report research_experience_years")
        return self


class PairwiseJudgment(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    pairwise_id: str = Field(pattern=r"^PW-[A-Za-z0-9._:-]+$")
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    system_left: EvaluationSystem
    system_right: EvaluationSystem
    preference: Literal["left", "right", "tie"]
    rater_id: str = Field(min_length=1)
    rater_type: Literal["human", "llm"]
    blind: bool
    research_experience_years: Optional[float] = Field(default=None, ge=0)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def pairwise_rating_is_blind_and_distinct(self) -> PairwiseJudgment:
        if self.system_left == self.system_right:
            raise ValueError("pairwise systems must be distinct")
        if not self.blind:
            raise ValueError("pairwise judgments must be blind")
        if self.rater_type == "human" and self.research_experience_years is None:
            raise ValueError("human raters must report research_experience_years")
        return self
