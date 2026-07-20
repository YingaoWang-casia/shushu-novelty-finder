import json

import pytest
from pydantic import ValidationError

from shushu_novelty.evaluation.report import validate_final_report
from shushu_novelty.io import sha256_file
from shushu_novelty.schemas import ReportManifest


def report_text() -> str:
    return """# Final report

Mode: full
## Research Scope Card
Scope is bounded.
## Representative Papers
Paper evidence is listed here.
## Trend Matrix
Trend is explicit.
## Gap Audit
Research gap is evidence-backed.
## Strong Idea Candidate
Strong novelty candidate.
## Risk and Failure Disclosure
No retrieval failures were observed in this fixture.
## Minimum Experiment and Baseline
An ablation is required.
## Paper Thesis
Core claim is bounded.
## Paper-readiness Verdict
Pilot-ready only.
## Uncertainty Budget
The mini fixture does not establish external validity.
## Known Limitations
No live connector evidence is included.
"""


def setup_run(tmp_path):
    for directory in [
        "report",
        "papers",
        "retrieval",
        "intake",
        "lineage",
        "gaps",
        "ideas",
        "collision",
        "audit",
    ]:
        (tmp_path / directory).mkdir()
    (tmp_path / "run.json").write_text(
        json.dumps(
            {
                "run_id": "fixture-run",
                "topic": "fixture",
                "topic_slug": "fixture",
                "mode": "full",
                "created_at": "now",
                "updated_at": "now",
                "phases": {},
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "report" / "report.md").write_text(report_text(), encoding="utf-8")
    claim = {
        "claim_id": "C-001",
        "claim": "The fixture is deliberately bounded.",
        "origin": "model-inference",
        "strength": "moderate",
        "evidence": [
            {
                "paper_id": "P-fixture:1",
                "role": "background",
                "verification": "metadata",
                "confidence": 0.5,
            }
        ],
    }
    (tmp_path / "papers" / "claims.jsonl").write_text(
        json.dumps(claim) + "\n", encoding="utf-8"
    )
    (tmp_path / "retrieval" / "failures.jsonl").write_text("", encoding="utf-8")
    for relative in [
        "intake/scope.json",
        "retrieval/papers.jsonl",
        "papers/fulltext.jsonl",
        "lineage/graph.json",
        "gaps/gaps.jsonl",
        "ideas/ideas.jsonl",
        "collision/collisions.json",
        "audit/reviewer.json",
    ]:
        (tmp_path / relative).write_text(f"fixture: {relative}\n", encoding="utf-8")


def manifest(tmp_path=None, **updates) -> ReportManifest:
    input_paths = [
        "intake/scope.json",
        "retrieval/papers.jsonl",
        "papers/fulltext.jsonl",
        "papers/claims.jsonl",
        "lineage/graph.json",
        "gaps/gaps.jsonl",
        "ideas/ideas.jsonl",
        "collision/collisions.json",
        "audit/reviewer.json",
    ]
    data = {
        "run_id": "fixture-run",
        "mode": "full",
        "report_path": "report/report.md",
        "report_sha256": (
            sha256_file(tmp_path / "report/report.md") if tmp_path else "a" * 64
        ),
        "input_artifact_hashes": {
            path: sha256_file(tmp_path / path) if tmp_path else "a" * 64
            for path in input_paths
        },
        "claim_ids": ["C-001"],
        "failure_logs": ["retrieval/failures.jsonl"],
        "failure_log_hashes": {
            "retrieval/failures.jsonl": (
                sha256_file(tmp_path / "retrieval/failures.jsonl")
                if tmp_path
                else "a" * 64
            )
        },
        "uncertainty_sections": ["Uncertainty Budget"],
        "known_limitations": ["No live connector evidence is included."],
    }
    data.update(updates)
    return ReportManifest.model_validate(data)


def test_final_report_discloses_failures_and_uncertainty(tmp_path):
    setup_run(tmp_path)

    result = validate_final_report(manifest(tmp_path), tmp_path)

    assert result.ok


def test_effectiveness_claim_requires_hashed_public_evaluation():
    with pytest.raises(ValidationError, match="effectiveness claims require"):
        manifest(effectiveness_claims=["The system improves novelty precision."])


def test_non_publishable_evaluation_cannot_support_effectiveness(tmp_path):
    setup_run(tmp_path)
    evaluation = tmp_path / "report" / "evaluation.json"
    evaluation.write_text(
        json.dumps({"publishable": False, "primary_basis": "human"}), encoding="utf-8"
    )
    candidate = manifest(
        tmp_path,
        effectiveness_claims=["No live connector evidence is included."],
        public_evaluation_path="report/evaluation.json",
        public_evaluation_sha256=sha256_file(evaluation),
    )

    result = validate_final_report(candidate, tmp_path)

    assert not result.ok
    assert any("must be marked publishable" in error for error in result.errors)


def test_report_paths_cannot_escape_run_directory(tmp_path):
    setup_run(tmp_path)

    with pytest.raises(ValidationError, match="portable relative path"):
        manifest(tmp_path, report_path="../outside.md")


def test_report_manifest_rejects_changed_input_artifact(tmp_path):
    setup_run(tmp_path)
    candidate = manifest(tmp_path)
    (tmp_path / "intake" / "scope.json").write_text("changed\n", encoding="utf-8")

    result = validate_final_report(candidate, tmp_path)

    assert not result.ok
    assert any("input artifact hash does not match" in error for error in result.errors)


def test_report_manifest_rejects_changed_report(tmp_path):
    setup_run(tmp_path)
    candidate = manifest(tmp_path)
    (tmp_path / "report" / "report.md").write_text("changed\n", encoding="utf-8")

    result = validate_final_report(candidate, tmp_path)

    assert not result.ok
    assert "report file hash does not match manifest" in result.errors


def test_report_manifest_rejects_changed_failure_log(tmp_path):
    setup_run(tmp_path)
    candidate = manifest(tmp_path)
    (tmp_path / "retrieval" / "failures.jsonl").write_text(
        '{"error":"late mutation"}\n', encoding="utf-8"
    )

    result = validate_final_report(candidate, tmp_path)

    assert not result.ok
    assert any("failure log hash does not match" in error for error in result.errors)
