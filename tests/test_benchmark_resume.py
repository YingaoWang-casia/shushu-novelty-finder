import hashlib
import json

from shushu_novelty.evaluation.benchmark import (
    merge_run_manifests,
    validate_benchmark_execution_manifest,
    validate_executed_run_manifest,
    validate_resume_matrix,
)
from shushu_novelty.schemas import BenchmarkRun


def run(run_id="B-001-bare", output_path="evals/results/bare/B-001.md"):
    return BenchmarkRun(
        run_id=run_id,
        seed_id="B-001",
        system="bare",
        output_path=output_path,
        prompt_hash="a" * 64,
    )


def test_matching_checkpoint_can_resume():
    assert validate_resume_matrix([run()], [run()]) == []


def test_checkpoint_cannot_redirect_an_output_path():
    errors = validate_resume_matrix([run()], [run(output_path="elsewhere.md")])

    assert any("output_path" in error for error in errors)


def test_pending_plan_is_not_an_executed_run_manifest(tmp_path):
    candidate = run()
    output = tmp_path / candidate.output_path
    output.parent.mkdir(parents=True)
    output.write_text("answer\n", encoding="utf-8")

    errors = validate_executed_run_manifest([candidate], tmp_path)

    assert any("240 runs" in error for error in errors)
    assert any("not complete" in error for error in errors)
    assert any("no adapter fingerprint" in error for error in errors)


def test_merge_prefers_complete_checkpoint_over_matching_pending_plan():
    pending = run()
    complete = run()
    complete.status = "complete"
    complete.model = "fixture"
    complete.adapter_sha256 = "b" * 64
    complete.output_sha256 = "c" * 64

    merged = merge_run_manifests([[pending], [complete]])

    assert merged.runs[0].status == "complete"
    assert merged.runs[0].output_sha256 == "c" * 64
    assert any("240 unique" in error for error in merged.errors)


def test_merge_rejects_conflicting_complete_results():
    first = run()
    second = run()
    for candidate in (first, second):
        candidate.status = "complete"
        candidate.model = "fixture"
        candidate.adapter_sha256 = "b" * 64
        candidate.output_sha256 = "c" * 64
    second.output_sha256 = "d" * 64

    merged = merge_run_manifests([[first], [second]])

    assert any("conflicting complete" in error for error in merged.errors)


def test_executed_manifest_rejects_changed_output_hash(tmp_path):
    candidate = run()
    candidate.status = "complete"
    candidate.model = "fixture"
    candidate.adapter_sha256 = "b" * 64
    candidate.output_sha256 = "c" * 64
    output = tmp_path / candidate.output_path
    output.parent.mkdir(parents=True)
    output.write_text("actual output\n", encoding="utf-8")

    errors = validate_executed_run_manifest([candidate], tmp_path)

    assert any("output hash does not match file" in error for error in errors)


def test_execution_manifest_rejects_changed_run_matrix(tmp_path):
    benchmark = tmp_path / "benchmark.jsonl"
    matrix = tmp_path / "matrix.jsonl"
    manifest = tmp_path / "execution.json"
    adapter = tmp_path / "adapters.json"
    benchmark.write_text("benchmark\n", encoding="utf-8")
    matrix.write_text("matrix\n", encoding="utf-8")
    adapter.write_text("adapter\n", encoding="utf-8")
    candidate = run()
    candidate.model = "fixture"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "status": "complete",
                "completed_at": "2026-01-01T00:00:00Z",
                "model": "fixture",
                "codex_cli_version": "fixture-runtime",
                "adapter_path": str(adapter),
                "adapter_sha256": hashlib.sha256(adapter.read_bytes()).hexdigest(),
                "benchmark_sha256": hashlib.sha256(benchmark.read_bytes()).hexdigest(),
                "completed_run_matrix_sha256": "b" * 64,
                "completed_run_matrix_path": str(matrix),
                "systems": ["bare", "self-reflection", "shushu-v0.1", "shushu-v0.2"],
                "expected_runs": 240,
            }
        ),
        encoding="utf-8",
    )

    errors = validate_benchmark_execution_manifest(
        manifest, [candidate], benchmark, matrix
    )

    assert any("run-matrix hash does not match" in error for error in errors)


def test_execution_manifest_rejects_changed_adapter_and_matrix_path(tmp_path):
    benchmark = tmp_path / "benchmark.jsonl"
    matrix = tmp_path / "matrix.jsonl"
    other_matrix = tmp_path / "other-matrix.jsonl"
    adapter = tmp_path / "adapters.json"
    manifest = tmp_path / "execution.json"
    benchmark.write_text("benchmark\n", encoding="utf-8")
    matrix.write_text("matrix\n", encoding="utf-8")
    other_matrix.write_text("matrix\n", encoding="utf-8")
    adapter.write_text("adapter\n", encoding="utf-8")
    candidate = run()
    candidate.model = "fixture"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "status": "complete",
                "completed_at": "2026-01-01T00:00:00Z",
                "model": "fixture",
                "codex_cli_version": "fixture-runtime",
                "adapter_path": str(adapter),
                "adapter_sha256": "a" * 64,
                "benchmark_sha256": hashlib.sha256(benchmark.read_bytes()).hexdigest(),
                "completed_run_matrix_path": str(other_matrix),
                "completed_run_matrix_sha256": hashlib.sha256(matrix.read_bytes()).hexdigest(),
                "systems": ["bare", "self-reflection", "shushu-v0.1", "shushu-v0.2"],
                "expected_runs": 240,
            }
        ),
        encoding="utf-8",
    )

    errors = validate_benchmark_execution_manifest(
        manifest, [candidate], benchmark, matrix
    )

    assert any("adapter hash does not match" in error for error in errors)
    assert any("run-matrix path does not match" in error for error in errors)
