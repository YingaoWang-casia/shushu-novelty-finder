"""Benchmark seed and run-matrix schemas."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel

BenchmarkCaseType = Literal[
    "broad-direction",
    "seed-paper",
    "known-scoop",
    "mechanism-transfer",
]

BenchmarkDomain = Literal[
    "llm-rag",
    "cv-multimodal",
    "speech",
    "agents",
    "systems",
    "data-mining",
    "security",
    "scientific-ml",
]


class BenchmarkReference(StrictModel):
    source: Literal["openreview", "arxiv", "doi", "other"]
    identifier: str = Field(min_length=1)
    title: str = Field(min_length=1)


class BenchmarkSeed(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    case_type: BenchmarkCaseType
    domain: BenchmarkDomain
    prompt: str = Field(min_length=10)
    reference: Optional[BenchmarkReference] = None
    candidate_idea: Optional[str] = None
    known_prior_ids: list[str] = Field(default_factory=list)
    expected_behavior: list[str] = Field(min_length=1)
    provenance: str = Field(min_length=1)
    leakage_risk: Literal["low", "medium", "high"] = "low"

    @model_validator(mode="after")
    def case_requirements(self) -> BenchmarkSeed:
        if self.case_type == "seed-paper" and self.reference is None:
            raise ValueError("seed-paper cases require a reference")
        if self.case_type == "known-scoop" and (
            not self.candidate_idea or not self.known_prior_ids
        ):
            raise ValueError("known-scoop cases require candidate_idea and known_prior_ids")
        if self.case_type == "mechanism-transfer" and not self.candidate_idea:
            raise ValueError("mechanism-transfer cases require candidate_idea")
        return self


class BenchmarkRun(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    run_id: str = Field(min_length=1)
    seed_id: str = Field(pattern=r"^B-\d{3}$")
    system: Literal["bare", "self-reflection", "shushu-v0.1", "shushu-v0.2", "researchstudio"]
    status: Literal["pending", "complete", "failed"] = "pending"
    output_path: str = Field(min_length=1)
    model: Optional[str] = None
    prompt_hash: Optional[str] = None
    adapter_sha256: Optional[str] = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    output_sha256: Optional[str] = Field(default=None, pattern=r"^[a-f0-9]{64}$")
