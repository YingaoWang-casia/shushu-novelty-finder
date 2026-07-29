"""Final-report manifest contract."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Literal, Optional

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel


class ReportManifest(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    run_id: str = Field(min_length=1)
    mode: Literal["lineage", "idea", "full"]
    report_path: str = Field(min_length=1)
    report_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    input_artifact_hashes: dict[str, str] = Field(min_length=1)
    claim_ids: list[str] = Field(default_factory=list)
    failure_logs: list[str] = Field(default_factory=list)
    failure_log_hashes: dict[str, str] = Field(default_factory=dict)
    uncertainty_sections: list[str] = Field(min_length=1)
    known_limitations: list[str] = Field(min_length=1)
    effectiveness_claims: list[str] = Field(default_factory=list)
    public_evaluation_path: Optional[str] = None
    public_evaluation_sha256: Optional[str] = Field(default=None, pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def effectiveness_requires_public_evaluation(self) -> ReportManifest:
        if bool(self.public_evaluation_path) != bool(self.public_evaluation_sha256):
            raise ValueError("public evaluation path and hash must be provided together")
        if self.effectiveness_claims and not self.public_evaluation_path:
            raise ValueError("effectiveness claims require a hashed public evaluation report")
        if set(self.failure_logs) != self.failure_log_hashes.keys():
            raise ValueError("every failure log must have exactly one manifest hash")
        for path_value, digest in self.failure_log_hashes.items():
            path = PurePosixPath(path_value)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("failure log paths must be portable relative paths")
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("failure log hashes must be SHA-256")
        for name, digest in self.input_artifact_hashes.items():
            if not name.strip() or len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("input artifact hashes must map non-empty names to SHA-256")
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("input artifact hash keys must be portable relative paths")
        report_path = PurePosixPath(self.report_path)
        if report_path.is_absolute() or ".." in report_path.parts:
            raise ValueError("report path must be a portable relative path")
        required = {
            "intake/scope.json",
            "retrieval/papers.jsonl",
            "papers/fulltext.jsonl",
            "papers/claims.jsonl",
            "gaps/gaps.jsonl",
        }
        if self.mode in {"lineage", "full"}:
            required.add("lineage/graph.json")
        if self.mode in {"idea", "full"}:
            required.update(
                {
                    "ideas/ideas.jsonl",
                    "collision/collisions.json",
                    "audit/reviewer.json",
                }
            )
        missing = required - self.input_artifact_hashes.keys()
        if missing:
            raise ValueError(
                "report manifest is missing required input hashes: "
                + ", ".join(sorted(missing))
            )
        return self
