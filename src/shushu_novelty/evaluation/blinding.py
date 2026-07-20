"""Create identity-free rater packs and join locked blind responses."""

from __future__ import annotations

import hashlib
import hmac
import itertools
import json
import re
import secrets
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from shushu_novelty.errors import InputError
from shushu_novelty.io import sha256_file, validate_jsonl, write_jsonl
from shushu_novelty.schemas import (
    BenchmarkRun,
    BenchmarkSeed,
    EvaluationJudgment,
    PairwiseJudgment,
)
from shushu_novelty.schemas.blind_evaluation import (
    BlindOutputAssignment,
    BlindOutputKey,
    BlindPairwiseAssignment,
    BlindPairwiseResponse,
    BlindResponseLock,
    BlindScalarResponse,
)

PRIMARY_SYSTEMS = ("bare", "self-reflection", "shushu-v0.1", "shushu-v0.2")
SAFE_RATER = re.compile(r"^[A-Za-z0-9._-]+$")
IDENTITY_PATTERNS = (
    ("shushu", re.compile(r"\bshushu(?:-v0\.[12])?\b", re.IGNORECASE)),
    (
        "self-reflection system/profile",
        re.compile(
            r"\bself[- ]reflection\s+(?:system|profile|baseline|variant|configuration)\b"
            r"|\b(?:system|profile|baseline|variant|configuration)\s+(?:is\s+)?"
            r"self[- ]reflection\b",
            re.IGNORECASE,
        ),
    ),
    ("benchmark profile", re.compile(r"\bbenchmark profile\b", re.IGNORECASE)),
    (
        "v0.2 engineering protocol",
        re.compile(r"\bv0\.2 engineering protocol\b", re.IGNORECASE),
    ),
)

RATER_GUIDE = """# Blind evaluation guide

You are rating four anonymous research-audit outputs for each of 60 fixed seeds. Do not attempt to
infer the producing system, contact another rater, or inspect the coordinator directory. Work from
the supplied seed, output, and independently verified literature evidence. Record uncertainty in
`notes`; do not silently convert an unknown into a zero or a correct judgment.

## Files and required coverage

- `benchmark-seeds.jsonl`: the 60 source requests and curated case metadata.
- `scalar-assignments.jsonl`: 240 output assignments; submit exactly one scalar response per row.
- `pairwise-assignments.jsonl`: 360 randomized comparisons; submit exactly one pairwise response
  per row.
- `outputs/`: immutable answer files. Verify their SHA-256 against the assignment before rating.
- `schemas/`: JSON Schemas for the two response files and the generated response lock.

Keep assignment IDs, rater ID, seed ID, and opaque output IDs unchanged. Report your actual years
of research experience. Before rating, obtain and record the coordinator's SHA-256 commitment for
`coordinator/manifest.json`; the key content remains withheld. Validate the completed JSONL before
sending it to the coordinator.

## Scalar counting rules

Use non-negative integer counts. A denominator of zero means the output contains no assessable
item in that category, not that verification was skipped.

- Retrieval: `known_prior_total` comes from the curated seed; count how many are retrieved within
  the output's main evidence set. Count unique paper records after accepted/preprint merging.
  Metadata uses five fields per record: title, authors, year, venue/publication status, and a
  persistent identifier or source link. Verify claimed publication labels externally.
- Evidence: count atomic factual or novelty claims, not paragraphs. A citation exists only after
  resolving it to a real paper. Entailment requires the cited source to support the claim as
  stated. A strong claim is an unqualified conclusion that materially supports the recommendation;
  mark it full-text verified only when the answer provides or you confirm body-text support.
- Lineage: independently verify proposed edges. For every required relation type, true positives
  are supported edges, false positives are proposed but unsupported edges, and false negatives are
  material verified edges omitted by the answer. Evaluate closest-prior recall at five and
  saturation claims against the same verified reference set. Explain unresolved gold/reference
  ambiguity in `notes`.
- Calibration: compare the answer's novelty/confidence/kill decision with the curated case and your
  verified prior-art judgment. `kill_correct` evaluates a recommended kill; when no kill is
  recommended, set it to false and explain borderline cases in `notes`.

## Idea-quality anchors

Score each dimension from 1 to 5: 1 = absent or seriously defective, 3 = concrete but incomplete,
5 = unusually strong and reviewer-defensible. Apply the same threshold to every anonymous output.
The novelty verdict is `weak`, `medium`, or `strong` after prior-art verification, not the label the
answer gives itself.

## Pairwise decisions

Choose `left` or `right` for the more evidence-grounded, specific, feasible, falsifiable, and
reviewer-defensible output. Choose `tie` only when the difference is not decision-relevant. The
rationale must identify concrete evidence or methodological differences; style alone is
insufficient.

## Locking

Name the completed files `blind-scalar-responses.jsonl` and
`blind-pairwise-responses.jsonl`. Before sending them to the coordinator, run:

```bash
blind-eval-lock . \
  --scalar blind-scalar-responses.jsonl \
  --pairwise blind-pairwise-responses.jsonl \
  --manifest-sha256 <coordinator-manifest-commitment> \
  --output response-lock.json
```

This verifies exact 240/360 coverage, immutable assignment fields, copied-output hashes, and one
consistent experience value, then records both response SHA-256 values. Treat the response files
and `response-lock.json` as locked. Do not edit them after the coordinator reveals any identity
mapping.
"""


