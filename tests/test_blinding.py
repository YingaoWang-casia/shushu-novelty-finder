import hashlib
import json
from pathlib import Path

import pytest

from shushu_novelty.cli import main
from shushu_novelty.errors import InputError
from shushu_novelty.evaluation.blinding import (
    create_blind_packages,
    lock_rater_responses,
    unblind_responses,
    validate_unblinded_responses,
    verify_blind_package_manifest,
)
from shushu_novelty.io import validate_jsonl, write_jsonl
from shushu_novelty.schemas import BenchmarkRun, BenchmarkSeed, EvaluationJudgment
from shushu_novelty.schemas.blind_evaluation import (
    BlindOutputAssignment,
    BlindOutputKey,
    BlindPairwiseAssignment,
    BlindPairwiseResponse,
    BlindResponseLock,
    BlindScalarResponse,
)

SYSTEMS = ["bare", "self-reflection", "shushu-v0.1", "shushu-v0.2"]


def benchmark_seeds():
    return validate_jsonl(Path("evals/benchmark-v1.jsonl"), BenchmarkSeed)


def complete_matrix(tmp_path, seeds):
    runs = []
    for seed in seeds:
        seed_id = seed.seed_id
        for system in SYSTEMS:
            relative = f"evals/results/{system}/{seed_id}.md"
            output = tmp_path / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(f"output for {seed_id}\n", encoding="utf-8")
            runs.append(
                BenchmarkRun(
                    run_id=f"{seed_id}-{system}",
                    seed_id=seed_id,
                    system=system,
                    status="complete",
                    output_path=relative,
                    model="fixture",
                    prompt_hash=hashlib.sha256(seed.prompt.encode()).hexdigest(),
                    adapter_sha256="b" * 64,
                    output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                )
            )
    return runs


def complete_rater_responses(rater_root, rater_id="rater-a"):
    fixture = EvaluationJudgment.model_validate(
        json.loads(Path("evals/judgment.example.jsonl").read_text(encoding="utf-8"))
    )
    scalar = []
    assignments = validate_jsonl(
        rater_root / "scalar-assignments.jsonl", BlindOutputAssignment
    )
    for assignment in assignments:
        scalar.append(
            BlindScalarResponse(
                assignment_id=assignment.assignment_id,
                rater_id=rater_id,
                research_experience_years=3,
                seed_id=assignment.seed_id,
                output_id=assignment.output_id,
                retrieval=fixture.retrieval,
                evidence=fixture.evidence,
                lineage=fixture.lineage,
                idea=fixture.idea,
                calibration=fixture.calibration,
                notes="independently rated fixture",
            )
        )
    pairwise = []
    pairs = validate_jsonl(
        rater_root / "pairwise-assignments.jsonl", BlindPairwiseAssignment
    )
    for assignment in pairs:
        pairwise.append(
            BlindPairwiseResponse(
                assignment_id=assignment.assignment_id,
                rater_id=rater_id,
                research_experience_years=3,
                seed_id=assignment.seed_id,
                output_left=assignment.output_left,
                output_right=assignment.output_right,
                preference="tie",
                rationale="The fixture outputs are equivalent.",
            )
        )
    return scalar, pairwise


