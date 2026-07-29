"""Aggregate benchmark metrics with human-rating primacy."""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from statistics import fmean
from typing import Iterable

from shushu_novelty.schemas import EvaluationJudgment, PairwiseJudgment

REQUIRED_PRIMARY_SYSTEMS = {
    "bare",
    "self-reflection",
    "shushu-v0.1",
    "shushu-v0.2",
}
MIN_SHARED_SEEDS = 12

IDEA_DIMENSIONS = [
    "problem_significance",
    "novelty",
    "method_specificity",
    "feasibility",
    "falsifiability",
    "baseline_completeness",
    "reviewer_defensibility",
]
RELATION_TYPES = [
    "ancestor",
    "closest-prior",
    "sibling",
    "follow-up",
    "benchmark",
    "contrary-evidence",
    "mechanism-transfer",
]


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _sum_ratio(
    judgments: list[EvaluationJudgment],
    numerator: str,
    denominator: str,
    group: str,
    weights: list[float] | None = None,
) -> float | None:
    item_weights = weights or [1.0] * len(judgments)
    objects = [getattr(item, group) for item in judgments]
    weighted_numerator = sum(
        weight * getattr(item, numerator) for item, weight in zip(objects, item_weights)
    )
    weighted_denominator = sum(
        weight * getattr(item, denominator) for item, weight in zip(objects, item_weights)
    )
    return weighted_numerator / weighted_denominator if weighted_denominator else None


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)


def _pearson(
    xs: list[float], ys: list[float], weights: list[float] | None = None
) -> float | None:
    if len(xs) < 2 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    item_weights = weights or [1.0] * len(xs)
    x_mean = _weighted_mean(xs, item_weights)
    y_mean = _weighted_mean(ys, item_weights)
    numerator = sum(
        weight * (x - x_mean) * (y - y_mean)
        for x, y, weight in zip(xs, ys, item_weights)
    )
    x_scale = math.sqrt(
        sum(weight * (x - x_mean) ** 2 for x, weight in zip(xs, item_weights))
    )
    y_scale = math.sqrt(
        sum(weight * (y - y_mean) ** 2 for y, weight in zip(ys, item_weights))
    )
    return numerator / (x_scale * y_scale) if x_scale and y_scale else None


def cohens_kappa(labels_a: list[str], labels_b: list[str]) -> float | None:
    if len(labels_a) != len(labels_b) or not labels_a:
        return None
    categories = set(labels_a) | set(labels_b)
    observed = sum(a == b for a, b in zip(labels_a, labels_b)) / len(labels_a)
    expected = sum(
        (labels_a.count(category) / len(labels_a)) * (labels_b.count(category) / len(labels_b))
        for category in categories
    )
    return (observed - expected) / (1 - expected) if expected < 1 else 1.0


def human_interrater_kappa(judgments: list[EvaluationJudgment]) -> float | None:
    humans = [item for item in judgments if item.rater_type == "human"]
    by_rater: dict[str, dict[tuple[str, str], str]] = defaultdict(dict)
    for item in humans:
        by_rater[item.rater_id][(item.seed_id, item.system)] = item.idea.novelty_verdict
    kappas = []
    for left, right in combinations(sorted(by_rater), 2):
        shared = sorted(set(by_rater[left]) & set(by_rater[right]))
        if shared:
            value = cohens_kappa(
                [by_rater[left][key] for key in shared],
                [by_rater[right][key] for key in shared],
            )
            if value is not None:
                kappas.append(value)
    return fmean(kappas) if kappas else None


def _canonical_pairwise(item: PairwiseJudgment) -> tuple[tuple[str, str], str]:
    pair = tuple(sorted((item.system_left, item.system_right)))
    if item.preference == "tie":
        return pair, "tie"
    preferred = item.system_left if item.preference == "left" else item.system_right
    return pair, preferred


def human_pairwise_kappa(judgments: list[PairwiseJudgment]) -> float | None:
    humans = [item for item in judgments if item.rater_type == "human"]
    by_rater: dict[str, dict[tuple[str, tuple[str, str]], str]] = defaultdict(dict)
    for item in humans:
        pair, preference = _canonical_pairwise(item)
        by_rater[item.rater_id][(item.seed_id, pair)] = preference
    kappas = []
    for left, right in combinations(sorted(by_rater), 2):
        shared = sorted(set(by_rater[left]) & set(by_rater[right]))
        if shared:
            value = cohens_kappa(
                [by_rater[left][key] for key in shared],
                [by_rater[right][key] for key in shared],
            )
            if value is not None:
                kappas.append(value)
    return fmean(kappas) if kappas else None