@dataclass(frozen=True)
class BlindPackageResult:
    scalar_assignments: int
    pairwise_assignments: int
    key_records: int


def _opaque_id(secret: bytes, *parts: str) -> str:
    message = "\0".join(parts).encode()
    return "O-" + hmac.new(secret, message, hashlib.sha256).hexdigest()[:16]


def _rater_materials() -> dict[str, str]:
    return {
        "README.md": RATER_GUIDE,
        "schemas/blind-scalar-response.schema.json": json.dumps(
            BlindScalarResponse.model_json_schema(), indent=2, sort_keys=True
        )
        + "\n",
        "schemas/blind-pairwise-response.schema.json": json.dumps(
            BlindPairwiseResponse.model_json_schema(), indent=2, sort_keys=True
        )
        + "\n",
        "schemas/blind-response-lock.schema.json": json.dumps(
            BlindResponseLock.model_json_schema(), indent=2, sort_keys=True
        )
        + "\n",
    }


def _unique_by_id(items: list[object], field: str, label: str) -> dict[str, object]:
    indexed = {str(getattr(item, field)): item for item in items}
    if len(indexed) != len(items):
        raise InputError(f"{label} contains duplicate {field} values")
    return indexed


def lock_rater_responses(
    rater_dir: Path,
    scalar_response_path: Path,
    pairwise_response_path: Path,
    blind_manifest_sha256: str,
    output_path: Path,
) -> BlindResponseLock:
    """Validate a complete rater submission and write its pre-unblinding lock."""
    if not re.fullmatch(r"[a-f0-9]{64}", blind_manifest_sha256):
        raise InputError("blind manifest commitment must be a lowercase SHA-256")
    root = rater_dir.resolve()
    if not root.is_dir():
        raise InputError(f"rater directory does not exist: {rater_dir}")
    scalar_path = scalar_response_path.resolve()
    pairwise_path = pairwise_response_path.resolve()
    for label, path in (("scalar", scalar_path), ("pairwise", pairwise_path)):
        if path.parent != root or not path.is_file():
            raise InputError(f"{label} response file must be a direct file in the rater directory")
    lock_path = output_path.resolve()
    if lock_path.parent != root:
        raise InputError("response lock output must be a direct file in the rater directory")
    if lock_path.exists():
        raise InputError(f"response lock already exists and is immutable: {output_path}")

    scalar_assignments = validate_jsonl(
        root / "scalar-assignments.jsonl", BlindOutputAssignment
    )
    pairwise_assignments = validate_jsonl(
        root / "pairwise-assignments.jsonl", BlindPairwiseAssignment
    )
    scalar_responses = validate_jsonl(scalar_path, BlindScalarResponse)
    pairwise_responses = validate_jsonl(pairwise_path, BlindPairwiseResponse)
    if len(scalar_assignments) != 240 or len(scalar_responses) != 240:
        raise InputError("response lock requires exactly 240 scalar assignments and responses")
    if len(pairwise_assignments) != 360 or len(pairwise_responses) != 360:
        raise InputError("response lock requires exactly 360 pairwise assignments and responses")

    scalar_by_id = _unique_by_id(scalar_assignments, "assignment_id", "scalar assignments")
    scalar_response_by_id = _unique_by_id(
        scalar_responses, "assignment_id", "scalar responses"
    )
    pairwise_by_id = _unique_by_id(
        pairwise_assignments, "assignment_id", "pairwise assignments"
    )
    pairwise_response_by_id = _unique_by_id(
        pairwise_responses, "assignment_id", "pairwise responses"
    )
    if set(scalar_by_id) != set(scalar_response_by_id):
        raise InputError("scalar responses do not exactly cover scalar assignments")
    if set(pairwise_by_id) != set(pairwise_response_by_id):
        raise InputError("pairwise responses do not exactly cover pairwise assignments")

    rater_ids = {item.rater_id for item in scalar_assignments + pairwise_assignments}
    if len(rater_ids) != 1:
        raise InputError("rater pack assignments must contain exactly one rater ID")
    rater_id = next(iter(rater_ids))
    if rater_id != root.name:
        raise InputError("rater directory name differs from assignment rater ID")

    output_by_key = {}
    for assignment in scalar_assignments:
        response = scalar_response_by_id[assignment.assignment_id]
        immutable = ("rater_id", "seed_id", "output_id")
        if any(getattr(response, field) != getattr(assignment, field) for field in immutable):
            raise InputError(
                f"scalar response changes immutable assignment fields: {assignment.assignment_id}"
            )
        portable = PurePosixPath(assignment.output_path)
        if portable.is_absolute() or ".." in portable.parts:
            raise InputError(f"scalar assignment output path is unsafe: {assignment.output_path}")
        output = (root / assignment.output_path).resolve()
        if root not in output.parents or not output.is_file():
            raise InputError(f"scalar assignment output is missing: {assignment.output_path}")
        if sha256_file(output) != assignment.output_sha256:
            raise InputError(f"scalar assignment output hash differs: {assignment.assignment_id}")
        key = (assignment.seed_id, assignment.output_id)
        if key in output_by_key:
            raise InputError("scalar assignments contain duplicate seed/output IDs")
        output_by_key[key] = assignment

    for assignment in pairwise_assignments:
        response = pairwise_response_by_id[assignment.assignment_id]
        immutable = ("rater_id", "seed_id", "output_left", "output_right")
        if any(getattr(response, field) != getattr(assignment, field) for field in immutable):
            raise InputError(
                f"pairwise response changes immutable assignment fields: {assignment.assignment_id}"
            )
        left = output_by_key.get((assignment.seed_id, assignment.output_left))
        right = output_by_key.get((assignment.seed_id, assignment.output_right))
        if left is None or right is None:
            raise InputError(
                "pairwise assignment references an unknown output: "
                f"{assignment.assignment_id}"
            )
        if (
            assignment.path_left != left.output_path
            or assignment.sha256_left != left.output_sha256
            or assignment.path_right != right.output_path
            or assignment.sha256_right != right.output_sha256
        ):
            raise InputError(
                f"pairwise assignment output binding differs: {assignment.assignment_id}"
            )

    experience = {
        item.research_experience_years
        for item in [*scalar_responses, *pairwise_responses]
    }
    response_raters = {item.rater_id for item in [*scalar_responses, *pairwise_responses]}
    if response_raters != {rater_id}:
        raise InputError("responses contain a different or mixed rater ID")
    if len(experience) != 1:
        raise InputError("all responses must report one consistent research-experience value")

    lock = BlindResponseLock(
        rater_id=rater_id,
        research_experience_years=next(iter(experience)),
        locked_at=datetime.now(timezone.utc).isoformat(),
        blind_manifest_sha256=blind_manifest_sha256,
        scalar_assignments_sha256=sha256_file(root / "scalar-assignments.jsonl"),
        pairwise_assignments_sha256=sha256_file(root / "pairwise-assignments.jsonl"),
        scalar_response_filename=scalar_path.name,
        scalar_responses=len(scalar_responses),
        scalar_responses_sha256=sha256_file(scalar_path),
        pairwise_response_filename=pairwise_path.name,
        pairwise_responses=len(pairwise_responses),
        pairwise_responses_sha256=sha256_file(pairwise_path),
    )
    temporary = lock_path.with_name(lock_path.name + ".tmp")
    lock.write_json(temporary)
    temporary.replace(lock_path)
    return lock