def test_blind_pack_has_full_opaque_coverage_and_separate_key(tmp_path):
    output_dir = tmp_path / "blind"
    seeds = benchmark_seeds()

    result = create_blind_packages(
        complete_matrix(tmp_path, seeds),
        seeds,
        tmp_path,
        output_dir,
        ["rater-a", "rater-b"],
        secret=b"test secret" * 4,
    )

    assert result.scalar_assignments == 480
    assert result.pairwise_assignments == 720
    assert result.key_records == 480
    scalar_text = (
        output_dir / "raters" / "rater-a" / "scalar-assignments.jsonl"
    ).read_text(encoding="utf-8")
    assert "shushu-v0.2" not in scalar_text
    assert "self-reflection" not in scalar_text
    assert "shushu-v0.2" in (
        output_dir / "coordinator" / "blind-key.jsonl"
    ).read_text(encoding="utf-8")
    assert len(
        (output_dir / "raters" / "rater-a" / "benchmark-seeds.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ) == 60
    rater_root = output_dir / "raters" / "rater-a"
    guide = (rater_root / "README.md").read_text(encoding="utf-8")
    assert "shushu" not in guide.casefold()
    assert "self-reflection" not in guide.casefold()
    assert (rater_root / "schemas" / "blind-scalar-response.schema.json").is_file()
    assert (rater_root / "schemas" / "blind-pairwise-response.schema.json").is_file()
    assert (rater_root / "schemas" / "blind-response-lock.schema.json").is_file()
    manifest = json.loads(
        (output_dir / "coordinator" / "manifest.json").read_text(encoding="utf-8")
    )
    assert len(manifest["rater_material_sha256"]) == 4
    assert manifest["blind_key_sha256"] == hashlib.sha256(
        (output_dir / "coordinator" / "blind-key.jsonl").read_bytes()
    ).hexdigest()


def test_rater_response_lock_validates_coverage_bindings_and_hashes(tmp_path):
    seeds = benchmark_seeds()
    blind_dir = tmp_path / "blind"
    create_blind_packages(
        complete_matrix(tmp_path, seeds),
        seeds,
        tmp_path,
        blind_dir,
        ["rater-a", "rater-b"],
        secret=b"test secret" * 4,
    )
    rater_root = blind_dir / "raters" / "rater-a"
    scalar, pairwise = complete_rater_responses(rater_root)
    scalar_path = rater_root / "blind-scalar-responses.jsonl"
    pairwise_path = rater_root / "blind-pairwise-responses.jsonl"
    write_jsonl(scalar, scalar_path)
    write_jsonl(pairwise, pairwise_path)
    commitment = hashlib.sha256(
        (blind_dir / "coordinator" / "manifest.json").read_bytes()
    ).hexdigest()
    lock_path = rater_root / "response-lock.json"

    assert main(
        [
            "benchmark",
            "lock-responses",
            str(rater_root),
            "--blind-scalar",
            str(scalar_path),
            "--blind-pairwise",
            str(pairwise_path),
            "--blind-manifest-sha256",
            commitment,
            "--output",
            str(lock_path),
        ]
    ) == 0
    lock = BlindResponseLock.model_validate(json.loads(lock_path.read_text()))
    assert lock.rater_id == "rater-a"
    assert lock.scalar_responses == 240
    assert lock.pairwise_responses == 360
    assert lock.scalar_responses_sha256 == hashlib.sha256(
        scalar_path.read_bytes()
    ).hexdigest()
    assert lock.pairwise_responses_sha256 == hashlib.sha256(
        pairwise_path.read_bytes()
    ).hexdigest()

    scalar[0].output_id = scalar[1].output_id
    write_jsonl(scalar, scalar_path)
    with pytest.raises(InputError, match="changes immutable assignment fields"):
        lock_rater_responses(
            rater_root,
            scalar_path,
            pairwise_path,
            commitment,
            rater_root / "tampered-lock.json",
        )

    scalar, _ = complete_rater_responses(rater_root)
    write_jsonl(scalar, scalar_path)
    write_jsonl(pairwise[:-1], pairwise_path)
    with pytest.raises(InputError, match="exactly 360 pairwise"):
        lock_rater_responses(
            rater_root,
            scalar_path,
            pairwise_path,
            commitment,
            rater_root / "incomplete-lock.json",
        )


def test_unblind_joins_system_identity_only_after_response_lock():
    fixture = EvaluationJudgment.model_validate(
        json.loads(Path("evals/judgment.example.jsonl").read_text(encoding="utf-8"))
    )
    scalar = BlindScalarResponse(
        assignment_id="BA-rater-a:B-001:O-1111111111111111",
        rater_id="rater-a",
        research_experience_years=3,
        seed_id="B-001",
        output_id="O-1111111111111111",
        retrieval=fixture.retrieval,
        evidence=fixture.evidence,
        lineage=fixture.lineage,
        idea=fixture.idea,
        calibration=fixture.calibration,
        notes="locked",
    )
    pairwise = BlindPairwiseResponse(
        assignment_id="BPA-rater-a:B-001:1",
        rater_id="rater-a",
        research_experience_years=3,
        seed_id="B-001",
        output_left="O-1111111111111111",
        output_right="O-2222222222222222",
        preference="right",
        rationale="The right output is more defensible.",
    )
    keys = [
        BlindOutputKey(
            rater_id="rater-a",
            seed_id="B-001",
            output_id="O-1111111111111111",
            system="bare",
            source_output_path="bare.md",
            output_sha256="a" * 64,
        ),
        BlindOutputKey(
            rater_id="rater-a",
            seed_id="B-001",
            output_id="O-2222222222222222",
            system="shushu-v0.2",
            source_output_path="v02.md",
            output_sha256="b" * 64,
        ),
    ]

    scalar_joined, pairwise_joined = unblind_responses([scalar], [pairwise], keys)

    assert scalar_joined[0].system == "bare"
    assert scalar_joined[0].blind is True
    assert pairwise_joined[0].system_left == "bare"
    assert pairwise_joined[0].system_right == "shushu-v0.2"
    assert pairwise_joined[0].preference == "right"
    assert not validate_unblinded_responses(
        [scalar], [pairwise], keys, scalar_joined, pairwise_joined
    )
    scalar_joined[0].notes = "altered after unblind"
    assert any(
        "scalar judgments differ" in error
        for error in validate_unblinded_responses(
            [scalar], [pairwise], keys, scalar_joined, pairwise_joined
        )
    )


def test_blind_manifest_detects_output_and_key_tampering(tmp_path):
    seeds = benchmark_seeds()
    output_dir = tmp_path / "blind"
    create_blind_packages(
        complete_matrix(tmp_path, seeds),
        seeds,
        tmp_path,
        output_dir,
        ["rater-a", "rater-b"],
        secret=b"test secret" * 4,
    )
    key = output_dir / "coordinator" / "blind-key.jsonl"
    manifest = output_dir / "coordinator" / "manifest.json"

    verify_blind_package_manifest(key, manifest)
    output = next((output_dir / "raters" / "rater-a" / "outputs").rglob("*.md"))
    original = output.read_bytes()
    output.write_bytes(original + b"tampered\n")

    with pytest.raises(InputError, match="rater artifact hash does not match"):
        verify_blind_package_manifest(key, manifest)

    output.write_bytes(original)
    verify_blind_package_manifest(key, manifest)
    key.write_text(key.read_text(encoding="utf-8") + " \n", encoding="utf-8")

    with pytest.raises(InputError, match="hash does not match"):
        verify_blind_package_manifest(key, manifest)


def test_blind_pack_rejects_identity_leakage_inside_output(tmp_path):
    seeds = benchmark_seeds()
    runs = complete_matrix(tmp_path, seeds)
    output = tmp_path / runs[0].output_path
    output.write_text("Generated by Shushu.\n", encoding="utf-8")
    runs[0].output_sha256 = hashlib.sha256(output.read_bytes()).hexdigest()

    with pytest.raises(InputError, match="identity marker"):
        create_blind_packages(
            runs,
            seeds,
            tmp_path,
            tmp_path / "blind",
            ["rater-a", "rater-b"],
            secret=b"test secret" * 4,
        )


def test_blind_pack_allows_self_reflection_as_research_term(tmp_path):
    seeds = benchmark_seeds()
    runs = complete_matrix(tmp_path, seeds)
    output = tmp_path / runs[0].output_path
    output.write_text(
        "Stage D studies learned self-reflection and internal-state policies.\n",
        encoding="utf-8",
    )
    runs[0].output_sha256 = hashlib.sha256(output.read_bytes()).hexdigest()

    result = create_blind_packages(
        runs,
        seeds,
        tmp_path,
        tmp_path / "blind",
        ["rater-a", "rater-b"],
        secret=b"test secret" * 4,
    )

    assert result.scalar_assignments == 480


def test_blind_pack_rejects_explicit_self_reflection_profile(tmp_path):
    seeds = benchmark_seeds()
    runs = complete_matrix(tmp_path, seeds)
    output = tmp_path / runs[0].output_path
    output.write_text(
        "This answer was generated by the self-reflection profile.\n",
        encoding="utf-8",
    )
    runs[0].output_sha256 = hashlib.sha256(output.read_bytes()).hexdigest()

    with pytest.raises(InputError, match="self-reflection system/profile"):
        create_blind_packages(
            runs,
            seeds,
            tmp_path,
            tmp_path / "blind",
            ["rater-a", "rater-b"],
            secret=b"test secret" * 4,
        )


def test_full_blind_unblind_and_score_cli_pipeline(tmp_path):
    seeds = benchmark_seeds()
    seed_path = tmp_path / "benchmark-v1.jsonl"
    write_jsonl(seeds, seed_path)
    runs = complete_matrix(tmp_path, seeds)
    matrix_path = tmp_path / "run-matrix.jsonl"
    write_jsonl(runs, matrix_path)
    adapter_path = tmp_path / "adapters.json"
    adapter_path.write_text("fixture adapter\n", encoding="utf-8")
    execution_manifest = tmp_path / "execution-manifest.json"
    execution_manifest.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "status": "complete",
                "started_at": "2026-01-01T00:00:00Z",
                "completed_at": "2026-01-01T01:00:00Z",
                "model": "fixture",
                "codex_cli_version": "fixture-runtime",
                "adapter_path": str(adapter_path),
                "adapter_sha256": hashlib.sha256(adapter_path.read_bytes()).hexdigest(),
                "benchmark_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
                "completed_run_matrix_sha256": hashlib.sha256(
                    matrix_path.read_bytes()
                ).hexdigest(),
                "completed_run_matrix_path": str(matrix_path),
                "systems": SYSTEMS,
                "expected_runs": 240,
            }
        ),
        encoding="utf-8",
    )
    blind_dir = tmp_path / "blind"
    create_blind_packages(
        runs,
        seeds,
        tmp_path,
        blind_dir,
        ["rater-a", "rater-b"],
        secret=b"test secret" * 4,
    )
    fixture = EvaluationJudgment.model_validate(
        json.loads(Path("evals/judgment.example.jsonl").read_text(encoding="utf-8"))
    )
    scalar_responses = []
    pairwise_responses = []
    for rater_id in ["rater-a", "rater-b"]:
        rater_root = blind_dir / "raters" / rater_id
        assignments = validate_jsonl(
            rater_root / "scalar-assignments.jsonl", BlindOutputAssignment
        )
        for assignment in assignments:
            scalar_responses.append(
                BlindScalarResponse(
                    assignment_id=assignment.assignment_id,
                    rater_id=rater_id,
                    research_experience_years=3,
                    seed_id=assignment.seed_id,
                    output_id=assignment.output_id,
                    retrieval=fixture.retrieval,
                    evidence=fixture.evidence,
                    lineage=fixture.lineage,
                    idea=fixture.idea,
                    calibration=fixture.calibration,
                    notes="locked fixture response",
                )
            )
        pairs = validate_jsonl(
            rater_root / "pairwise-assignments.jsonl", BlindPairwiseAssignment
        )
        for assignment in pairs:
            pairwise_responses.append(
                BlindPairwiseResponse(
                    assignment_id=assignment.assignment_id,
                    rater_id=rater_id,
                    research_experience_years=3,
                    seed_id=assignment.seed_id,
                    output_left=assignment.output_left,
                    output_right=assignment.output_right,
                    preference="tie",
                    rationale="The fixture outputs are equivalent.",
                )
            )
    scalar_path = tmp_path / "blind-scalar-responses.jsonl"
    pairwise_path = tmp_path / "blind-pairwise-responses.jsonl"
    write_jsonl(scalar_responses, scalar_path)
    write_jsonl(pairwise_responses, pairwise_path)
    key_path = blind_dir / "coordinator" / "blind-key.jsonl"
    blind_manifest = blind_dir / "coordinator" / "manifest.json"
    judgments_path = tmp_path / "judgments.jsonl"
    pairwise_judgments_path = tmp_path / "pairwise-judgments.jsonl"

    assert main(
        [
            "benchmark",
            "unblind",
            str(scalar_path),
            "--blind-pairwise",
            str(pairwise_path),
            "--blind-key",
            str(key_path),
            "--blind-manifest",
            str(blind_manifest),
            "--output",
            str(judgments_path),
            "--pairwise-output",
            str(pairwise_judgments_path),
        ]
    ) == 0
    public_results = tmp_path / "public-results.json"
    assert main(
        [
            "benchmark",
            "score",
            str(judgments_path),
            "--pairwise",
            str(pairwise_judgments_path),
            "--blind-scalar",
            str(scalar_path),
            "--blind-pairwise",
            str(pairwise_path),
            "--blind-key",
            str(key_path),
            "--blind-manifest",
            str(blind_manifest),
            "--benchmark-seeds",
            str(seed_path),
            "--run-matrix",
            str(matrix_path),
            "--execution-manifest",
            str(execution_manifest),
            "--results-root",
            str(tmp_path),
            "--output",
            str(public_results),
        ]
    ) == 0
    payload = json.loads(public_results.read_text(encoding="utf-8"))
    assert payload["publishable"] is True
    assert payload["human_judgments"] == 480
    assert payload["pairwise"]["human_judgments"] == 720
    assert set(payload["artifacts"]) == {
        "benchmark_seeds",
        "blind_key",
        "blind_manifest",
        "blind_pairwise_responses",
        "blind_scalar_responses",
        "execution_manifest",
        "pairwise_judgments",
        "run_matrix",
        "scalar_judgments",
    }