def aggregate_system(judgments: list[EvaluationJudgment]) -> dict[str, object]:
    ratings_per_seed: dict[str, int] = defaultdict(int)
    for item in judgments:
        ratings_per_seed[item.seed_id] += 1
    weights = [1.0 / ratings_per_seed[item.seed_id] for item in judgments]
    strong = [item for item in judgments if item.idea.novelty_verdict == "strong"]
    strong_weights = [
        weight
        for item, weight in zip(judgments, weights)
        if item.idea.novelty_verdict == "strong"
    ]
    scoop_cases = [item for item in judgments if item.calibration.is_scoop_case]
    scoop_weights = [
        weight for item, weight in zip(judgments, weights) if item.calibration.is_scoop_case
    ]
    kill_positive = [item for item in judgments if item.calibration.kill_recommended]
    kill_weights = [
        weight
        for item, weight in zip(judgments, weights)
        if item.calibration.kill_recommended
    ]
    relation_f1 = []
    relation_metrics = {}
    for relation in RELATION_TYPES:
        assessments = [
            next(item for item in judgment.lineage.relations if item.relation == relation)
            for judgment in judgments
        ]
        true_positive = sum(
            weight * item.true_positive for item, weight in zip(assessments, weights)
        )
        false_positive = sum(
            weight * item.false_positive for item, weight in zip(assessments, weights)
        )
        false_negative = sum(
            weight * item.false_negative for item, weight in zip(assessments, weights)
        )
        denominator = 2 * true_positive + false_positive + false_negative
        value = 2 * true_positive / denominator if denominator else None
        relation_metrics[relation] = value
        if value is not None:
            relation_f1.append(value)
    return {
        "judgments": len(judgments),
        "effective_seed_judgments": sum(weights),
        "retrieval": {
            "known_prior_recall_at_k": _sum_ratio(
                judgments,
                "known_prior_retrieved_at_k",
                "known_prior_total",
                "retrieval",
                weights,
            ),
            "duplicate_rate": _sum_ratio(
                judgments, "duplicate_records", "retrieved_records", "retrieval", weights
            ),
            "metadata_completeness": _sum_ratio(
                judgments,
                "metadata_fields_present",
                "metadata_fields_total",
                "retrieval",
                weights,
            ),
            "accepted_preprint_accuracy": _sum_ratio(
                judgments,
                "publication_labels_correct",
                "publication_labels_total",
                "retrieval",
                weights,
            ),
        },
        "evidence": {
            "citation_existence_precision": _sum_ratio(
                judgments, "citations_existing", "citations_total", "evidence", weights
            ),
            "claim_entailment_accuracy": _sum_ratio(
                judgments, "claims_entailed", "claims_total", "evidence", weights
            ),
            "unsupported_claim_rate": _sum_ratio(
                judgments, "unsupported_claims", "claims_total", "evidence", weights
            ),
            "full_text_verification_coverage": _sum_ratio(
                judgments,
                "full_text_verified_claims",
                "strong_claims",
                "evidence",
                weights,
            ),
        },
        "lineage": {
            "relation_classification_macro_f1": (
                fmean(relation_f1) if relation_f1 else None
            ),
            "relation_f1_by_type": relation_metrics,
            "closest_prior_recall_at_5": _sum_ratio(
                judgments,
                "closest_prior_retrieved_at_5",
                "closest_prior_total",
                "lineage",
                weights,
            ),
            "saturated_contribution_precision": _sum_ratio(
                judgments,
                "saturated_contributions_correct",
                "saturated_contributions_predicted",
                "lineage",
                weights,
            ),
            "unsupported_lineage_edge_rate": _sum_ratio(
                judgments,
                "unsupported_lineage_edges",
                "lineage_edges_total",
                "lineage",
                weights,
            ),
        },
        "idea": {
            dimension: _weighted_mean(
                [getattr(item.idea, dimension) for item in judgments], weights
            )
            for dimension in IDEA_DIMENSIONS
        },
        "calibration": {
            "strong_false_positive_rate": (
                sum(
                    weight * (not item.calibration.prediction_correct)
                    for item, weight in zip(strong, strong_weights)
                )
                / sum(strong_weights)
                if strong_weights
                else None
            ),
            "scoop_detection_recall": (
                sum(
                    weight * item.calibration.scoop_detected
                    for item, weight in zip(scoop_cases, scoop_weights)
                )
                / sum(scoop_weights)
                if scoop_weights
                else None
            ),
            "confidence_accuracy_correlation": _pearson(
                [item.calibration.confidence for item in judgments],
                [float(item.calibration.prediction_correct) for item in judgments],
                weights,
            ),
            "kill_decision_precision": (
                sum(
                    weight * item.calibration.kill_correct
                    for item, weight in zip(kill_positive, kill_weights)
                )
                / sum(kill_weights)
                if kill_weights
                else None
            ),
        },
    }


