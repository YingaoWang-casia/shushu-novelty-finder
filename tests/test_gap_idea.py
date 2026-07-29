from shushu_novelty.evaluation.gap import validate_gaps
from shushu_novelty.evaluation.idea import validate_ideas
from shushu_novelty.schemas import (
    ClaimEvidence,
    EvidenceRef,
    GapRecord,
    IdeaCandidate,
    PaperRecord,
    Provenance,
)


def paper() -> PaperRecord:
    return PaperRecord(
        paper_id="P-fixture:1",
        title="Closest Paper",
        identifiers={"fixture": "1"},
        provenance=[Provenance(source="fixture", source_identifier="1", retrieved_at="now")],
    )


def claim() -> ClaimEvidence:
    return ClaimEvidence(
        claim_id="C-001",
        claim="The closest paper blocks the submitted mechanism.",
        origin="cross-paper-synthesis",
        strength="moderate",
        evidence=[
            EvidenceRef(
                paper_id="P-fixture:1",
                role="boundary",
                verification="metadata",
                confidence=0.7,
            )
        ],
    )


def gap() -> GapRecord:
    return GapRecord(
        gap_id="G-001",
        statement="A different assumption remains testable.",
        gap_type="cross-paper-pattern",
        evidence_claim_ids=["C-001"],
        blocked_by_paper_ids=["P-fixture:1"],
        open_assumptions=["dynamic corpus"],
        confidence=0.7,
    )


def idea() -> IdeaCandidate:
    return IdeaCandidate(
        idea_id="I-001",
        title="Dynamic-corpus audit",
        novelty_level="medium",
        task="RAG evaluation",
        mechanism="corpus-update intervention",
        supervision_or_data="versioned corpora",
        assumption="knowledge changes over time",
        evaluation="update robustness",
        application="knowledge-intensive QA",
        gap_ids=["G-001"],
        closest_prior_work=["P-fixture:1"],
        kill_criteria=["no effect under corpus updates"],
    )


def test_gap_and_idea_cross_record_chain_is_valid():
    assert validate_gaps([gap()], [paper()], [claim()]).ok
    assert validate_ideas([idea()], [gap()], [paper()]).ok


def test_gap_rejects_unknown_claim_and_blocking_paper():
    invalid = gap().model_copy(
        update={
            "evidence_claim_ids": ["C-missing"],
            "blocked_by_paper_ids": ["P-missing:1"],
        }
    )

    result = validate_gaps([invalid], [paper()], [claim()])

    assert not result.ok
    assert any("unknown claims" in error for error in result.errors)
    assert any("unknown blocking papers" in error for error in result.errors)


def test_idea_rejects_unknown_gap_and_closest_paper():
    invalid = idea().model_copy(
        update={"gap_ids": ["G-missing"], "closest_prior_work": ["P-missing:1"]}
    )

    result = validate_ideas([invalid], [gap()], [paper()])

    assert not result.ok
    assert any("unknown gaps" in error for error in result.errors)
    assert any("unknown closest papers" in error for error in result.errors)
