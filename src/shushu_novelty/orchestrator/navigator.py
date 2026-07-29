"""Inspect artifacts and return exactly one deterministic next action."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from shushu_novelty.errors import GateError, InputError
from shushu_novelty.evaluation.citation import validate_ledger
from shushu_novelty.evaluation.collision import validate_collision_batch
from shushu_novelty.evaluation.gap import validate_gaps
from shushu_novelty.evaluation.idea import validate_ideas
from shushu_novelty.evaluation.lineage import validate_lineage
from shushu_novelty.evaluation.report import validate_final_report
from shushu_novelty.evaluation.reviewer import validate_reviewer_batch
from shushu_novelty.io import load_json, sha256_file, validate_jsonl
from shushu_novelty.orchestrator.phases import PhaseSpec, phases_for_mode
from shushu_novelty.orchestrator.state import load_state, save_state
from shushu_novelty.retrieval.replay import replay_search
from shushu_novelty.schemas import (
    ClaimEvidence,
    CollisionBatch,
    FullTextDocument,
    GapRecord,
    IdeaCandidate,
    LineageGraph,
    PaperRecord,
    ReportManifest,
    ReviewerBatch,
)
from shushu_novelty.schemas.run_state import utc_now


def _require_keys(value: dict[str, Any], path: Path, keys: set[str]) -> None:
    missing = sorted(keys - value.keys())
    if missing:
        raise GateError(f"{path} is missing required keys: {', '.join(missing)}")


def _auxiliary_hashes(run_dir: Path, phase: PhaseSpec) -> dict[str, str]:
    hashes = {}
    for relative in phase.auxiliary_artifacts:
        path = run_dir / relative
        if not path.is_file():
            raise GateError(f"{phase.code} is missing required auxiliary artifact: {path}")
        hashes[relative] = sha256_file(path)
    return hashes


def _bundle_hash(primary_hash: str, auxiliary_hashes: dict[str, str]) -> str:
    if not auxiliary_hashes:
        return primary_hash
    digest = hashlib.sha256()
    digest.update(primary_hash.encode())
    for path, value in sorted(auxiliary_hashes.items()):
        digest.update(b"\0")
        digest.update(path.encode())
        digest.update(b"\0")
        digest.update(value.encode())
    return digest.hexdigest()


def validate_artifact(path: Path, phase: PhaseSpec) -> None:
    kind = phase.artifact_kind
    try:
        if kind == "intake":
            _require_keys(load_json(path), path, {"topic", "mode", "created_at"})
        elif kind == "scope":
            _require_keys(
                load_json(path),
                path,
                {"core_task", "inclusion_criteria", "exclusion_criteria", "time_window"},
            )
        elif kind == "paper-jsonl":
            records = validate_jsonl(path, PaperRecord)
            manifest_path = path.with_suffix(path.suffix + ".manifest.json")
            manifest, replayed, _ = replay_search(manifest_path)
            manifest_records_path = (manifest_path.parent / manifest.records_path).resolve()
            if manifest_records_path != path.resolve():
                raise GateError("retrieval replay manifest does not bind the phase paper artifact")
            if [item.paper_id for item in records] != [item.paper_id for item in replayed]:
                raise GateError("retrieval replay order differs from the phase paper artifact")
        elif kind == "fulltext-jsonl":
            documents = validate_jsonl(path, FullTextDocument)
            run_dir = path.parent.parent
            papers = validate_jsonl(run_dir / "retrieval" / "papers.jsonl", PaperRecord)
            claims = validate_jsonl(run_dir / "papers" / "claims.jsonl", ClaimEvidence)
            result = validate_ledger(papers, documents, claims)
            if result.errors:
                raise GateError("; ".join(result.errors))
        elif kind == "lineage":
            try:
                graph = LineageGraph.model_validate(load_json(path))
                run_dir = path.parent.parent
                papers = validate_jsonl(run_dir / "retrieval" / "papers.jsonl", PaperRecord)
                claims = validate_jsonl(run_dir / "papers" / "claims.jsonl", ClaimEvidence)
                result = validate_lineage(graph, papers, claims)
                if result.errors:
                    raise GateError("; ".join(result.errors))
            except GateError:
                raise
            except Exception as exc:
                raise GateError(f"invalid lineage graph in {path}: {exc}") from exc
        elif kind == "gap-jsonl":
            gaps = validate_jsonl(path, GapRecord)
            run_dir = path.parent.parent
            papers = validate_jsonl(run_dir / "retrieval" / "papers.jsonl", PaperRecord)
            claims = validate_jsonl(run_dir / "papers" / "claims.jsonl", ClaimEvidence)
            result = validate_gaps(gaps, papers, claims)
            if result.errors:
                raise GateError("; ".join(result.errors))
        elif kind == "idea-jsonl":
            ideas = validate_jsonl(path, IdeaCandidate)
            run_dir = path.parent.parent
            gaps = validate_jsonl(run_dir / "gaps" / "gaps.jsonl", GapRecord)
            papers = validate_jsonl(run_dir / "retrieval" / "papers.jsonl", PaperRecord)
            result = validate_ideas(ideas, gaps, papers)
            if result.errors:
                raise GateError("; ".join(result.errors))
        elif kind == "collision":
            try:
                batch = CollisionBatch.model_validate(load_json(path))
                run_dir = path.parent.parent
                ideas = validate_jsonl(run_dir / "ideas" / "ideas.jsonl", IdeaCandidate)
                papers = validate_jsonl(run_dir / "retrieval" / "papers.jsonl", PaperRecord)
                claims = validate_jsonl(run_dir / "papers" / "claims.jsonl", ClaimEvidence)
                result = validate_collision_batch(batch, ideas, papers, claims)
                if result.errors:
                    raise GateError("; ".join(result.errors))
            except GateError:
                raise
            except Exception as exc:
                raise GateError(f"invalid collision batch in {path}: {exc}") from exc
        elif kind == "reviewer":
            try:
                batch = ReviewerBatch.model_validate(load_json(path))
                run_dir = path.parent.parent
                ideas = validate_jsonl(run_dir / "ideas" / "ideas.jsonl", IdeaCandidate)
                collisions = CollisionBatch.model_validate(
                    load_json(run_dir / "collision" / "collisions.json")
                )
                claims = validate_jsonl(run_dir / "papers" / "claims.jsonl", ClaimEvidence)
                result = validate_reviewer_batch(batch, ideas, collisions, claims)
                if result.errors:
                    raise GateError("; ".join(result.errors))
            except GateError:
                raise
            except Exception as exc:
                raise GateError(f"invalid reviewer audit in {path}: {exc}") from exc
        elif kind == "report":
            try:
                manifest = ReportManifest.model_validate(load_json(path))
                result = validate_final_report(manifest, path.parent.parent)
                if result.errors:
                    raise GateError("; ".join(result.errors))
            except GateError:
                raise
            except Exception as exc:
                raise GateError(f"invalid final-report manifest in {path}: {exc}") from exc
        else:
            raise GateError(f"unknown artifact kind for {phase.code}: {kind}")
    except InputError as exc:
        raise GateError(str(exc)) from exc


def next_action(run_dir: Path) -> dict[str, Any]:
    state = load_state(run_dir)
    original_state = state.model_dump(mode="json")

    def save_if_changed() -> None:
        if state.model_dump(mode="json") != original_state:
            save_state(run_dir, state)

    previous_hash = hashlib.sha256(
        f"{state.topic}\0{state.mode}\0{state.model or ''}\0{state.prompt_version or ''}".encode()
    ).hexdigest()
    upstream_bundle_migrated = False
    for phase in phases_for_mode(state.mode):
        phase_state = state.phases[phase.code]
        artifact = run_dir / phase.artifact
        if not artifact.exists():
            phase_state.input_hash = previous_hash
            phase_state.status = "ready"
            phase_state.error = None
            save_if_changed()
            return {
                "status": "ready",
                "phase": phase.code,
                "name": phase.name,
                "artifact": str(artifact),
            }
        current_hash = sha256_file(artifact)
        try:
            current_auxiliary = _auxiliary_hashes(run_dir, phase)
        except GateError as exc:
            phase_state.status = "failed"
            phase_state.error = str(exc)
            save_if_changed()
            return {
                "status": "failed",
                "phase": phase.code,
                "name": phase.name,
                "artifact": str(artifact),
                "error": str(exc),
            }
        phase_bundle_migrated = False
        if phase_state.output_hash is not None:
            if phase_state.input_hash is None:
                if phase_state.output_hash != current_hash:
                    phase_state.status = "failed"
                    phase_state.error = (
                        f"{phase.code} legacy artifact changed before input-hash migration: "
                        f"{artifact}"
                    )
                    save_if_changed()
                    return {
                        "status": "failed",
                        "phase": phase.code,
                        "name": phase.name,
                        "artifact": str(artifact),
                        "error": phase_state.error,
                    }
                phase_state.input_hash = previous_hash
            elif phase_state.input_hash != previous_hash and upstream_bundle_migrated:
                phase_state.input_hash = previous_hash
            elif phase_state.input_hash != previous_hash:
                phase_state.status = "failed"
                phase_state.error = (
                    f"{phase.code} input hash no longer matches its validated upstream artifact"
                )
                save_if_changed()
                return {
                    "status": "failed",
                    "phase": phase.code,
                    "name": phase.name,
                    "artifact": str(artifact),
                    "error": phase_state.error,
                }
            if phase_state.output_hash != current_hash:
                phase_state.status = "failed"
                phase_state.error = f"{phase.code} artifact changed after validation: {artifact}"
                save_if_changed()
                return {
                    "status": "failed",
                    "phase": phase.code,
                    "name": phase.name,
                    "artifact": str(artifact),
                    "error": phase_state.error,
                }
            if not phase_state.auxiliary_hashes and current_auxiliary:
                phase_state.auxiliary_hashes = current_auxiliary
                phase_bundle_migrated = True
            elif phase_state.auxiliary_hashes != current_auxiliary:
                phase_state.status = "failed"
                phase_state.error = f"{phase.code} auxiliary artifact changed after validation"
                save_if_changed()
                return {
                    "status": "failed",
                    "phase": phase.code,
                    "name": phase.name,
                    "artifact": str(artifact),
                    "error": phase_state.error,
                }
        else:
            phase_state.input_hash = previous_hash
        try:
            validate_artifact(artifact, phase)
        except GateError as exc:
            phase_state.status = "failed"
            phase_state.error = str(exc)
            save_if_changed()
            return {
                "status": "failed",
                "phase": phase.code,
                "name": phase.name,
                "artifact": str(artifact),
                "error": str(exc),
            }
        phase_state.status = "complete"
        phase_state.output_hash = current_hash
        phase_state.auxiliary_hashes = current_auxiliary
        previous_hash = _bundle_hash(current_hash, current_auxiliary)
        upstream_bundle_migrated = phase_bundle_migrated
        phase_state.completed_at = phase_state.completed_at or utc_now()
        phase_state.error = None

    save_if_changed()
    return {"status": "complete", "run_id": state.run_id, "mode": state.mode}
