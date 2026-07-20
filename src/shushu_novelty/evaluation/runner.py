"""Resumable, no-shell execution of external benchmark adapters."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from shushu_novelty.errors import InputError
from shushu_novelty.io import write_jsonl
from shushu_novelty.schemas import (
    BenchmarkAdapterSet,
    BenchmarkRun,
    BenchmarkSeed,
)

SYSTEMIC_ADAPTER_FAILURE_MARKERS = (
    "you've hit your usage limit",
    "you have hit your usage limit",
    "usage limit reached",
    "not logged in",
    "please run codex login",
    "401 unauthorized",
    "429 too many requests",
)


@dataclass(frozen=True)
class RunExecution:
    runs: list[BenchmarkRun]
    failures: list[dict[str, object]]

    @property
    def ok(self) -> bool:
        return not self.failures


def _load_failure_history(path: Path) -> list[dict[str, object]]:
    if not path.is_file():
        return []
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InputError(
                f"invalid benchmark failure history at {path}:{line_number}: {exc}"
            ) from exc
        if not isinstance(value, dict):
            raise InputError(
                f"benchmark failure history must contain objects at {path}:{line_number}"
            )
        records.append(value)
    return records


def _write_failure_history(records: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _is_systemic_adapter_failure(detail: str) -> bool:
    normalized = detail.casefold()
    return any(marker in normalized for marker in SYSTEMIC_ADAPTER_FAILURE_MARKERS)


def adapter_fingerprint(adapter: object) -> str:
    payload = adapter.model_dump(mode="json")
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


def _adapter_provenance_error(adapter: object, root: Path) -> str | None:
    for relative, expected_hash in adapter.provenance_files.items():
        path = (root / relative).resolve()
        if root not in path.parents:
            return f"adapter provenance path escapes results root: {relative}"
        if not path.is_file():
            return f"adapter provenance file is missing: {relative}"
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            return f"adapter provenance hash changed: {relative}"
    return None


def execute_run_matrix(
    runs: list[BenchmarkRun],
    seeds: list[BenchmarkSeed],
    adapter_set: BenchmarkAdapterSet,
    results_root: Path,
    failure_log: Path,
    checkpoint_path: Path | None = None,
) -> RunExecution:
    seed_by_id = {item.seed_id: item for item in seeds}
    adapter_by_system = {item.system: item for item in adapter_set.adapters}
    root = results_root.resolve()
    adapter_errors = {
        system: _adapter_provenance_error(adapter, root)
        for system, adapter in adapter_by_system.items()
    }
    failures = []
    failure_history = _load_failure_history(failure_log)
    for run in runs:
        seed = seed_by_id.get(run.seed_id)
        adapter = adapter_by_system.get(run.system)
        output = (root / run.output_path).resolve()
        error = None
        halt_after_failure = False
        if root not in output.parents:
            error = "output path escapes results root"
        elif seed is None:
            error = f"unknown benchmark seed {run.seed_id}"
        elif adapter is None:
            error = f"no command adapter configured for {run.system}"
        elif adapter_errors[run.system]:
            error = adapter_errors[run.system]
        elif run.status == "complete" and output.is_file() and run.output_sha256:
            current_hash = hashlib.sha256(output.read_bytes()).hexdigest()
            if current_hash == run.output_sha256:
                fingerprint = adapter_fingerprint(adapter)
                if run.adapter_sha256 and run.adapter_sha256 != fingerprint:
                    error = "completed run adapter fingerprint changed"
                else:
                    run.adapter_sha256 = fingerprint
                    if checkpoint_path is not None:
                        write_jsonl(runs, checkpoint_path)
                    continue
            else:
                error = "completed output hash changed"
        elif output.exists():
            error = "pending output path already exists; refusing to overwrite"
        else:
            environment = {
                **os.environ,
                "SHUSHU_RUN_ID": run.run_id,
                "SHUSHU_SEED_ID": run.seed_id,
                "SHUSHU_SYSTEM": run.system,
            }
            try:
                completed = subprocess.run(
                    adapter.command,
                    input=seed.prompt,
                    text=True,
                    capture_output=True,
                    timeout=adapter.timeout_seconds,
                    check=False,
                    env=environment,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                error = str(exc)
            else:
                if completed.returncode != 0:
                    detail = completed.stderr.strip()
                    error = (
                        f"adapter exited {completed.returncode}: "
                        f"{detail[-4000:]}"
                    )
                    halt_after_failure = _is_systemic_adapter_failure(detail)
                elif not completed.stdout.strip():
                    error = "adapter returned empty stdout"
                else:
                    output.parent.mkdir(parents=True, exist_ok=True)
                    temporary = output.with_suffix(output.suffix + ".tmp")
                    temporary.write_text(completed.stdout, encoding="utf-8")
                    temporary.replace(output)
                    run.status = "complete"
                    run.model = adapter.model
                    run.adapter_sha256 = adapter_fingerprint(adapter)
                    run.output_sha256 = hashlib.sha256(output.read_bytes()).hexdigest()
        if error:
            run.status = "failed"
            failure = {
                "schema_version": "1.0",
                "run_id": run.run_id,
                "seed_id": run.seed_id,
                "system": run.system,
                "error": error,
                "occurred_at": datetime.now(timezone.utc).isoformat(),
            }
            failures.append(failure)
            failure_history.append(failure)
            _write_failure_history(failure_history, failure_log)
        if checkpoint_path is not None:
            write_jsonl(runs, checkpoint_path)
        if halt_after_failure:
            break
    if not failure_log.exists():
        _write_failure_history(failure_history, failure_log)
    return RunExecution(runs=runs, failures=failures)
