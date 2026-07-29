from shushu_novelty.evaluation.benchmark import (
    build_run_matrix,
    collect_run_outputs,
    validate_suite,
)
from shushu_novelty.schemas import BenchmarkSeed


def make_seed(index: int, case_type: str, domain: str) -> BenchmarkSeed:
    data = {
        "seed_id": f"B-{index:03d}",
        "case_type": case_type,
        "domain": domain,
        "prompt": f"Generate a research audit for unique problem {index}.",
        "expected_behavior": ["trace evidence"],
        "provenance": "test",
    }
    if case_type == "seed-paper":
        data["reference"] = {
            "source": "openreview",
            "identifier": f"id-{index}",
            "title": f"Paper {index}",
        }
    if case_type in {"known-scoop", "mechanism-transfer"}:
        data["candidate_idea"] = f"Candidate {index}"
    if case_type == "known-scoop":
        data["known_prior_ids"] = [f"prior-{index}"]
    return BenchmarkSeed.model_validate(data)


def valid_suite():
    domains = [
        "llm-rag",
        "cv-multimodal",
        "speech",
        "agents",
        "systems",
        "data-mining",
        "security",
        "scientific-ml",
    ]
    case_types = ["broad-direction"] * 20 + ["seed-paper"] * 20
    case_types += ["known-scoop"] * 10 + ["mechanism-transfer"] * 10
    return [
        make_seed(index, case_type, domains[(index - 1) % len(domains)])
        for index, case_type in enumerate(case_types, 1)
    ]


def test_valid_suite_has_required_distribution():
    result = validate_suite(valid_suite())
    assert result.ok
    assert result.counts["known-scoop"] == 10


def test_run_matrix_has_four_baselines_per_seed():
    runs = build_run_matrix(valid_suite())
    assert len(runs) == 240
    assert len({run.prompt_hash for run in runs}) == 60


def test_collection_hashes_every_nonempty_baseline_output(tmp_path):
    runs = build_run_matrix(valid_suite())
    for run in runs:
        output = tmp_path / run.output_path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(f"result for {run.run_id}\n", encoding="utf-8")

    result = collect_run_outputs(runs, tmp_path)

    assert result.ok
    assert all(run.status == "complete" for run in result.runs)
    assert all(run.output_sha256 for run in result.runs)


def test_collection_rejects_missing_outputs(tmp_path):
    result = collect_run_outputs(build_run_matrix(valid_suite()), tmp_path)

    assert not result.ok
    assert any("output is missing" in error for error in result.errors)
