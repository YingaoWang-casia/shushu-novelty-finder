"""Persisted run-state schema."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Literal, Optional

from pydantic import Field

from shushu_novelty.schemas.base import StrictModel

RunMode = Literal["lineage", "idea", "full"]
PhaseStatus = Literal["pending", "ready", "complete", "failed"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class PhaseRecord(StrictModel):
    status: PhaseStatus = "pending"
    artifact: str
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    auxiliary_hashes: Dict[str, str] = Field(default_factory=dict)
    completed_at: Optional[str] = None
    error: Optional[str] = None


class RunState(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    run_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    topic_slug: str = Field(min_length=1)
    mode: RunMode
    created_at: str = Field(default_factory=utc_now)
    updated_at: str = Field(default_factory=utc_now)
    model: Optional[str] = None
    prompt_version: Optional[str] = None
    phases: Dict[str, PhaseRecord]
