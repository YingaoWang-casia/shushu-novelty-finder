"""Claim-to-evidence ledger schemas."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel


class EvidenceRef(StrictModel):
    paper_id: str = Field(pattern=r"^P-[A-Za-z0-9._:-]+$")
    role: Literal["support", "counter", "boundary", "background"]
    verification: Literal["metadata", "abstract", "full-text"]
    section: Optional[str] = None
    locator: Optional[str] = None
    passage_hash: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def full_text_needs_locator(self) -> EvidenceRef:
        if self.verification == "full-text" and (not self.locator or not self.passage_hash):
            raise ValueError("full-text evidence requires locator and passage_hash")
        return self


class ClaimEvidence(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    claim_id: str = Field(pattern=r"^C-[A-Za-z0-9._:-]+$")
    claim: str = Field(min_length=1)
    origin: Literal["author-statement", "cross-paper-synthesis", "model-inference"]
    strength: Literal["weak", "moderate", "strong"]
    evidence: List[EvidenceRef] = Field(default_factory=list)

    @model_validator(mode="after")
    def strong_claims_need_full_text(self) -> ClaimEvidence:
        if not self.evidence:
            raise ValueError("every claim requires at least one traceable evidence reference")
        if self.strength == "strong" and not any(
            item.role == "support" and item.verification == "full-text" for item in self.evidence
        ):
            raise ValueError("strong claims require at least one full-text support reference")
        return self
