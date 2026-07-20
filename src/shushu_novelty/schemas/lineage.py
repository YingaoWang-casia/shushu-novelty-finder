"""Lineage graph and contribution-saturation schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from shushu_novelty.schemas.base import StrictModel

RelationType = Literal[
    "ancestor",
    "closest-prior",
    "sibling",
    "follow-up",
    "benchmark",
    "contrary-evidence",
    "mechanism-transfer",
]


class LineageNode(StrictModel):
    paper_id: str = Field(pattern=r"^P-[A-Za-z0-9._:-]+$")
    method_family: str = Field(min_length=1)
    assumptions: list[str] = Field(default_factory=list)
    contributions: list[str] = Field(min_length=1)


class LineageEdge(StrictModel):
    edge_id: str = Field(pattern=r"^E-[A-Za-z0-9._:-]+$")
    source_paper_id: str = Field(pattern=r"^P-[A-Za-z0-9._:-]+$")
    target_paper_id: str = Field(pattern=r"^P-[A-Za-z0-9._:-]+$")
    relation: RelationType
    rationale: str = Field(min_length=1)
    evidence_claim_ids: list[str] = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


class SaturationRecord(StrictModel):
    saturation_id: str = Field(pattern=r"^S-[A-Za-z0-9._:-]+$")
    contribution: str = Field(min_length=1)
    status: Literal["open", "emerging", "saturated", "blocked"]
    paper_ids: list[str] = Field(min_length=1)
    evidence_claim_ids: list[str] = Field(min_length=1)
    blocked_idea_space: list[str] = Field(default_factory=list)
    open_idea_space: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def saturated_contributions_need_multiple_papers(self) -> SaturationRecord:
        if self.status in {"saturated", "blocked"} and len(set(self.paper_ids)) < 2:
            raise ValueError("saturated/blocked contributions require at least two papers")
        return self


class LineageGraph(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    nodes: list[LineageNode] = Field(min_length=1)
    edges: list[LineageEdge] = Field(default_factory=list)
    saturation: list[SaturationRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_graph_integrity(self) -> LineageGraph:
        node_ids = [node.paper_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("lineage node paper_ids must be unique")
        known = set(node_ids)
        edge_ids = [edge.edge_id for edge in self.edges]
        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("lineage edge_ids must be unique")
        for edge in self.edges:
            if edge.source_paper_id not in known or edge.target_paper_id not in known:
                raise ValueError(f"edge {edge.edge_id} references a paper outside nodes")
            if edge.source_paper_id == edge.target_paper_id:
                raise ValueError(f"edge {edge.edge_id} must not be a self-edge")
        return self
