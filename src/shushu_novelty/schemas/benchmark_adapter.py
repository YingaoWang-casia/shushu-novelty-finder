"""External command adapters for reproducible baseline execution."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Literal

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel
from shushu_novelty.schemas.evaluation import EvaluationSystem


class BenchmarkAdapter(StrictModel):
    system: EvaluationSystem
    command: list[str] = Field(min_length=1)
    model: str = Field(min_length=1)
    timeout_seconds: float = Field(default=300.0, gt=0, le=3600)
    provenance_files: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def provenance_is_portable_and_hashed(self) -> BenchmarkAdapter:
        for name, digest in self.provenance_files.items():
            path = PurePosixPath(name)
            if not name.strip() or path.is_absolute() or ".." in path.parts:
                raise ValueError("adapter provenance paths must be portable relative paths")
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("adapter provenance values must be SHA-256")
        return self


class BenchmarkAdapterSet(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    adapters: list[BenchmarkAdapter] = Field(min_length=1)

    @model_validator(mode="after")
    def systems_are_unique(self) -> BenchmarkAdapterSet:
        systems = [item.system for item in self.adapters]
        if len(systems) != len(set(systems)):
            raise ValueError("benchmark adapter systems must be unique")
        return self
