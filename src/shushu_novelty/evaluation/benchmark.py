"""Benchmark composition gates and deterministic run planning."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from shushu_novelty.schemas import BenchmarkRun, BenchmarkSeed

EXPECTED_CASE_COUNTS = {
    "broad-direction": 20,
    "seed-paper": 20,
    "known-scoop": 10,
    "mechanism-transfer": 10,
}
REQUIRED_DOMAINS = {
    "llm-rag",
    "cv-multimodal",
    "speech",
    "agents",
    "systems",
    "data-mining",
    "security",
    "scientific-ml",
}
DEFAULT_SYSTEMS = ["bare", "self-reflection", "shushu-v0.1", "shushu-v0.2"]


@dataclass(frozen=True)
class BenchmarkValidation:
    errors: list[str]
    counts: dict[str, int]
    domains: dict[str, int]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class RunCollection:
    runs: list[BenchmarkRun]
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class RunMerge:
    runs: list[BenchmarkRun]
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_resume_matrix(
    planned: list[BenchmarkRun], checkpointed: list[BenchmarkRun]
) -> list[str]:
    """Require a checkpoint to describe exactly the same immutable run plan."""
    errors = []
    if len(planned) != len(checkpointed):
        errors.append(
            "checkpoint run count differs from plan: "
            f"{len(checkpointed)} != {len(planned)}"
        )
        return errors
    checkpoint_by_id = {item.run_id: item for item in checkpointed}
    if len(checkpoint_by_id) != len(checkpointed):
        errors.append("checkpoint contains duplicate run IDs")
        return errors
    immutable_fields = ("seed_id", "system", "output_path", "prompt_hash")
    for expected in planned:
        actual = checkpoint_by_id.get(expected.run_id)
        if actual is None:
            errors.append(f"checkpoint is missing run {expected.run_id}")
            continue
        changed = [
            field
            for field in immutable_fields
            if getattr(expected, field) != getattr(actual, field)
        ]
        if changed:
            errors.append(
                f"checkpoint run {expected.run_id} changed immutable fields: "
                + ", ".join(changed)
            )
    return errors


def merge_run_manifests(manifests: list[list[BenchmarkRun]]) -> RunMerge:
    """Merge overlapping checkpoints without allowing identity or result conflicts."""
    errors = []
    merged: dict[str, BenchmarkRun] = {}
    immutable_fields = ("seed_id", "system", "output_path", "prompt_hash")
    for manifest in manifests:
        for candidate in manifest:
            existing = merged.get(candidate.run_id)
            if existing is None:
                merged[candidate.run_id] = candidate.model_copy(deep=True)
                continue
            changed = [
                field
                for field in immutable_fields
                if getattr(existing, field) != getattr(candidate, field)
            ]
            if changed:
                errors.append(
                    f"run {candidate.run_id} conflicts on immutable fields: "
                    + ", ".join(changed)
                )
                continue
            if existing.status == "complete" and candidate.status == "complete":
                result_fields = ("model", "adapter_sha256", "output_sha256")
                if any(
                    getattr(existing, field) != getattr(candidate, field)
                    for field in result_fields
                ):
                    errors.append(f"run {candidate.run_id} has conflicting complete results")
            elif candidate.status == "complete":
                merged[candidate.run_id] = candidate.model_copy(deep=True)
    system_order = {system: index for index, system in enumerate(DEFAULT_SYSTEMS)}
    runs = sorted(
        merged.values(), key=lambda item: (item.seed_id, system_order.get(item.system, 99))
    )
    if len(runs) != 240:
        errors.append(f"merged run manifest must contain 240 unique runs, found {len(runs)}")
    incomplete = [run.run_id for run in runs if run.status != "complete"]
    if incomplete:
        errors.append(f"merged run manifest contains {len(incomplete)} incomplete runs")
    return RunMerge(runs=runs, errors=errors)


def validate_suite(seeds: list[BenchmarkSeed]) -> BenchmarkValidation:
    errors = []
    counts = Counter(seed.case_type for seed in seeds)
    domains = Counter(seed.domain for seed in seeds)
    if len(seeds) != 60:
        errors.append(f"benchmark must contain exactly 60 seeds, found {len(seeds)}")
    for case_type, expected in EXPECTED_CASE_COUNTS.items():
        if counts[case_type] != expected:
            errors.append(f"{case_type} count must be {expected}, found {counts[case_type]}")
    missing_domains = REQUIRED_DOMAINS - domains.keys()
    if missing_domains:
        errors.append(f"benchmark is missing domains: {', '.join(sorted(missing_domains))}")
    seed_ids = [seed.seed_id for seed in seeds]
    if len(seed_ids) != len(set(seed_ids)):
        errors.append("benchmark seed IDs must be unique")
    prompts = [" ".join(seed.prompt.casefold().split()) for seed in seeds]
    if len(prompts) != len(set(prompts)):
        errors.append("benchmark prompts must be unique")
    return BenchmarkValidation(errors=errors, counts=dict(counts), domains=dict(domains))


def build_run_matrix(
    seeds: list[BenchmarkSeed], systems: list[str] | None = None
) -> list[BenchmarkRun]:
    selected = systems or DEFAULT_SYSTEMS
    runs = []
    for seed in seeds:
        prompt_hash = hashlib.sha256(seed.prompt.encode("utf-8")).hexdigest()
        for system in selected:
            run_id = f"{seed.seed_id}-{system}"
            runs.append(
                BenchmarkRun(
                    run_id=run_id,
                    seed_id=seed.seed_id,
                    system=system,
                    output_path=f"evals/results/{system}/{seed.seed_id}.md",
                    prompt_hash=prompt_hash,
                )
            )
    return runs


def collect_run_outputs(runs: list[BenchmarkRun], results_root: Path) -> RunCollection:
    errors = []
    root = results_root.resolve()
    run_ids = [run.run_id for run in runs]
    if len(run_ids) != len(set(run_ids)):
        errors.append("benchmark run IDs must be unique")
    paths = [run.output_path for run in runs]
    if len(paths) != len(set(paths)):
        errors.append("benchmark output paths must be unique")
    by_seed: dict[str, set[str]] = {}
    for run in runs:
        by_seed.setdefault(run.seed_id, set()).add(run.system)
    for seed_id, systems in sorted(by_seed.items()):
        missing = set(DEFAULT_SYSTEMS) - systems
        if missing:
            errors.append(
                f"seed {seed_id} is missing required systems: {', '.join(sorted(missing))}"
            )
    if len(by_seed) != 60:
        errors.append(f"run collection must cover 60 seeds, found {len(by_seed)}")
    if len(runs) != 240:
        errors.append(f"run collection must contain 240 runs, found {len(runs)}")

    for run in runs:
        output = (root / run.output_path).resolve()
        if root not in output.parents:
            errors.append(f"run {run.run_id} output path escapes results root")
            continue
        if not output.is_file():
            errors.append(f"run {run.run_id} output is missing: {run.output_path}")
            continue
        if output.stat().st_size == 0:
            errors.append(f"run {run.run_id} output is empty: {run.output_path}")
            continue
        run.status = "complete"
        run.output_sha256 = hashlib.sha256(output.read_bytes()).hexdigest()
    return RunCollection(runs=runs, errors=errors)


def validate_executed_run_manifest(
    runs: list[BenchmarkRun], results_root: Path
) -> list[str]:
    """Require the manifest itself to carry verified execution provenance."""
    original = {
        run.run_id: (run.status, run.model, run.adapter_sha256, run.output_sha256)
        for run in runs
    }
    collection = collect_run_outputs(
        [run.model_copy(deep=True) for run in runs], results_root
    )
    errors = list(collection.errors)
    collected_by_id = {run.run_id: run for run in collection.runs}
    for run in runs:
        status, model, adapter_sha256, output_sha256 = original[run.run_id]
        if status != "complete":
            errors.append(f"executed run manifest record is not complete: {run.run_id}")
        if not model:
            errors.append(f"executed run manifest record has no model: {run.run_id}")
        if not adapter_sha256:
            errors.append(
                f"executed run manifest record has no adapter fingerprint: {run.run_id}"
            )
        if not output_sha256:
            errors.append(f"executed run manifest record has no output hash: {run.run_id}")
        elif collected_by_id[run.run_id].output_sha256 != output_sha256:
            errors.append(
                f"executed run manifest output hash does not match file: {run.run_id}"
            )
    return errors


def validate_benchmark_execution_manifest(
    manifest_path: Path,
    runs: list[BenchmarkRun],
    benchmark_path: Path,
    run_matrix_path: Path,
) -> list[str]:
    """Bind public scores to the completed execution environment and matrix bytes."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read benchmark execution manifest: {exc}"]
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "1.0":
        return ["benchmark execution manifest must be a schema v1.0 object"]
    errors = []
    if manifest.get("status") != "complete":
        errors.append("benchmark execution manifest status must be complete")
    if not isinstance(manifest.get("completed_at"), str) or not manifest["completed_at"].strip():
        errors.append("benchmark execution manifest must record completed_at")
    if manifest.get("expected_runs") != 240 or len(runs) != 240:
        errors.append("benchmark execution manifest must bind exactly 240 runs")
    expected_systems = set(DEFAULT_SYSTEMS)
    manifest_systems = manifest.get("systems")
    if not isinstance(manifest_systems, list) or set(manifest_systems) != expected_systems:
        errors.append("benchmark execution manifest systems differ from the primary systems")
    models = {run.model for run in runs}
    if models != {manifest.get("model")}:
        errors.append("benchmark execution manifest model differs from completed runs")
    if not isinstance(manifest.get("codex_cli_version"), str) or not manifest[
        "codex_cli_version"
    ].strip():
        errors.append("benchmark execution manifest must record the CLI/runtime version")
    adapter_digest = manifest.get("adapter_sha256")
    if not isinstance(adapter_digest, str) or len(adapter_digest) != 64 or any(
        character not in "0123456789abcdef" for character in adapter_digest
    ):
        errors.append("benchmark execution manifest must record the adapter SHA-256")
    adapter_path_value = manifest.get("adapter_path")
    if not isinstance(adapter_path_value, str) or not adapter_path_value.strip():
        errors.append("benchmark execution manifest must record the adapter path")
    else:
        adapter_path = Path(adapter_path_value)
        if not adapter_path.is_absolute():
            adapter_path = Path.cwd() / adapter_path
        if not adapter_path.is_file():
            errors.append("benchmark execution manifest adapter file does not exist")
        elif isinstance(adapter_digest, str):
            actual_adapter_digest = hashlib.sha256(adapter_path.read_bytes()).hexdigest()
            if adapter_digest != actual_adapter_digest:
                errors.append("benchmark execution manifest adapter hash does not match")
    expected_benchmark_hash = hashlib.sha256(benchmark_path.read_bytes()).hexdigest()
    if manifest.get("benchmark_sha256") != expected_benchmark_hash:
        errors.append("benchmark execution manifest benchmark hash does not match")
    expected_matrix_hash = hashlib.sha256(run_matrix_path.read_bytes()).hexdigest()
    if manifest.get("completed_run_matrix_sha256") != expected_matrix_hash:
        errors.append("benchmark execution manifest run-matrix hash does not match")
    declared_matrix_value = manifest.get("completed_run_matrix_path")
    if not isinstance(declared_matrix_value, str) or not declared_matrix_value.strip():
        errors.append("benchmark execution manifest must record the completed run-matrix path")
    else:
        declared_matrix = Path(declared_matrix_value)
        if not declared_matrix.is_absolute():
            declared_matrix = Path.cwd() / declared_matrix
        if declared_matrix.resolve() != run_matrix_path.resolve():
            errors.append("benchmark execution manifest run-matrix path does not match")
    return errors