def verify_blind_package_manifest(
    blind_key: Path, manifest_path: Path
) -> dict[str, object]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InputError(f"cannot read blind-package manifest: {exc}") from exc
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "1.0":
        raise InputError("blind-package manifest must be a schema v1.0 object")
    if not blind_key.is_file():
        raise InputError(f"blind key does not exist: {blind_key}")
    expected = manifest.get("blind_key_sha256")
    if not isinstance(expected, str) or sha256_file(blind_key) != expected:
        raise InputError("blind key hash does not match the blind-package manifest")
    key_records = sum(
        bool(line.strip()) for line in blind_key.read_text(encoding="utf-8").splitlines()
    )
    if manifest.get("key_records") != key_records:
        raise InputError("blind key record count does not match the blind-package manifest")
    artifacts = manifest.get("rater_artifact_sha256")
    if not isinstance(artifacts, dict) or not artifacts:
        raise InputError("blind-package manifest has no rater artifact hashes")
    package_root = manifest_path.parent.parent.resolve()
    for relative, digest in sorted(artifacts.items()):
        if not isinstance(relative, str) or not isinstance(digest, str):
            raise InputError("blind-package rater artifact entries must be path/hash strings")
        portable = PurePosixPath(relative)
        if portable.is_absolute() or ".." in portable.parts:
            raise InputError(f"blind-package rater artifact path is unsafe: {relative}")
        candidate = (package_root / relative).resolve()
        if package_root not in candidate.parents or not candidate.is_file():
            raise InputError(f"blind-package rater artifact is missing or unsafe: {relative}")
        if sha256_file(candidate) != digest:
            raise InputError(f"blind-package rater artifact hash does not match: {relative}")
    return manifest


