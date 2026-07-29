import sys

import pytest

from shushu_novelty.evaluation.runner import execute_run_matrix
from shushu_novelty.io import sha256_file
from shushu_novelty.schemas import (
    BenchmarkAdapter,
    BenchmarkAdapterSet,
    BenchmarkRun,
    BenchmarkSeed,
)


def seed() -> BenchmarkSeed:
    return BenchmarkSeed(
        seed_id="B-001",
        case_type="broad-direction",
        domain="llm-rag",
        prompt="Audit retrieval evidence for a concrete research direction.",
        expected_behavior=["trace evidence"],
        provenance="fixture",
    )


def run() -> BenchmarkRun:
    return BenchmarkRun(
        run_id="B-001-bare",
        seed_id="B-001",
        system="bare",
        output_path="evals/results/bare/B-001.md",
    )


def adapters() -> BenchmarkAdapterSet:
    return BenchmarkAdapterSet(
        adapters=[
            BenchmarkAdapter(
                system="bare",
                command=[
                    sys.executable,
                    "-c",
                    "import sys; print('OUTPUT:' + sys.stdin.read())",
                ],
                model="fixture-model",
                timeout_seconds=10,
            )
        ]
    )


def test_external_adapter_execution_is_hashed_and_resumable(tmp_path):
    matrix = [run()]
    failure_log = tmp_path / "failures.jsonl"

    first = execute_run_matrix(matrix, [seed()], adapters(), tmp_path, failure_log)
    second = execute_run_matrix(matrix, [seed()], adapters(), tmp_path, failure_log)

    assert first.ok
    assert second.ok
    assert matrix[0].status == "complete"
    assert matrix[0].model == "fixture-model"
    assert matrix[0].adapter_sha256
    assert matrix[0].output_sha256
    assert "OUTPUT:Audit retrieval evidence" in (
        tmp_path / matrix[0].output_path
    ).read_text(encoding="utf-8")


def test_pending_run_refuses_to_overwrite_existing_output(tmp_path):
    matrix = [run()]
    output = tmp_path / matrix[0].output_path
    output.parent.mkdir(parents=True)
    output.write_text("user-owned output", encoding="utf-8")

    result = execute_run_matrix(
        matrix, [seed()], adapters(), tmp_path, tmp_path / "failures.jsonl"
    )

    assert not result.ok
    assert "refusing to overwrite" in result.failures[0]["error"]
    assert output.read_text(encoding="utf-8") == "user-owned output"


def test_adapter_provenance_tampering_fails_before_execution(tmp_path):
    protocol = tmp_path / "protocol.md"
    protocol.write_text("original", encoding="utf-8")
    configured = adapters()
    configured.adapters[0].provenance_files = {"protocol.md": sha256_file(protocol)}
    protocol.write_text("changed", encoding="utf-8")

    result = execute_run_matrix(
        [run()], [seed()], configured, tmp_path, tmp_path / "failures.jsonl"
    )

    assert not result.ok
    assert "provenance hash changed" in result.failures[0]["error"]


def test_execution_checkpoints_before_a_later_interrupt(tmp_path, monkeypatch):
    second = BenchmarkRun(
        run_id="B-002-bare",
        seed_id="B-002",
        system="bare",
        output_path="evals/results/bare/B-002.md",
    )
    second_seed = BenchmarkSeed(
        seed_id="B-002",
        case_type="broad-direction",
        domain="llm-rag",
        prompt="Audit a second concrete research direction.",
        expected_behavior=["trace evidence"],
        provenance="fixture",
    )
    original_run = __import__("subprocess").run
    calls = 0

    def interrupt_second(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise KeyboardInterrupt
        return original_run(*args, **kwargs)

    monkeypatch.setattr("shushu_novelty.evaluation.runner.subprocess.run", interrupt_second)
    checkpoint = tmp_path / "checkpoint.jsonl"

    with pytest.raises(KeyboardInterrupt):
        execute_run_matrix(
            [run(), second],
            [seed(), second_seed],
            adapters(),
            tmp_path,
            tmp_path / "failures.jsonl",
            checkpoint_path=checkpoint,
        )

    lines = checkpoint.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert '"status":"complete"' in lines[0]
    assert '"status":"pending"' in lines[1]


def test_failure_history_survives_a_successful_retry(tmp_path):
    broken = adapters()
    broken.adapters[0].command = [sys.executable, "-c", "raise SystemExit(7)"]
    failure_log = tmp_path / "failures.jsonl"
    matrix = [run()]

    first = execute_run_matrix(matrix, [seed()], broken, tmp_path, failure_log)
    second = execute_run_matrix(matrix, [seed()], adapters(), tmp_path, failure_log)

    assert not first.ok
    assert second.ok
    history = failure_log.read_text(encoding="utf-8").splitlines()
    assert len(history) == 1
    assert '"run_id": "B-001-bare"' in history[0]


def test_systemic_usage_failure_keeps_error_tail_and_stops_queue(tmp_path):
    second = BenchmarkRun(
        run_id="B-002-bare",
        seed_id="B-002",
        system="bare",
        output_path="evals/results/bare/B-002.md",
    )
    second_seed = BenchmarkSeed(
        seed_id="B-002",
        case_type="broad-direction",
        domain="llm-rag",
        prompt="Audit a second concrete research direction.",
        expected_behavior=["trace evidence"],
        provenance="fixture",
    )
    configured = adapters()
    configured.adapters[0].command = [
        sys.executable,
        "-c",
        "import sys; print('x' * 5000, file=sys.stderr); "
        "print(\"ERROR: You've hit your usage limit\", file=sys.stderr); raise SystemExit(2)",
    ]
    checkpoint = tmp_path / "checkpoint.jsonl"

    result = execute_run_matrix(
        [run(), second],
        [seed(), second_seed],
        configured,
        tmp_path,
        tmp_path / "failures.jsonl",
        checkpoint_path=checkpoint,
    )

    assert not result.ok
    assert len(result.failures) == 1
    assert "You've hit your usage limit" in result.failures[0]["error"]
    assert result.runs[0].status == "failed"
    assert result.runs[1].status == "pending"
    assert len((tmp_path / "failures.jsonl").read_text(encoding="utf-8").splitlines()) == 1


def test_ordinary_adapter_failure_does_not_stop_later_runs(tmp_path):
    second = BenchmarkRun(
        run_id="B-002-bare",
        seed_id="B-002",
        system="bare",
        output_path="evals/results/bare/B-002.md",
    )
    second_seed = BenchmarkSeed(
        seed_id="B-002",
        case_type="broad-direction",
        domain="llm-rag",
        prompt="Audit a second concrete research direction.",
        expected_behavior=["trace evidence"],
        provenance="fixture",
    )
    configured = adapters()
    configured.adapters[0].command = [
        sys.executable,
        "-c",
        "import os, sys; seed = os.environ['SHUSHU_SEED_ID']; "
        "print('ordinary failure', file=sys.stderr) if seed == 'B-001' else print('ok'); "
        "raise SystemExit(7 if seed == 'B-001' else 0)",
    ]

    result = execute_run_matrix(
        [run(), second],
        [seed(), second_seed],
        configured,
        tmp_path,
        tmp_path / "failures.jsonl",
    )

    assert not result.ok
    assert len(result.failures) == 1
    assert result.runs[0].status == "failed"
    assert result.runs[1].status == "complete"
