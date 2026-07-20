"""Canonical paper and provenance records."""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import Field, HttpUrl, model_validator

from shushu_novelty.schemas.base import StrictModel

EvidenceStatus = Literal["candidate", "verified", "model-supplied", "placeholder"]
VerificationLevel = Literal["metadata", "abstract", "full-text"]


class Provenance(StrictModel):
    source: str = Field(min_length=1)
    source_identifier: str = Field(min_length=1)
    retrieved_at: str = Field(min_length=1)
    source_url: Optional[HttpUrl] = None


class PaperRecord(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    paper_id: str = Field(pattern=r"^P-[A-Za-z0-9._:-]+$")
    title: str = Field(min_length=1)
    year: Optional[int] = Field(default=None, ge=1400, le=2200)
    venue_or_source: str = "unknown"
    paper_type: str = "unknown"
    identifiers: Dict[str, str]
    urls: List[HttpUrl] = Field(default_factory=list)
    authors: List[str] = Field(default_factory=list)
    task: str = "unknown"
    datasets: List[str] = Field(default_factory=list)
    metrics: List[str] = Field(default_factory=list)
    abstract: Optional[str] = None
    main_contribution: str = "unknown"
    why_relevant: str = "unknown"
    evidence_status: EvidenceStatus = "candidate"
    verification_level: VerificationLevel = "metadata"
    evidence_roles: List[str] = Field(default_factory=list)
    supported_claim_ids: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.25, ge=0.0, le=1.0)
    provenance: List[Provenance]

    @model_validator(mode="after")
    def enforce_evidence_invariants(self) -> PaperRecord:
        if not self.identifiers:
            raise ValueError("at least one canonical identifier is required")
        if not self.provenance:
            raise ValueError("at least one provenance record is required")
        if self.verification_level == "full-text" and self.evidence_status != "verified":
            raise ValueError("full-text verification requires evidence_status='verified'")
        return self