@dataclass(frozen=True)
class EvaluationAggregation:
    report: dict[str, object]
    errors: list[str]
    warnings: list[str]

    @property
    def publishable(self) -> bool:
        return not self.errors


def aggregate_evaluation(
    judgments: Iterable[EvaluationJudgment],
    expected_seed_ids: Iterable[str] | None = None,
    pairwise_judgments: Iterable[PairwiseJudgment] = (),
) -> EvaluationAggregation:
    items = list(judgments)
    pairwise_items = list(pairwise_judgments)
    errors = []
    warnings = []
    humans = [item for item in items if item.rater_type == "human"]
    llms = [item for item in items if item.rater_type == "llm"]
    pairwise_humans = [item for item in pairwise_items if item.rater_type == "human"]
    pairwise_llms = [item for item in pairwise_items if item.rater_type == "llm"]
    human_raters = sorted({item.rater_id for item in humans})
    judgment_ids = [item.judgment_id for item in items]
    if len(judgment_ids) != len(set(judgment_ids)):
        errors.append("judgment IDs must be unique")
    human_keys = [(item.rater_id, item.seed_id, item.system) for item in humans]
    if len(human_keys) != len(set(human_keys)):
        errors.append("each human rater may submit one judgment per seed/system")
    if len(human_raters) < 2:
        errors.append("at least two human raters are required for publishable evaluation")
    pairwise_raters = sorted({item.rater_id for item in pairwise_humans})
    if pairwise_raters != human_raters:
        errors.append("the same human raters must complete scalar and pairwise judgments")
    pairwise_ids = [item.pairwise_id for item in pairwise_items]
    if len(pairwise_ids) != len(set(pairwise_ids)):
        errors.append("pairwise judgment IDs must be unique")
    pairwise_keys = []
    for item in pairwise_humans:
        pair, _ = _canonical_pairwise(item)
        pairwise_keys.append((item.rater_id, item.seed_id, pair))
    if len(pairwise_keys) != len(set(pairwise_keys)):
        errors.append("each human rater may submit one judgment per seed/system pair")
    observed_systems = {item.system for item in humans}
    missing_systems = REQUIRED_PRIMARY_SYSTEMS - observed_systems
    if missing_systems:
        errors.append(
            "human evaluation is missing required systems: "
            + ", ".join(sorted(missing_systems))
        )
    expected_seeds = set(expected_seed_ids or [])
    if expected_seed_ids is not None and not expected_seeds:
        errors.append("expected benchmark seed IDs cannot be empty")
    required_pairs = set(combinations(sorted(REQUIRED_PRIMARY_SYSTEMS), 2))
    scalar_seed_raters: dict[str, set[str]] = defaultdict(set)
    pairwise_seed_raters: dict[str, set[str]] = defaultdict(set)
    rater_seed_counts: dict[str, int] = {}
    for rater_id in human_raters:
        scalar_by_seed: dict[str, set[str]] = defaultdict(set)
        pairwise_by_seed: dict[str, set[tuple[str, str]]] = defaultdict(set)
        for item in humans:
            if item.rater_id == rater_id:
                scalar_by_seed[item.seed_id].add(item.system)
        for item in pairwise_humans:
            if item.rater_id == rater_id:
                pairwise_by_seed[item.seed_id].add(_canonical_pairwise(item)[0])
        for seed_id, systems in sorted(scalar_by_seed.items()):
            missing = REQUIRED_PRIMARY_SYSTEMS - systems
            if missing:
                errors.append(
                    f"human rater {rater_id} seed {seed_id} is missing {len(missing)} "
                    "required system judgments"
                )
            scalar_seed_raters[seed_id].add(rater_id)
        for seed_id, pairs in sorted(pairwise_by_seed.items()):
            missing = required_pairs - pairs
            if missing:
                errors.append(
                    f"human rater {rater_id} seed {seed_id} is missing {len(missing)} "
                    "required pairwise judgments"
                )
            pairwise_seed_raters[seed_id].add(rater_id)
        if set(scalar_by_seed) != set(pairwise_by_seed):
            errors.append(
                f"human rater {rater_id} must rate the same seeds in scalar and pairwise files"
            )
        rater_seed_counts[rater_id] = len(scalar_by_seed)

    collective_seeds = set(scalar_seed_raters)
    shared_seed_ids = {
        seed_id
        for seed_id, raters in scalar_seed_raters.items()
        if len(raters) >= 2 and len(pairwise_seed_raters.get(seed_id, set())) >= 2
    }
    if expected_seeds:
        unknown_seeds = {
            item.seed_id for item in [*items, *pairwise_items]
        } - expected_seeds
        if unknown_seeds:
            errors.append(
                "judgments reference unknown benchmark seeds: "
                + ", ".join(sorted(unknown_seeds))
            )
        missing_collective = expected_seeds - collective_seeds
        if missing_collective:
            errors.append(
                "human ratings collectively miss benchmark seeds: "
                + ", ".join(sorted(missing_collective))
            )
        required_shared = min(MIN_SHARED_SEEDS, len(expected_seeds))
        if len(shared_seed_ids) < required_shared:
            errors.append(
                f"human raters must share at least {required_shared} complete seeds for "
                "agreement"
            )
    elif human_raters:
        warnings.append(
            "benchmark seed suite was not supplied; full 60-seed coverage was not verified"
        )
    kappa = human_interrater_kappa(items)
    if len(human_raters) >= 2 and kappa is None:
        errors.append("human raters have no shared seed/system judgments for agreement")
    if llms:
        warnings.append("LLM judgments are auxiliary and excluded from primary system metrics")
    pairwise_kappa = human_pairwise_kappa(pairwise_items)
    if len(human_raters) >= 2 and pairwise_kappa is None:
        errors.append("human raters have no shared pairwise judgments for agreement")
    if pairwise_llms:
        warnings.append("LLM pairwise judgments are auxiliary and excluded from primary evidence")
    primary = humans
    by_system: dict[str, list[EvaluationJudgment]] = defaultdict(list)
    for item in primary:
        by_system[item.system].append(item)
    if expected_seeds and shared_seed_ids == expected_seeds and all(
        count == len(expected_seeds) for count in rater_seed_counts.values()
    ):
        rating_design = "complete"
    elif (
        expected_seeds
        and collective_seeds == expected_seeds
        and len(shared_seed_ids) >= min(MIN_SHARED_SEEDS, len(expected_seeds))
    ):
        rating_design = "balanced-overlap"
    else:
        rating_design = "incomplete-or-unverified"
    report = {
        "schema_version": "1.0",
        "primary_basis": "human" if len(human_raters) >= 2 else "insufficient-human-ratings",
        "rating_design": rating_design,
        "human_raters": human_raters,
        "human_judgments": len(humans),
        "auxiliary_llm_judgments": len(llms),
        "expected_seed_count": len(expected_seeds) if expected_seeds else None,
        "coverage": {
            "collective_seed_count": len(collective_seeds),
            "shared_seed_count": len(shared_seed_ids),
            "shared_seed_ids": sorted(shared_seed_ids),
            "minimum_raters_per_seed": (
                min(len(scalar_seed_raters.get(seed_id, set())) for seed_id in expected_seeds)
                if expected_seeds
                else None
            ),
            "maximum_raters_per_seed": (
                max(len(scalar_seed_raters.get(seed_id, set())) for seed_id in expected_seeds)
                if expected_seeds
                else None
            ),
            "rater_seed_counts": rater_seed_counts,
        },
        "cohens_kappa": kappa,
        "pairwise": {
            "human_judgments": len(pairwise_humans),
            "auxiliary_llm_judgments": len(pairwise_llms),
            "cohens_kappa": pairwise_kappa,
        },
        "systems": {
            system: aggregate_system(system_judgments)
            for system, system_judgments in sorted(by_system.items())
        },
    }
    return EvaluationAggregation(report=report, errors=errors, warnings=warnings)
