"""Serializable retrieval replay manifest."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Literal

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel


class SearchManifest(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    query: str = Field(min_length=1)
    sources: list[
        Literal["arxiv", "openalex", "semantic-scholar", "openreview"]
    ] = Field(min_length=1)
    max_results_per_source: int = Field(ge=1)
    arxiv_start: int = Field(default=0, ge=0)
    arxiv_sort_by: Literal["relevance", "lastUpdatedDate", "submittedDate"] = "relevance"
    arxiv_sort_order: Literal["ascending", "descending"] = "descending"
    records_path: str = Field(min_length=1)
    records_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    records_count: int = Field(ge=1)
    failure_log_path: str = Field(min_length=1)
    failure_log_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    failure_count: int = Field(ge=0)
    source_record_counts: dict[str, int]
    created_at: str = Field(min_length=1)

    @model_validator(mode="after")
    def paths_are_portable_and_sources_unique(self) -> SearchManifest:
        for value in [self.records_path, self.failure_log_path]:
            path = PurePosixPath(value)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("replay manifest paths must be relative and cannot contain '..'")
        if len(self.sources) != len(set(self.sources)):
            raise ValueError("replay manifest sources must be unique")
        if any(count < 0 for count in self.source_record_counts.values()):
            raise ValueError("source record counts cannot be negative")
        return self