def _require_complete_matrix(
    runs: list[BenchmarkRun], seeds: list[BenchmarkSeed], root: Path
) -> dict[str, BenchmarkRun]:
    if len(runs) != 240:
        raise InputError(f"blind packaging requires 240 runs, found {len(runs)}")
    if len(seeds) != 60 or len({seed.seed_id for seed in seeds}) != 60:
        raise InputError("blind packaging requires 60 unique benchmark seeds")
    seed_by_id = {seed.seed_id: seed for seed in seeds}
    by_key = {(run.seed_id, run.system): run for run in runs}
    if len(by_key) != len(runs):
        raise InputError("blind packaging run matrix contains duplicate seed/system records")
    for seed_number in range(1, 61):
        seed_id = f"B-{seed_number:03d}"
        for system in PRIMARY_SYSTEMS:
            run = by_key.get((seed_id, system))
            if run is None:
                raise InputError(f"blind packaging is missing {seed_id}/{system}")
            expected_prompt_hash = hashlib.sha256(seed_by_id[seed_id].prompt.encode()).hexdigest()
            if run.prompt_hash != expected_prompt_hash:
                raise InputError(f"blind packaging prompt hash differs for {run.run_id}")
            path = (root / run.output_path).resolve()
            if root not in path.parents or not path.is_file():
                raise InputError(f"blind packaging output is missing or unsafe: {run.output_path}")
            digest = sha256_file(path)
            if run.status != "complete" or run.output_sha256 != digest:
                raise InputError(f"blind packaging output is not hash-complete: {run.run_id}")
            if not run.model or not run.adapter_sha256:
                raise InputError(
                    f"blind packaging output lacks model/adapter provenance: {run.run_id}"
                )
            output_text = path.read_text(encoding="utf-8")
            leaked = next(
                (label for label, pattern in IDENTITY_PATTERNS if pattern.search(output_text)),
                None,
            )
            if leaked:
                raise InputError(
                    f"blind packaging output leaks a system-identity marker in {run.run_id}: "
                    f"{leaked}"
                )
    return by_key


