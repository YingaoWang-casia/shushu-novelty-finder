import pytest
from pydantic import ValidationError

from shushu_novelty.schemas import (
    ClaimEvidence,
    EvidenceRef,
    IdeaCandidate,
    PaperRecord,
    Provenance,
)


def provenance() -> Provenance:
    return Provenance(
        source="arxiv",
        source_identifier="2401.00001",
        retrieved_at="2026-07-16T00:00:00+00:00",
        source_url="https://arxiv.org/abs/2401.00001",
    )


def test_full_text_paper_must_be_verified():
    with pytest.raises(ValidationError, match="full-text verification"):
        PaperRecord(
            paper_id="P-arxiv:2401.00001",
            title="Example",
            identifiers={"arxiv": "2401.00001"},
            provenance=[provenance()],
            verification_level="full-text",
            evidence_status="candidate",
        )


def test_strong_claim_requires_full_text_support():
    with pytest.raises(ValidationError, match="strong claims require"):
        ClaimEvidence(
            claim_id="C-001",
            claim="A strong claim",
            origin="cross-paper-synthesis",
            strength="strong",
            evidence=[
                EvidenceRef(
                    paper_id="P-arxiv:2401.00001",
                    role="support",
                    verification="abstract",
                    confidence=0.8,
                )
            ],
        )


def test_every_claim_requires_traceable_evidence():
    with pytest.raises(ValidationError, match="traceable evidence"):
        ClaimEvidence(
            claim_id="C-002",
            claim="An ungrounded claim",
            origin="model-inference",
            strength="weak",
            evidence=[],
        )


@pytest.mark.parametrize("novelty_level", ["weak", "medium", "strong"])
def test_every_idea_requires_prior_work(novelty_level):
    with pytest.raises(ValidationError, match="closest prior work"):
        IdeaCandidate(
            idea_id="I-001",
            title="Candidate",
            novelty_level=novelty_level,
            task="task",
            mechanism="mechanism",
            supervision_or_data="data",
            assumption="assumption",
            evaluation="evaluation",
            application="application",
            gap_ids=["G-001"],
            kill_criteria=["no gain over baseline"],
        )
