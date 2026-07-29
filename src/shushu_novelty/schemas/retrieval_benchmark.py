"""Fixed retrieval-benchmark topic contract."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from shushu_novelty.schemas.base import StrictModel


class RetrievalBenchmarkTopic(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    topic_id: str = Field(pattern=r"^RT-\d{3}$")
    query: str = Field(min_length=5)
    domain: str = Field(min_length=1)