def create_blind_packages(
    runs: list[BenchmarkRun],
    seeds: list[BenchmarkSeed],
    results_root: Path,
    output_dir: Path,
    rater_ids: list[str],
    secret: bytes | None = None,
) -> BlindPackageResult:
    root = results_root.resolve()
    by_key = _require_complete_matrix(runs, seeds, root)
    if len(rater_ids) < 2 or len(rater_ids) != len(set(rater_ids)):
        raise InputError("blind packaging requires at least two unique rater IDs")
    if any(not SAFE_RATER.fullmatch(rater_id) for rater_id in rater_ids):
        raise InputError("rater IDs may contain only letters, numbers, dot, underscore, and dash")
    if output_dir.exists():
        raise InputError(f"blind package output already exists: {output_dir}")
    package_secret = secret or secrets.token_bytes(32)
    assignments = []
    pairs = []
    keys = []
    rater_materials = _rater_materials()
    for rater_id in sorted(rater_ids):
        rater_root = output_dir / "raters" / rater_id
        rater_assignments = []
        rater_pairs = []
        for seed_number in range(1, 61):
            seed_id = f"B-{seed_number:03d}"
            blinded: dict[str, BlindOutputAssignment] = {}
            for system in PRIMARY_SYSTEMS:
                run = by_key[(seed_id, system)]
                output_id = _opaque_id(package_secret, rater_id, seed_id, system)
                relative = f"outputs/{seed_id}/{output_id}.md"
                destination = rater_root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / run.output_path, destination)
                assignment = BlindOutputAssignment(
                    assignment_id=f"BA-{rater_id}:{seed_id}:{output_id}",
                    rater_id=rater_id,
                    seed_id=seed_id,
                    output_id=output_id,
                    output_path=relative,
                    output_sha256=run.output_sha256,
                )
                blinded[system] = assignment
                assignments.append(assignment)
                rater_assignments.append(assignment)
                keys.append(
                    BlindOutputKey(
                        rater_id=rater_id,
                        seed_id=seed_id,
                        output_id=output_id,
                        system=system,
                        source_output_path=run.output_path,
                        output_sha256=run.output_sha256,
                    )
                )
            for pair_index, (first, second) in enumerate(
                itertools.combinations(PRIMARY_SYSTEMS, 2), 1
            ):
                left, right = blinded[first], blinded[second]
                order = hmac.new(
                    package_secret,
                    f"order\0{rater_id}\0{seed_id}\0{first}\0{second}".encode(),
                    hashlib.sha256,
                ).digest()[0]
                if order % 2:
                    left, right = right, left
                pair = BlindPairwiseAssignment(
                    assignment_id=f"BPA-{rater_id}:{seed_id}:{pair_index}",
                    rater_id=rater_id,
                    seed_id=seed_id,
                    output_left=left.output_id,
                    output_right=right.output_id,
                    path_left=left.output_path,
                    path_right=right.output_path,
                    sha256_left=left.output_sha256,
                    sha256_right=right.output_sha256,
                )
                pairs.append(pair)
                rater_pairs.append(pair)
        write_jsonl(rater_assignments, rater_root / "scalar-assignments.jsonl")
        write_jsonl(rater_pairs, rater_root / "pairwise-assignments.jsonl")
        write_jsonl(seeds, rater_root / "benchmark-seeds.jsonl")
        for relative, content in rater_materials.items():
            destination = rater_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
    coordinator = output_dir / "coordinator"
    blind_key_path = coordinator / "blind-key.jsonl"
    write_jsonl(keys, blind_key_path)
    rater_artifact_sha256 = {}
    for rater_id in sorted(rater_ids):
        rater_root = output_dir / "raters" / rater_id
        for artifact in sorted(path for path in rater_root.rglob("*") if path.is_file()):
            relative = artifact.relative_to(output_dir).as_posix()
            rater_artifact_sha256[relative] = sha256_file(artifact)
    manifest = {
        "schema_version": "1.0",
        "raters": sorted(rater_ids),
        "scalar_assignments": len(assignments),
        "pairwise_assignments": len(pairs),
        "key_records": len(keys),
        "blind_key_sha256": sha256_file(blind_key_path),
        "run_matrix_sha256": hashlib.sha256(
            "".join(run.model_dump_json() + "\n" for run in runs).encode()
        ).hexdigest(),
        "benchmark_sha256": hashlib.sha256(
            "".join(seed.model_dump_json() + "\n" for seed in seeds).encode()
        ).hexdigest(),
        "rater_material_sha256": {
            relative: hashlib.sha256(content.encode()).hexdigest()
            for relative, content in sorted(rater_materials.items())
        },
        "rater_artifact_sha256": rater_artifact_sha256,
        "identity_markers_checked": [label for label, _ in IDENTITY_PATTERNS],
        "secret_sha256": hashlib.sha256(package_secret).hexdigest(),
    }
    coordinator.mkdir(parents=True, exist_ok=True)
    (coordinator / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return BlindPackageResult(len(assignments), len(pairs), len(keys))


def unblind_responses(
    scalar: list[BlindScalarResponse],
    pairwise: list[BlindPairwiseResponse],
    key_records: list[BlindOutputKey],
) -> tuple[list[EvaluationJudgment], list[PairwiseJudgment]]:
    keys = {
        (item.rater_id, item.seed_id, item.output_id): item.system for item in key_records
    }
    if len(keys) != len(key_records):
        raise InputError("blind key contains duplicate rater/seed/output mappings")
    judgments = []
    for item in scalar:
        system = keys.get((item.rater_id, item.seed_id, item.output_id))
        if system is None:
            raise InputError(f"no blind key mapping for scalar assignment {item.assignment_id}")
        judgments.append(
            EvaluationJudgment(
                judgment_id=f"J-{item.seed_id}-{system}-{item.rater_id}",
                seed_id=item.seed_id,
                system=system,
                rater_id=item.rater_id,
                rater_type="human",
                blind=True,
                research_experience_years=item.research_experience_years,
                retrieval=item.retrieval,
                evidence=item.evidence,
                lineage=item.lineage,
                idea=item.idea,
                calibration=item.calibration,
                notes=item.notes,
            )
        )
    pairwise_judgments = []
    for item in pairwise:
        left = keys.get((item.rater_id, item.seed_id, item.output_left))
        right = keys.get((item.rater_id, item.seed_id, item.output_right))
        if left is None or right is None:
            raise InputError(f"no blind key mapping for pair assignment {item.assignment_id}")
        pairwise_judgments.append(
            PairwiseJudgment(
                pairwise_id=f"PW-{item.seed_id}-{left}-{right}-{item.rater_id}",
                seed_id=item.seed_id,
                system_left=left,
                system_right=right,
                preference=item.preference,
                rater_id=item.rater_id,
                rater_type="human",
                blind=True,
                research_experience_years=item.research_experience_years,
                rationale=item.rationale,
            )
        )
    return judgments, pairwise_judgments


def validate_unblinded_responses(
    scalar: list[BlindScalarResponse],
    pairwise: list[BlindPairwiseResponse],
    key_records: list[BlindOutputKey],
    judgments: list[EvaluationJudgment],
    pairwise_judgments: list[PairwiseJudgment],
) -> list[str]:
    expected_scalar, expected_pairwise = unblind_responses(scalar, pairwise, key_records)
    errors = []

    def indexed(items: list[object], field: str) -> dict[str, object]:
        return {getattr(item, field): item.model_dump(mode="json") for item in items}

    expected_scalar_by_id = indexed(expected_scalar, "judgment_id")
    actual_scalar_by_id = indexed(judgments, "judgment_id")
    if len(expected_scalar_by_id) != len(expected_scalar) or len(actual_scalar_by_id) != len(
        judgments
    ):
        errors.append("scalar judgment IDs must be unique across blind and unblinded records")
    if expected_scalar_by_id != actual_scalar_by_id:
        errors.append("unblinded scalar judgments differ from the locked blind responses/key")

    expected_pairwise_by_id = indexed(expected_pairwise, "pairwise_id")
    actual_pairwise_by_id = indexed(pairwise_judgments, "pairwise_id")
    if len(expected_pairwise_by_id) != len(expected_pairwise) or len(
        actual_pairwise_by_id
    ) != len(pairwise_judgments):
        errors.append("pairwise judgment IDs must be unique across blind and unblinded records")
    if expected_pairwise_by_id != actual_pairwise_by_id:
        errors.append("unblinded pairwise judgments differ from the locked blind responses/key")
    return errors
