import pytest
from pydantic import ValidationError

from shushu_novelty.evaluation.collision import validate_collision, validate_collision_batch
from shushu_novelty.schemas import (
    AxisOverlap,
    ClaimEvidence,
    CollisionAudit,
    CollisionBatch,
    CollisionQueries,
    EvidenceRef,
    IdeaCandidate,
    PaperRecord,
    PriorComparison,
    Provenance,
)

AXES = ["task", "mechanism", "supervision-data", "assumption", "evaluation", "application"]


def paper(index: int) -> PaperRecord:
    paper_id = f"P-example:{index}"
    return PaperRecord(
        paper_id=paper_id,
        title=f"Prior {index}",
        identifiers={"example": str(index)},
        abstract="prior work",
        provenance=[Provenance(source="example", source_identifier=str(index), retrieved_at="now")],
    )


def claim(index: int) -> ClaimEvidence:
    return ClaimEvidence(
        claim_id=f"C-prior-{index}",
        claim=f"Prior {index} axis evidence",
        origin="cross-paper-synthesis",
        strength="moderate",
        evidence=[
            EvidenceRef(
                paper_id=f"P-example:{index}",
                role="support",
                verification="abstract",
                confidence=0.7,
            )
        ],
    )


def comparison(index: int, full_axes: set[str], risk: str) -> PriorComparison:
    return PriorComparison(
        paper_id=f"P-example:{index}",
        axes=[
            AxisOverlap(
                axis=axis,
                overlap="full" if axis in full_axes else "none",
                rationale=f"{axis} comparison",
                evidence_claim_ids=[f"C-prior-{index}"],
            )
            for axis in AXES
        ],
        collision_risk=risk,
    )


def idea() -> IdeaCandidate:
    return IdeaCandidate(
        idea_id="I-001",
        title="Candidate",
        novelty_level="strong",
        task="task",
        mechanism="mechanism",
        supervision_or_data="data",
        assumption="assumption",
        evaluation="evaluation",
        application="new application",
        gap_ids=["G-001"],
        closest_prior_work=["P-example:1"],
        kill_criteria=["no gain"],
    )


def audit(decision: str, first: PriorComparison) -> CollisionAudit:
    return CollisionAudit(
        audit_id="A-001",
        idea_id="I-001",
        generator_context_hash="a" * 64,
        auditor_context_hash="b" * 64,
        queries=CollisionQueries(
            problem=["problem query"],
            mechanism_signature=["mechanism query"],
            escape_mechanism=["escape query"],
        ),
        comparisons=[
            first,
            comparison(2, set(), "low"),
            comparison(3, {"task"}, "low"),
        ],
        decision=decision,
        rationale="audit decision",
    )


def test_scooped_idea_can_be_downgraded():
    full = set(AXES)
    result = validate_collision(
        audit("downgrade", comparison(1, full, "high")),
        idea(),
        [paper(1), paper(2), paper(3)],
        [claim(1), claim(2), claim(3)],
    )
    assert result.ok


def test_application_only_transfer_cannot_pass_as_strong():
    same_except_application = set(AXES) - {"application"}
    result = validate_collision(
        audit("pass", comparison(1, same_except_application, "medium")),
        idea(),
        [paper(1), paper(2), paper(3)],
        [claim(1), claim(2), claim(3)],
    )
    assert not result.ok
    assert any("only by application" in error for error in result.errors)


def test_auditor_context_must_be_isolated():
    with pytest.raises(ValidationError, match="contexts must be isolated"):
        CollisionAudit(
            audit_id="A-001",
            idea_id="I-001",
            generator_context_hash="a" * 64,
            auditor_context_hash="a" * 64,
            queries=CollisionQueries(
                problem=["problem"],
                mechanism_signature=["mechanism"],
                escape_mechanism=["escape"],
            ),
            comparisons=[
                comparison(1, set(), "low"),
                comparison(2, set(), "low"),
                comparison(3, set(), "low"),
            ],
            decision="pass",
            rationale="invalid shared context",
        )


def test_every_idea_requires_exactly_one_collision_audit():
    first_idea = idea()
    second_idea = first_idea.model_copy(
        update={"idea_id": "I-002", "title": "Unreviewed candidate"}
    )
    batch = CollisionBatch(
        audits=[audit("downgrade", comparison(1, set(AXES), "high"))]
    )

    result = validate_collision_batch(
        batch,
        [first_idea, second_idea],
        [paper(1), paper(2), paper(3)],
        [claim(1), claim(2), claim(3)],
    )

    assert not result.ok
    assert any("I-002" in error and "missing collision" in error for error in result.errors)
