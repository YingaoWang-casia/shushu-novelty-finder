"""Novelty-candidate portfolio schemas."""

from __future__ import annotations

from typing import List, Literal

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel


class IdeaCandidate(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    idea_id: str = Field(pattern=r"^I-[A-Za-z0-9._:-]+$")
    title: str = Field(min_length=1)
    novelty_level: Literal["weak", "medium", "strong"]
    task: str = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    supervision_or_data: str = Field(min_length=1)
    assumption: str = Field(min_length=1)
    evaluation: str = Field(min_length=1)
    application: str = Field(min_length=1)
    gap_ids: List[str] = Field(min_length=1)
    closest_prior_work: List[str] = Field(default_factory=list)
    kill_criteria: List[str] = Field(min_length=1)
    status: Literal["proposed", "pass", "revise", "downgrade", "abandon"] = "proposed"

    @model_validator(mode="after")
    def novelty_needs_prior_work(self) -> IdeaCandidate:
        if not self.closest_prior_work:
            raise ValueError("every idea requires closest prior work")
        return self
