"""Phase definitions and mode routing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PhaseSpec:
    code: str
    name: str
    artifact: str
    artifact_kind: str
    auxiliary_artifacts: tuple[str, ...] = ()


ALL_PHASES = [
    PhaseSpec("P0", "Intake", "intake/intake.json", "intake"),
    PhaseSpec("P1", "Scope Narrowing", "intake/scope.json", "scope"),
    PhaseSpec(
        "P2",
        "Literature Retrieval",
        "retrieval/papers.jsonl",
        "paper-jsonl",
        ("retrieval/papers.jsonl.manifest.json", "retrieval/failures.jsonl"),
    ),
    PhaseSpec(
        "P3",
        "Paper Verification",
        "papers/fulltext.jsonl",
        "fulltext-jsonl",
        ("papers/claims.jsonl", "papers/fulltext.failures.jsonl"),
    ),
    PhaseSpec("P4", "Lineage Construction", "lineage/graph.json", "lineage"),
    PhaseSpec("P5", "Gap Audit", "gaps/gaps.jsonl", "gap-jsonl"),
    PhaseSpec("P6", "Idea Portfolio Generation", "ideas/ideas.jsonl", "idea-jsonl"),
    PhaseSpec("P7", "Novelty Collision Check", "collision/collisions.json", "collision"),
    PhaseSpec("P8", "Reviewer Audit", "audit/reviewer.json", "reviewer"),
    PhaseSpec("P9", "Final Report", "report/manifest.json", "report"),
]

PHASE_BY_CODE = {phase.code: phase for phase in ALL_PHASES}

MODE_PHASES = {
    "lineage": ["P0", "P1", "P2", "P3", "P4", "P5", "P9"],
    "idea": ["P0", "P1", "P2", "P3", "P5", "P6", "P7", "P8", "P9"],
    "full": [phase.code for phase in ALL_PHASES],
}


def phases_for_mode(mode: str) -> list[PhaseSpec]:
    return [PHASE_BY_CODE[code] for code in MODE_PHASES[mode]]
