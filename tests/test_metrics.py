from itertools import combinations

from shushu_novelty.evaluation.metrics import aggregate_evaluation, cohens_kappa
from shushu_novelty.schemas import EvaluationJudgment, PairwiseJudgment

SYSTEMS = ["bare", "self-reflection", "shushu-v0.1", "shushu-v0.2"]


def make_judgment(
    seed_id: str,
    system: str,
    rater_id: str,
    rater_type: str = "human",
) -> EvaluationJudgment:
    return EvaluationJudgment.model_validate(
        {
            "judgment_id": f"J-{seed_id}-{system}-{rater_id}",
            "seed_id": seed_id,
            "system": system,
            "rater_id": rater_id,
            "rater_type": rater_type,
            "blind": True,
            "research_experience_years": 3 if rater_type == "human" else None,
            "retrieval": {
                "known_prior_total": 2,
                "known_prior_retrieved_at_k": 1,
                "retrieved_records": 10,
                "duplicate_records": 1,
                "metadata_fields_total": 8,
                "metadata_fields_present": 6,
                "publication_labels_total": 4,
                "publication_labels_correct": 3,
            },
            "evidence": {
                "citations_total": 4,
                "citations_existing": 3,
                "claims_total": 5,
                "claims_entailed": 4,
                "unsupported_claims": 1,
                "strong_claims": 2,
                "full_text_verified_claims": 1,
            },
            "lineage": {
                "relations": [
                    {
                        "relation": relation,
                        "true_positive": 1,
                        "false_positive": 0,
                        "false_negative": 0,
                    }
                    for relation in [
                        "ancestor",
                        "closest-prior",
                        "sibling",
                        "follow-up",
                        "benchmark",
                        "contrary-evidence",
                        "mechanism-transfer",
                    ]
                ],
                "closest_prior_total": 2,
                "closest_prior_retrieved_at_5": 1,
                "saturated_contributions_predicted": 2,
                "saturated_contributions_correct": 1,
                "lineage_edges_total": 4,
                "unsupported_lineage_edges": 1,
            },
            "idea": {
                "problem_significance": 4,
                "novelty": 4,
                "method_specificity": 4,
                "feasibility": 4,
                "falsifiability": 4,
                "baseline_completeness": 4,
                "reviewer_defensibility": 4,
                "novelty_verdict": "strong",
            },
            "calibration": {
                "confidence": 0.8,
                "prediction_correct": True,
                "is_scoop_case": True,
                "scoop_detected": True,
                "kill_recommended": True,
                "kill_correct": True,
            },
        }
    )


def make_pairwise(seed_id: str, left: str, right: str, rater_id: str) -> PairwiseJudgment:
    return PairwiseJudgment(
        pairwise_id=f"PW-{seed_id}-{left}-{right}-{rater_id}",
        seed_id=seed_id,
        system_left=left,
        system_right=right,
        preference="right",
        rater_id=rater_id,
        rater_type="human",
        blind=True,
        research_experience_years=3,
        rationale="The right output is more evidence-grounded in this fixture.",
    )


def paired_ratings(seed_ids):
    return [
        make_pairwise(seed, left, right, rater)
        for seed in seed_ids
        for left, right in combinations(SYSTEMS, 2)
        for rater in ["rater-a", "rater-b"]
    ]


def test_cohens_kappa_for_perfect_agreement():
    assert cohens_kappa(["weak", "strong"], ["weak", "strong"]) == 1.0


def test_publishable_aggregation_requires_paired_human_coverage():
    judgments = [
        make_judgment(seed, system, rater)
        for seed in ["B-001", "B-002"]
        for system in SYSTEMS
        for rater in ["rater-a", "rater-b"]
    ]
    judgments.append(make_judgment("B-001", "bare", "judge", "llm"))

    result = aggregate_evaluation(
        judgments,
        ["B-001", "B-002"],
        paired_ratings(["B-001", "B-002"]),
    )

    assert result.publishable
    assert result.report["human_judgments"] == 16
    assert result.report["auxiliary_llm_judgments"] == 1
    assert result.report["cohens_kappa"] == 1.0
    assert result.report["pairwise"]["cohens_kappa"] == 1.0
    assert result.report["systems"]["bare"]["retrieval"]["known_prior_recall_at_k"] == 0.5
    assert result.report["systems"]["bare"]["lineage"] == {
        "relation_classification_macro_f1": 1.0,
        "relation_f1_by_type": {relation: 1.0 for relation in [
            "ancestor",
            "closest-prior",
            "sibling",
            "follow-up",
            "benchmark",
            "contrary-evidence",
            "mechanism-transfer",
        ]},
        "closest_prior_recall_at_5": 0.5,
        "saturated_contribution_precision": 0.5,
        "unsupported_lineage_edge_rate": 0.25,
    }
    assert any("excluded" in warning for warning in result.warnings)


def test_incomplete_human_coverage_is_not_publishable():
    judgments = [
        make_judgment("B-001", system, "rater-a")
        for system in SYSTEMS
    ]
    judgments += [
        make_judgment("B-001", system, "rater-b")
        for system in SYSTEMS[:-1]
    ]

    result = aggregate_evaluation(judgments, ["B-001"], paired_ratings(["B-001"]))

    assert not result.publishable
    assert any("missing 1 required" in error for error in result.errors)


def test_llm_only_judgments_cannot_be_primary_evidence():
    judgments = [make_judgment("B-001", system, "judge", "llm") for system in SYSTEMS]

    result = aggregate_evaluation(judgments, ["B-001"])

    assert not result.publishable
    assert result.report["systems"] == {}
    assert any("two human raters" in error for error in result.errors)


def test_full_sixty_seed_human_matrix_is_publishable():
    seed_ids = [f"B-{index:03d}" for index in range(1, 61)]
    judgments = [
        make_judgment(seed, system, rater)
        for seed in seed_ids
        for system in SYSTEMS
        for rater in ["rater-a", "rater-b"]
    ]

    result = aggregate_evaluation(judgments, seed_ids, paired_ratings(seed_ids))

    assert result.publishable
    assert result.report["human_judgments"] == 480
    assert result.report["pairwise"]["human_judgments"] == 720
    assert result.report["expected_seed_count"] == 60
