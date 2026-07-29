"""Cross-record lineage evidence validation."""

from __future__ import annotations

from dataclasses import dataclass

from shushu_novelty.schemas import ClaimEvidence, LineageGraph, PaperRecord


@dataclass(frozen=True)
class LineageResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_lineage(
    graph: LineageGraph,
    papers: list[PaperRecord],
    claims: list[ClaimEvidence],
) -> LineageResult:
    paper_by_id = {paper.paper_id: paper for paper in papers}
    claim_by_id = {claim.claim_id: claim for claim in claims}
    errors = []
    warnings = []
    for node in graph.nodes:
        if node.paper_id not in paper_by_id:
            errors.append(f"lineage node references unknown paper {node.paper_id}")
    for edge in graph.edges:
        evidence_papers = set()
        for claim_id in edge.evidence_claim_ids:
            claim = claim_by_id.get(claim_id)
            if claim is None:
                errors.append(f"edge {edge.edge_id} references unknown claim {claim_id}")
                continue
            evidence_papers.update(item.paper_id for item in claim.evidence)
        required = {edge.source_paper_id, edge.target_paper_id}
        missing = required - evidence_papers
        if missing:
            errors.append(
                f"edge {edge.edge_id} evidence does not cover papers: {', '.join(sorted(missing))}"
            )
        source = paper_by_id.get(edge.source_paper_id)
        target = paper_by_id.get(edge.target_paper_id)
        if (
            edge.relation in {"ancestor", "closest-prior", "follow-up"}
            and source
            and target
            and source.year
            and target.year
            and source.year > target.year
        ):
            warnings.append(
                f"edge {edge.edge_id} points from newer paper {source.year} to older {target.year}"
            )
    for item in graph.saturation:
        evidence_papers = set()
        for claim_id in item.evidence_claim_ids:
            claim = claim_by_id.get(claim_id)
            if claim is None:
                errors.append(
                    f"saturation {item.saturation_id} references unknown claim {claim_id}"
                )
                continue
            evidence_papers.update(ref.paper_id for ref in claim.evidence)
        missing = set(item.paper_ids) - evidence_papers
        if missing:
            errors.append(
                f"saturation {item.saturation_id} evidence does not cover papers: "
                + ", ".join(sorted(missing))
            )
    return LineageResult(errors=errors, warnings=warnings)
