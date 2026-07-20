import pytest
from pydantic import ValidationError

from shushu_novelty.evaluation.reviewer import validate_reviewer_batch
from shushu_novelty.schemas import (
    AxisOverlap,
    ClaimEvidence,
    CollisionAudit,
    CollisionBatch,
    CollisionQueries,
    EvidenceRef,
    IdeaCandidate,
    PriorComparison,
    ReviewerAudit,
    ReviewerBatch,
    ReviewerObjection,
    RevisionRecord,
)

AXES = ["task", "mechanism", "supervision-data", "assumption", "evaluation", "application"]


def objection(severity: str = "medium", status: str = "mitigated") -> ReviewerObjection:
    return ReviewerObjection(
        category="novelty",
        severity=severity,
        objection="The novelty boundary may be too narrow.",
        evidence_claim_ids=["C-001"],
        response="The axis-level comparison makes the boundary explicit.",
        status=status,
    )


def collision() -> CollisionAudit:
    comparisons = []
    for index in range(3):
        comparisons.append(
            PriorComparison(
                paper_id=f"P-{index}",
                axes=[
                    AxisOverlap(
                        axis=axis,
                        overlap="partial" if axis == "task" else "none",
                        rationale="bounded overlap",
                        evidence_claim_ids=["C-001"],
                    )
                    for axis in AXES
                ],
                collision_risk="medium",
            )
        )
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
        comparisons=comparisons,
        decision="revise",
        rationale="A structural revision can isolate the contribution.",
    )


def reviewer_audit(**updates) -> ReviewerAudit:
    data = {
        "review_id": "R-001",
        "idea_id": "I-001",
        "collision_audit_id": "A-001",
        "reviewer_context_hash": "c" * 64,
        "strongest_reason_for": "The mechanism tests a falsifiable boundary.",
        "strongest_reason_against": "The closest prior remains competitive.",
        "supporting_claim_ids": ["C-001"],
        "objections": [objection(), objection(), objection()],
        "kill_triggers": ["No improvement over the closest prior."],
        "initial_decision": "revise",
        "revision": RevisionRecord(
            before_hash="d" * 64,
            after_hash="e" * 64,
            structural_change="Replace application transfer with an assumption-level intervention.",
            rationale="This changes the novelty-bearing mechanism.",
        ),
        "final_decision": "pass",
        "rationale": "The single structural revision resolves the blocking objection.",
    }
    data.update(updates)
    return ReviewerAudit.model_validate(data)


def test_revise_decision_requires_exactly_one_structural_revision():
    with pytest.raises(ValidationError, match="exactly one structural revision"):
        reviewer_audit(revision=None)


def test_fatal_objection_forces_abandonment():
    with pytest.raises(ValidationError, match="fatal reviewer objections"):
        reviewer_audit(objections=[objection("fatal", "mitigated"), objection(), objection()])


def test_review_context_and_claims_are_cross_validated():
    idea = IdeaCandidate(
        idea_id="I-001",
        title="Candidate",
        novelty_level="strong",
        task="task",
        mechanism="mechanism",
        supervision_or_data="data",
        assumption="assumption",
        evaluation="evaluation",
        application="application",
        gap_ids=["G-001"],
        closest_prior_work=["P-0"],
        kill_criteria=["no gain"],
    )
    claim = ClaimEvidence(
        claim_id="C-001",
        claim="The closest prior uses a different assumption.",
        origin="cross-paper-synthesis",
        strength="moderate",
        evidence=[
            EvidenceRef(
                paper_id="P-0",
                role="support",
                verification="abstract",
                confidence=0.7,
            )
        ],
    )
    batch = ReviewerBatch(audits=[reviewer_audit(reviewer_context_hash="a" * 64)])

    result = validate_reviewer_batch(batch, [idea], CollisionBatch(audits=[collision()]), [claim])

    assert not result.ok
    assert any("context isolated" in error for error in result.errors)


def test_valid_review_passes_cross_artifact_gate():
    idea = IdeaCandidate(
        idea_id="I-001",
        title="Candidate",
        novelty_level="strong",
        task="task",
        mechanism="mechanism",
        supervision_or_data="data",
        assumption="assumption",
        evaluation="evaluation",
        application="application",
        gap_ids=["G-001"],
        closest_prior_work=["P-0"],
        kill_criteria=["no gain"],
    )
    claim = ClaimEvidence(
        claim_id="C-001",
        claim="The closest prior uses a different assumption.",
        origin="cross-paper-synthesis",
        strength="moderate",
        evidence=[
            EvidenceRef(
                paper_id="P-0",
                role="support",
                verification="abstract",
                confidence=0.7,
            )
        ],
    )

    result = validate_reviewer_batch(
        ReviewerBatch(audits=[reviewer_audit()]),
        [idea],
        CollisionBatch(audits=[collision()]),
        [claim],
    )

    assert result.ok


def test_every_idea_requires_exactly_one_reviewer_audit():
    first_idea = IdeaCandidate(
        idea_id="I-001",
        title="Candidate",
        novelty_level="strong",
        task="task",
        mechanism="mechanism",
        supervision_or_data="data",
        assumption="assumption",
        evaluation="evaluation",
        application="application",
        gap_ids=["G-001"],
        closest_prior_work=["P-0"],
        kill_criteria=["no gain"],
    )
    second_idea = first_idea.model_copy(
        update={"idea_id": "I-002", "title": "Unreviewed candidate"}
    )
    claim = ClaimEvidence(
        claim_id="C-001",
        claim="The closest prior uses a different assumption.",
        origin="cross-paper-synthesis",
        strength="moderate",
        evidence=[
            EvidenceRef(
                paper_id="P-0",
                role="support",
                verification="abstract",
                confidence=0.7,
            )
        ],
    )

    result = validate_reviewer_batch(
        ReviewerBatch(audits=[reviewer_audit()]),
        [first_idea, second_idea],
        CollisionBatch(audits=[collision()]),
        [claim],
    )

    assert not result.ok
    assert any("I-002" in error and "missing reviewer" in error for error in result.errors)
