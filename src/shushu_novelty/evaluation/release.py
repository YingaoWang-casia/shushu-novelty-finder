"""Release gate for README effectiveness claims."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from shushu_novelty.evaluation.metrics import MIN_SHARED_SEEDS, REQUIRED_PRIMARY_SYSTEMS
from shushu_novelty.io import sha256_file

START = "<!-- EFFECTIVENESS_CLAIMS_START -->"
END = "<!-- EFFECTIVENESS_CLAIMS_END -->"
NO_CLAIM_MARKERS = {
    "当前没有公开的比较效果声明",
    "no public comparative effectiveness claims",
}
REQUIRED_METRIC_FAMILIES = {
    "retrieval": {
        "known_prior_recall_at_k",
        "duplicate_rate",
        "metadata_completeness",
        "accepted_preprint_accuracy",
    },
    "evidence": {
        "citation_existence_precision",
        "claim_entailment_accuracy",
        "unsupported_claim_rate",
        "full_text_verification_coverage",
    },
    "lineage": {
        "relation_classification_macro_f1",
        "relation_f1_by_type",
        "closest_prior_recall_at_5",
        "saturated_contribution_precision",
        "unsupported_lineage_edge_rate",
    },
    "idea": {
        "problem_significance",
        "novelty",
        "method_specificity",
        "feasibility",
        "falsifiability",
        "baseline_completeness",
        "reviewer_defensibility",
    },
    "calibration": {
        "strong_false_positive_rate",
        "scoop_detection_recall",
        "confidence_accuracy_correlation",
        "kill_decision_precision",
    },
}
REQUIRED_RELATION_TYPES = {
    "ancestor",
    "closest-prior",
    "sibling",
    "follow-up",
    "benchmark",
    "contrary-evidence",
    "mechanism-transfer",
}
REQUIRED_PUBLIC_ARTIFACTS = {
    "benchmark_seeds",
    "blind_key",
    "blind_manifest",
    "blind_pairwise_responses",
    "blind_scalar_responses",
    "execution_manifest",
    "run_matrix",
    "scalar_judgments",
    "pairwise_judgments",
}


@dataclass(frozen=True)
class ReleaseCheckResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _claim_section(readme_text: str) -> str | None:
    if readme_text.count(START) != 1 or readme_text.count(END) != 1:
        return None
    return readme_text.split(START, 1)[1].split(END, 1)[0].strip()


def validate_public_evaluation(evaluation: dict[str, object]) -> list[str]:
    errors = []
    if evaluation.get("publishable") is not True:
        errors.append("public evaluation must be marked publishable")
    if evaluation.get("primary_basis") != "human":
        errors.append("public evaluation must use human judgments as its primary basis")
    human_raters = evaluation.get("human_raters", [])
    if not isinstance(human_raters, list) or len(human_raters) < 2:
        errors.append("public evaluation must list at least two human raters")
    coverage = evaluation.get("coverage")
    overlap_coverage = isinstance(coverage, dict)
    expected_human_seed_ratings = None
    if overlap_coverage:
        if evaluation.get("rating_design") not in {"complete", "balanced-overlap"}:
            errors.append("public evaluation must declare a verified human rating design")
        if coverage.get("collective_seed_count") != 60:
            errors.append("public evaluation must collectively cover all 60 benchmark seeds")
        if not isinstance(coverage.get("shared_seed_count"), int) or coverage.get(
            "shared_seed_count", 0
        ) < MIN_SHARED_SEEDS:
            errors.append(
                "public evaluation must include at least "
                f"{MIN_SHARED_SEEDS} shared human-rated seeds"
            )
        minimum_raters = coverage.get("minimum_raters_per_seed")
        if not isinstance(minimum_raters, int) or minimum_raters < 1:
            errors.append("public evaluation must report per-seed human coverage")
        maximum_raters = coverage.get("maximum_raters_per_seed")
        if not isinstance(maximum_raters, int) or maximum_raters < 2:
            errors.append("public evaluation must include multiply rated shared seeds")
        shared_seed_ids = coverage.get("shared_seed_ids")
        if (
            not isinstance(shared_seed_ids, list)
            or len(shared_seed_ids) != coverage.get("shared_seed_count")
            or any(not isinstance(seed_id, str) for seed_id in shared_seed_ids)
            or len(set(shared_seed_ids)) != len(shared_seed_ids)
        ):
            errors.append("public evaluation shared seed IDs must match shared coverage")
        rater_seed_counts = coverage.get("rater_seed_counts")
        if (
            not isinstance(rater_seed_counts, dict)
            or len(rater_seed_counts) < 2
            or any(not isinstance(key, str) for key in rater_seed_counts)
            or any(
                not isinstance(value, int) or value < 1
                for value in rater_seed_counts.values()
            )
        ):
            errors.append("public evaluation must report valid per-rater seed counts")
        else:
            expected_human_seed_ratings = sum(rater_seed_counts.values())
    human_judgments = evaluation.get("human_judgments", 0)
    minimum_scalar = (60 + MIN_SHARED_SEEDS) * 4 if overlap_coverage else 480
    if not isinstance(human_judgments, int) or human_judgments < minimum_scalar:
        errors.append(
            f"public evaluation must include at least {minimum_scalar} scalar human judgments"
        )
    if (
        expected_human_seed_ratings is not None
        and human_judgments != expected_human_seed_ratings * 4
    ):
        errors.append("scalar human judgments do not match per-rater seed coverage")
    if evaluation.get("cohens_kappa") is None:
        errors.append("public evaluation must report scalar Cohen's kappa")
    pairwise = evaluation.get("pairwise", {})
    pairwise_count = pairwise.get("human_judgments", 0) if isinstance(pairwise, dict) else 0
    minimum_pairwise = (60 + MIN_SHARED_SEEDS) * 6 if overlap_coverage else 720
    if not isinstance(pairwise_count, int) or pairwise_count < minimum_pairwise:
        errors.append(
            f"public evaluation must include at least {minimum_pairwise} pairwise human judgments"
        )
    if (
        expected_human_seed_ratings is not None
        and pairwise_count != expected_human_seed_ratings * 6
    ):
        errors.append("pairwise human judgments do not match per-rater seed coverage")
    if not isinstance(pairwise, dict) or pairwise.get("cohens_kappa") is None:
        errors.append("public evaluation must report pairwise Cohen's kappa")
    if evaluation.get("expected_seed_count") != 60:
        errors.append("public evaluation must verify all 60 benchmark seeds")
    if evaluation.get("completed_run_count") != 240:
        errors.append("public evaluation must bind all 240 completed system runs")
    artifacts = evaluation.get("artifacts", {})
    if not isinstance(artifacts, dict):
        artifacts = {}
    missing_artifacts = REQUIRED_PUBLIC_ARTIFACTS - set(artifacts)
    if missing_artifacts:
        errors.append(
            "public evaluation is missing hashed artifacts: "
            + ", ".join(sorted(missing_artifacts))
        )
    for name in sorted(REQUIRED_PUBLIC_ARTIFACTS & set(artifacts)):
        artifact = artifacts[name]
        if (
            not isinstance(artifact, dict)
            or not isinstance(artifact.get("path"), str)
            or not artifact["path"].strip()
        ):
            errors.append(f"public evaluation artifact {name} must include a path")
            continue
        artifact_path = PurePosixPath(artifact["path"])
        if artifact_path.is_absolute() or ".." in artifact_path.parts:
            errors.append(
                f"public evaluation artifact {name} path must be portable and relative"
            )
        digest = artifact.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            errors.append(f"public evaluation artifact {name} must include a SHA-256")
    systems = evaluation.get("systems", {})
    if not isinstance(systems, dict):
        systems = {}
    missing_systems = REQUIRED_PRIMARY_SYSTEMS - set(systems)
    if missing_systems:
        errors.append(
            "public evaluation is missing required systems: "
            + ", ".join(sorted(missing_systems))
        )
    for system in sorted(REQUIRED_PRIMARY_SYSTEMS & set(systems)):
        payload = systems[system]
        if not isinstance(payload, dict):
            errors.append(f"public evaluation system {system} is not an object")
            continue
        judgment_count = payload.get("judgments", 0)
        minimum_system_judgments = 60 + MIN_SHARED_SEEDS if overlap_coverage else 120
        if not isinstance(judgment_count, int) or judgment_count < minimum_system_judgments:
            errors.append(
                f"public evaluation system {system} has fewer than "
                f"{minimum_system_judgments} judgments"
            )
        if overlap_coverage:
            effective = payload.get("effective_seed_judgments")
            if not isinstance(effective, (int, float)) or effective < 60:
                errors.append(
                    f"public evaluation system {system} has fewer than 60 effective seed "
                    "judgments"
                )
        for family, required_keys in REQUIRED_METRIC_FAMILIES.items():
            metrics = payload.get(family, {})
            missing = required_keys - set(metrics if isinstance(metrics, dict) else {})
            if missing:
                errors.append(
                    f"public evaluation system {system}/{family} is missing metrics: "
                    + ", ".join(sorted(missing))
                )
                continue
            for metric_name in required_keys - {"relation_f1_by_type"}:
                if not isinstance(metrics.get(metric_name), (int, float)):
                    errors.append(
                        f"public evaluation metric {system}/{family}/{metric_name} "
                        "must be numeric"
                    )
            if family == "lineage":
                relation_metrics = metrics.get("relation_f1_by_type", {})
                missing_relations = REQUIRED_RELATION_TYPES - set(
                    relation_metrics if isinstance(relation_metrics, dict) else {}
                )
                if missing_relations:
                    errors.append(
                        f"public evaluation system {system}/lineage is missing relation F1: "
                        + ", ".join(sorted(missing_relations))
                    )
                elif any(
                    not isinstance(value, (int, float))
                    for value in relation_metrics.values()
                ):
                    errors.append(
                        f"public evaluation system {system}/lineage relation F1 must be numeric"
                    )
    if evaluation.get("errors"):
        errors.append("public evaluation contains unresolved gate errors")
    return errors


def validate_public_evaluation_artifacts(
    evaluation: dict[str, object], report_path: Path
) -> list[str]:
    errors = []
    artifacts = evaluation.get("artifacts", {})
    if not isinstance(artifacts, dict):
        return errors
    root = report_path.parent.resolve()
    for name, artifact in artifacts.items():
        if not isinstance(artifact, dict) or not isinstance(artifact.get("path"), str):
            continue
        candidate = (root / artifact["path"]).resolve()
        if root not in candidate.parents:
            errors.append(f"public evaluation artifact {name} escapes its report directory")
        elif not candidate.is_file():
            errors.append(f"public evaluation artifact {name} does not exist")
        elif sha256_file(candidate) != artifact.get("sha256"):
            errors.append(f"public evaluation artifact {name} hash does not match")
    return errors


def check_release_claims(readme: Path, public_evaluation: Path | None) -> ReleaseCheckResult:
    errors = []
    warnings = []
    text = readme.read_text(encoding="utf-8")
    section = _claim_section(text)
    if section is None:
        errors.append("README must contain exactly one effectiveness-claims marker block")
        return ReleaseCheckResult(errors, warnings)
    has_no_claim_marker = any(marker in section.casefold() for marker in NO_CLAIM_MARKERS)
    if public_evaluation is None:
        if not has_no_claim_marker:
            errors.append("README effectiveness claims require a public evaluation report")
        else:
            warnings.append("README correctly discloses that comparative evaluation is pending")
        return ReleaseCheckResult(errors, warnings)

    try:
        evaluation = json.loads(public_evaluation.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read public evaluation report: {exc}")
        return ReleaseCheckResult(errors, warnings)
    errors.extend(validate_public_evaluation(evaluation))
    errors.extend(validate_public_evaluation_artifacts(evaluation, public_evaluation))
    digest_marker = f"evaluation sha-256: {sha256_file(public_evaluation)}"
    if not has_no_claim_marker and digest_marker not in section.casefold():
        errors.append("README effectiveness claim block must include the public evaluation SHA-256")
    if has_no_claim_marker:
        warnings.append(
            "a public evaluation exists, but README still declares no comparative claims"
        )
    return ReleaseCheckResult(errors, warnings)
