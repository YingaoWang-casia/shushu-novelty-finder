"""Research-gap records with explicit epistemic origin."""

from __future__ import annotations

from typing import List, Literal

from pydantic import Field

from shushu_novelty.schemas.base import StrictModel


class GapRecord(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    gap_id: str = Field(pattern=r"^G-[A-Za-z0-9._:-]+$")
    statement: str = Field(min_length=1)
    gap_type: Literal["author-limitation", "cross-paper-pattern", "model-inference"]
    evidence_claim_ids: List[str] = Field(min_length=1)
    blocked_by_paper_ids: List[str] = Field(default_factory=list)
    open_assumptions: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
