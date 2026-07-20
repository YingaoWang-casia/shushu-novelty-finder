import json

from shushu_novelty.evaluation.release import END, START, check_release_claims
from shushu_novelty.io import sha256_file


def test_pending_evaluation_disclosure_passes_without_quality_claims(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        f"{START}\n当前没有公开的比较效果声明。\n{END}\n", encoding="utf-8"
    )

    result = check_release_claims(readme, None)

    assert result.ok
    assert result.warnings


def test_comparative_claim_without_public_evaluation_fails(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(f"{START}\nShushu outperforms bare.\n{END}\n", encoding="utf-8")

    result = check_release_claims(readme, None)

    assert not result.ok


def test_publishable_claim_is_bound_to_evaluation_hash(tmp_path):
    system_metrics = {
        "judgments": 120,
        "retrieval": {
            "known_prior_recall_at_k": 0.8,
            "duplicate_rate": 0.01,
            "metadata_completeness": 0.9,
            "accepted_preprint_accuracy": 0.9,
        },
        "evidence": {
            "citation_existence_precision": 0.9,
            "claim_entailment_accuracy": 0.8,
            "unsupported_claim_rate": 0.1,
            "full_text_verification_coverage": 0.7,
        },
        "lineage": {
            "relation_classification_macro_f1": 0.7,
            "relation_f1_by_type": {
                "ancestor": 0.7,
                "closest-prior": 0.7,
                "sibling": 0.7,
                "follow-up": 0.7,
                "benchmark": 0.7,
                "contrary-evidence": 0.7,
                "mechanism-transfer": 0.7,
            },
            "closest_prior_recall_at_5": 0.8,
            "saturated_contribution_precision": 0.7,
            "unsupported_lineage_edge_rate": 0.1,
        },
        "idea": {
            "problem_significance": 4,
            "novelty": 4,
            "method_specificity": 4,
            "feasibility": 4,
            "falsifiability": 4,
            "baseline_completeness": 4,
            "reviewer_defensibility": 4,
        },
        "calibration": {
            "strong_false_positive_rate": 0.1,
            "scoop_detection_recall": 0.9,
            "confidence_accuracy_correlation": 0.6,
            "kill_decision_precision": 0.9,
        },
    }
    artifact_names = [
        "benchmark_seeds",
        "blind_key",
        "blind_manifest",
        "blind_pairwise_responses",
        "blind_scalar_responses",
        "execution_manifest",
        "run_matrix",
        "scalar_judgments",
        "pairwise_judgments",
    ]
    artifacts = {}
    for name in artifact_names:
        path = tmp_path / f"{name}.jsonl"
        path.write_text(f"{name}\n", encoding="utf-8")
        artifacts[name] = {"path": path.name, "sha256": sha256_file(path)}
    evaluation = tmp_path / "public-results.json"
    evaluation.write_text(
        json.dumps(
            {
                "publishable": True,
                "primary_basis": "human",
                "human_raters": ["r1", "r2"],
                "human_judgments": 480,
                "cohens_kappa": 0.7,
                "pairwise": {"human_judgments": 720, "cohens_kappa": 0.7},
                "expected_seed_count": 60,
                "completed_run_count": 240,
                "artifacts": artifacts,
                "systems": {
                    "bare": system_metrics,
                    "self-reflection": system_metrics,
                    "shushu-v0.1": system_metrics,
                    "shushu-v0.2": system_metrics,
                },
                "errors": [],
            }
        ),
        encoding="utf-8",
    )
    readme = tmp_path / "README.md"
    readme.write_text(
        f"{START}\nShushu outperforms bare.\n"
        f"Evaluation SHA-256: {sha256_file(evaluation)}\n{END}\n",
        encoding="utf-8",
    )

    result = check_release_claims(readme, evaluation)

    assert result.ok

    (tmp_path / "run_matrix.jsonl").write_text("changed\n", encoding="utf-8")
    changed = check_release_claims(readme, evaluation)
    assert any("hash does not match" in error for error in changed.errors)


def test_public_evaluation_without_run_artifact_binding_fails(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        f"{START}\n当前没有公开的比较效果声明。\n{END}\n", encoding="utf-8"
    )
    evaluation = tmp_path / "public-results.json"
    evaluation.write_text(
        json.dumps({"publishable": True, "primary_basis": "human"}), encoding="utf-8"
    )

    result = check_release_claims(readme, evaluation)

    assert not result.ok
    assert any("240 completed" in error for error in result.errors)
    assert any("hashed artifacts" in error for error in result.errors)
