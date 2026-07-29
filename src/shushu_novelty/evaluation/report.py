"""Deterministic final-report gates."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from shushu_novelty.evaluation.release import (
    validate_public_evaluation,
    validate_public_evaluation_artifacts,
)
from shushu_novelty.evaluation.structural import validate_report
from shushu_novelty.io import load_json, sha256_file, validate_jsonl
from shushu_novelty.schemas import ClaimEvidence, ReportManifest, RunState


@dataclass(frozen=True)
class FinalReportResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _resolve_inside(run_dir: Path, relative: str) -> Path | None:
    root = run_dir.resolve()
    candidate = (root / relative).resolve()
    return candidate if candidate == root or root in candidate.parents else None


def validate_final_report(manifest: ReportManifest, run_dir: Path) -> FinalReportResult:
    errors = []
    warnings = []
    try:
        state = RunState.model_validate(load_json(run_dir / "run.json"))
    except Exception as exc:
        errors.append(f"cannot validate final report against run state: {exc}")
    else:
        if manifest.run_id != state.run_id:
            errors.append("report manifest run_id does not match run state")
        if manifest.mode != state.mode:
            errors.append("report manifest mode does not match run state")
    report_path = _resolve_inside(run_dir, manifest.report_path)
    text = ""
    if report_path is None:
        errors.append("report path escapes the run directory")
    elif not report_path.is_file():
        errors.append(f"report file does not exist: {manifest.report_path}")
    else:
        if sha256_file(report_path) != manifest.report_sha256:
            errors.append("report file hash does not match manifest")
        text = report_path.read_text(encoding="utf-8")
        structural = validate_report(
            text,
            paper_mode=manifest.mode in {"idea", "full"},
            workflow_mode=manifest.mode,
        )
        errors.extend(
            f"report is missing structural section: {item}" for item in structural.missing
        )
        warnings.extend(f"report language warning: {item}" for item in structural.warnings)
        folded = text.casefold()
        if "failure" not in folded and "失败" not in text:
            errors.append("report must explicitly disclose failures, including an explicit none")
        if "uncertainty" not in folded and "不确定" not in text:
            errors.append("report must explicitly disclose uncertainty")
        for section in manifest.uncertainty_sections:
            if section.casefold() not in folded:
                errors.append(f"uncertainty section is absent from report: {section}")
        for limitation in manifest.known_limitations:
            if limitation.casefold() not in folded:
                errors.append(f"known limitation is absent from report: {limitation}")
        for claim in manifest.effectiveness_claims:
            if claim.casefold() not in folded:
                errors.append(f"effectiveness claim is absent from report: {claim}")

    claims_path = run_dir / "papers" / "claims.jsonl"
    try:
        claims = validate_jsonl(claims_path, ClaimEvidence)
    except Exception as exc:
        errors.append(f"cannot validate report claims from {claims_path}: {exc}")
    else:
        known_claim_ids = {item.claim_id for item in claims}
        unknown = set(manifest.claim_ids) - known_claim_ids
        if unknown:
            errors.append("report references unknown claims: " + ", ".join(sorted(unknown)))
        strong_ids = {item.claim_id for item in claims if item.strength == "strong"}
        omitted_strong = strong_ids - set(manifest.claim_ids)
        if omitted_strong:
            errors.append(
                "report manifest omits strong claims: " + ", ".join(sorted(omitted_strong))
            )

    for relative, expected_hash in manifest.input_artifact_hashes.items():
        input_path = _resolve_inside(run_dir, relative)
        if input_path is None:
            errors.append(f"input artifact escapes the run directory: {relative}")
        elif not input_path.is_file():
            errors.append(f"input artifact does not exist: {relative}")
        elif sha256_file(input_path) != expected_hash:
            errors.append(f"input artifact hash does not match manifest: {relative}")

    for relative in manifest.failure_logs:
        failure_path = _resolve_inside(run_dir, relative)
        if failure_path is None:
            errors.append(f"failure log escapes the run directory: {relative}")
        elif not failure_path.is_file():
            errors.append(f"declared failure log does not exist: {relative}")
        elif sha256_file(failure_path) != manifest.failure_log_hashes[relative]:
            errors.append(f"failure log hash does not match manifest: {relative}")

    if manifest.public_evaluation_path:
        evaluation_path = _resolve_inside(run_dir, manifest.public_evaluation_path)
        if evaluation_path is None:
            errors.append("public evaluation path escapes the run directory")
        elif not evaluation_path.is_file():
            errors.append(
                f"public evaluation report does not exist: {manifest.public_evaluation_path}"
            )
        elif sha256_file(evaluation_path) != manifest.public_evaluation_sha256:
            errors.append("public evaluation report hash does not match manifest")
        else:
            try:
                evaluation = json.loads(evaluation_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"invalid public evaluation report: {exc}")
            else:
                errors.extend(validate_public_evaluation(evaluation))
                errors.extend(
                    validate_public_evaluation_artifacts(evaluation, evaluation_path)
                )
    return FinalReportResult(errors=errors, warnings=warnings)
