from shushu_novelty.evaluation.lineage import validate_lineage
from shushu_novelty.schemas import (
    ClaimEvidence,
    EvidenceRef,
    LineageEdge,
    LineageGraph,
    LineageNode,
    PaperRecord,
    Provenance,
    SaturationRecord,
)


def paper(paper_id: str, year: int) -> PaperRecord:
    return PaperRecord(
        paper_id=paper_id,
        title=paper_id,
        year=year,
        identifiers={"example": paper_id},
        abstract="abstract",
        provenance=[Provenance(source="example", source_identifier=paper_id, retrieved_at="now")],
    )


def claim(*paper_ids: str) -> ClaimEvidence:
    return ClaimEvidence(
        claim_id="C-relation",
        claim="The second paper follows the first mechanism.",
        origin="cross-paper-synthesis",
        strength="moderate",
        evidence=[
            EvidenceRef(
                paper_id=paper_id,
                role="support",
                verification="abstract",
                confidence=0.7,
            )
            for paper_id in paper_ids
        ],
    )


def graph() -> LineageGraph:
    return LineageGraph(
        nodes=[
            LineageNode(
                paper_id="P-example:A",
                method_family="retrieval",
                contributions=["base mechanism"],
            ),
            LineageNode(
                paper_id="P-example:B",
                method_family="retrieval",
                contributions=["follow-up mechanism"],
            ),
        ],
        edges=[
            LineageEdge(
                edge_id="E-A-B",
                source_paper_id="P-example:A",
                target_paper_id="P-example:B",
                relation="ancestor",
                rationale="B extends A",
                evidence_claim_ids=["C-relation"],
                confidence=0.8,
            )
        ],
        saturation=[
            SaturationRecord(
                saturation_id="S-retrieval",
                contribution="basic retrieval",
                status="saturated",
                paper_ids=["P-example:A", "P-example:B"],
                evidence_claim_ids=["C-relation"],
                blocked_idea_space=["repeat basic retrieval"],
                open_idea_space=["dynamic corpus assumptions"],
            )
        ],
    )


def test_lineage_evidence_covers_both_edge_endpoints():
    papers = [paper("P-example:A", 2020), paper("P-example:B", 2022)]
    result = validate_lineage(graph(), papers, [claim("P-example:A", "P-example:B")])
    assert result.ok
    assert not result.warnings


def test_lineage_rejects_unsupported_endpoint():
    papers = [paper("P-example:A", 2020), paper("P-example:B", 2022)]
    result = validate_lineage(graph(), papers, [claim("P-example:A")])
    assert not result.ok
    assert any("P-example:B" in error for error in result.errors)
