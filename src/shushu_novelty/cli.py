"""Command-line interface for the deterministic runtime."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from shushu_novelty import __version__
from shushu_novelty.errors import (
    EXIT_GATE_FAILURE,
    EXIT_INVALID_INPUT,
    EXIT_OK,
    EXIT_RETRIEVAL_FAILURE,
    GateError,
    InputError,
    RetrievalError,
)
from shushu_novelty.evaluation.benchmark import (
    build_run_matrix,
    collect_run_outputs,
    merge_run_manifests,
    validate_benchmark_execution_manifest,
    validate_executed_run_manifest,
    validate_resume_matrix,
    validate_suite,
)
from shushu_novelty.evaluation.blinding import (
    DEFAULT_SHARED_SEEDS,
    RATING_DESIGNS,
    collect_locked_rater_responses,
    create_blind_packages,
    lock_rater_responses,
    unblind_responses,
    validate_unblinded_responses,
    verify_blind_package_manifest,
)
from shushu_novelty.evaluation.citation import validate_ledger
from shushu_novelty.evaluation.collision import validate_collision_batch
from shushu_novelty.evaluation.gap import validate_gaps
from shushu_novelty.evaluation.idea import validate_ideas
from shushu_novelty.evaluation.lineage import validate_lineage
from shushu_novelty.evaluation.metrics import aggregate_evaluation
from shushu_novelty.evaluation.release import check_release_claims
from shushu_novelty.evaluation.report import validate_final_report
from shushu_novelty.evaluation.retrieval_benchmark import run_retrieval_benchmark
from shushu_novelty.evaluation.reviewer import validate_reviewer_batch
from shushu_novelty.evaluation.runner import execute_run_matrix
from shushu_novelty.evaluation.structural import validate_report
from shushu_novelty.fulltext import build_fulltext_ledger
from shushu_novelty.io import load_jsonl, sha256_file, validate_jsonl, write_jsonl
from shushu_novelty.normalization import to_markdown
from shushu_novelty.orchestrator.navigator import next_action
from shushu_novelty.orchestrator.state import create_run
from shushu_novelty.retrieval.arxiv import as_legacy_records
from shushu_novelty.retrieval.multi import SOURCE_FUNCTIONS, search_sources
from shushu_novelty.retrieval.replay import create_search_manifest, replay_search
from shushu_novelty.schemas import (
    SCHEMA_MODELS,
    BenchmarkAdapterSet,
    BenchmarkRun,
    BenchmarkSeed,
    BlindOutputKey,
    BlindPairwiseResponse,
    BlindScalarResponse,
    ClaimEvidence,
    CollisionBatch,
    EvaluationJudgment,
    FullTextDocument,
    GapRecord,
    IdeaCandidate,
    LineageGraph,
    PairwiseJudgment,
    PaperRecord,
    ReportManifest,
    RetrievalBenchmarkTopic,
    ReviewerBatch,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shushu", description="Lineage-first novelty workflow")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("check", help="check runtime and schema availability")

    search = commands.add_parser("search", help="search a paper source")
    search.add_argument("query")
    search.add_argument(
        "--source",
        action="append",
        choices=[*SOURCE_FUNCTIONS, "all"],
        help="repeat for multiple sources; default is arxiv",
    )
    search.add_argument("--max-results", type=int, default=10)
    search.add_argument("--start", type=int, default=0)
    search.add_argument(
        "--sort-by", choices=["relevance", "lastUpdatedDate", "submittedDate"], default="relevance"
    )
    search.add_argument("--sort-order", choices=["ascending", "descending"], default="descending")
    search.add_argument("--output", type=Path)
    search.add_argument("--failure-log", type=Path)
    search.add_argument("--manifest", type=Path, help="portable replay manifest output")
    search.add_argument("--legacy", action="store_true", help="emit the v0.1 record format")

    replay = commands.add_parser("replay", help="verify and replay a retrieval manifest")
    replay.add_argument("manifest", type=Path)
    replay.add_argument("--output", type=Path)

    retrieval_benchmark = commands.add_parser(
        "retrieval-benchmark", help="run the fixed live connector benchmark"
    )
    retrieval_benchmark.add_argument("topics", type=Path)
    retrieval_benchmark.add_argument(
        "--source",
        action="append",
        choices=list(SOURCE_FUNCTIONS),
        help="repeat to select sources; default is all four",
    )
    retrieval_benchmark.add_argument("--max-results", type=int, default=5)
    retrieval_benchmark.add_argument("--output-dir", type=Path, required=True)
    retrieval_benchmark.add_argument("--report", type=Path, required=True)

    normalize = commands.add_parser("normalize", help="render legacy JSONL evidence cards")
    normalize.add_argument("input", type=Path)
    normalize.add_argument("--output", type=Path)

    validate = commands.add_parser("validate", help="validate a report or schema records")
    validate.add_argument("input", type=Path)
    validate.add_argument("--paper-mode", action="store_true")
    validate.add_argument("--schema", choices=sorted(SCHEMA_MODELS))

    run = commands.add_parser("run", help="create a resumable run directory")
    run.add_argument("topic")
    run.add_argument("--mode", choices=["lineage", "idea", "full"], default="full")
    run.add_argument("--runs-dir", type=Path, default=Path("runs"))
    run.add_argument("--model")
    run.add_argument("--prompt-version")

    next_parser = commands.add_parser("next", help="return the unique next phase for a run")
    next_parser.add_argument("--run", type=Path, required=True)

    fulltext = commands.add_parser(
        "fulltext", help="download and extract paper full text into a page-text ledger"
    )
    fulltext.add_argument("papers", type=Path, help="canonical PaperRecord JSONL")
    fulltext.add_argument("--cache-dir", type=Path, default=Path(".shushu/fulltext"))
    fulltext.add_argument("--output", type=Path, required=True)
    fulltext.add_argument("--failure-log", type=Path)
    fulltext.add_argument("--workers", type=int, default=4)

    ledger = commands.add_parser("ledger", help="cross-validate claims, papers, and full text")
    ledger.add_argument("claims", type=Path)
    ledger.add_argument("--papers", type=Path, required=True)
    ledger.add_argument("--fulltext", type=Path, required=True)

    lineage = commands.add_parser("lineage", help="validate lineage edges and saturation evidence")
    lineage.add_argument("graph", type=Path)
    lineage.add_argument("--papers", type=Path, required=True)
    lineage.add_argument("--claims", type=Path, required=True)

    gap = commands.add_parser("gap", help="cross-validate gap evidence")
    gap.add_argument("gaps", type=Path)
    gap.add_argument("--papers", type=Path, required=True)
    gap.add_argument("--claims", type=Path, required=True)

    idea = commands.add_parser("idea", help="cross-validate an idea portfolio")
    idea.add_argument("ideas", type=Path)
    idea.add_argument("--gaps", type=Path, required=True)
    idea.add_argument("--papers", type=Path, required=True)

    collision = commands.add_parser("collision", help="validate independent novelty audits")
    collision.add_argument("audits", type=Path)
    collision.add_argument("--ideas", type=Path, required=True)
    collision.add_argument("--papers", type=Path, required=True)
    collision.add_argument("--claims", type=Path, required=True)

    reviewer = commands.add_parser("reviewer", help="validate independent reviewer audits")
    reviewer.add_argument("audits", type=Path)
    reviewer.add_argument("--ideas", type=Path, required=True)
    reviewer.add_argument("--collisions", type=Path, required=True)
    reviewer.add_argument("--claims", type=Path, required=True)

    report = commands.add_parser("report", help="validate a final-report manifest")
    report.add_argument("manifest", type=Path)
    report.add_argument(
        "--run-dir",
        type=Path,
        help="run root; defaults to the manifest's grandparent directory",
    )

    release = commands.add_parser("release-check", help="gate README effectiveness claims")
    release.add_argument("--readme", type=Path, default=Path("README.md"))
    release.add_argument("--public-evaluation", type=Path)

    benchmark = commands.add_parser("benchmark", help="validate, plan, or score benchmarks")
    benchmark.add_argument(
        "action",
        choices=[
            "validate",
            "plan",
            "execute",
            "collect",
            "merge",
            "blind-pack",
            "collect-responses",
            "lock-responses",
            "unblind",
            "score",
        ],
    )
    benchmark.add_argument("input", type=Path)
    benchmark.add_argument("--systems", default="bare,self-reflection,shushu-v0.1,shushu-v0.2")
    benchmark.add_argument(
        "--benchmark-seeds",
        type=Path,
        help="required for a publishable score to verify full suite coverage",
    )
    benchmark.add_argument(
        "--pairwise",
        type=Path,
        help="blind pairwise judgments; required for a publishable score",
    )
    benchmark.add_argument(
        "--results-root",
        type=Path,
        default=Path("."),
        help="root used to resolve run output paths for collect",
    )
    benchmark.add_argument("--adapters", type=Path, help="command adapters for execute")
    benchmark.add_argument("--failure-log", type=Path, help="run failures for execute")
    benchmark.add_argument(
        "--run-matrix", type=Path, help="hash-complete 240-run matrix required for score"
    )
    benchmark.add_argument(
        "--execution-manifest",
        type=Path,
        help="completed runtime/provenance manifest required for score",
    )
    benchmark.add_argument(
        "--matrix", action="append", type=Path, help="additional checkpoint for merge"
    )
    benchmark.add_argument("--rater", action="append", help="blind-pack rater ID; repeat")
    benchmark.add_argument(
        "--rater-dir",
        action="append",
        type=Path,
        help="additional locked rater directory for collect-responses; repeat as needed",
    )
    benchmark.add_argument(
        "--rating-design",
        choices=RATING_DESIGNS,
        default="complete",
        help="blind-pack coverage design; balanced-overlap requires exactly two raters",
    )
    benchmark.add_argument(
        "--shared-seeds",
        type=int,
        default=DEFAULT_SHARED_SEEDS,
        help=f"shared seeds in balanced-overlap design (default: {DEFAULT_SHARED_SEEDS})",
    )
    benchmark.add_argument("--output-dir", type=Path, help="blind-pack destination")
    benchmark.add_argument("--blind-key", type=Path, help="coordinator key for unblind")
    benchmark.add_argument(
        "--blind-manifest", type=Path, help="hash manifest for blind key and rater pack"
    )
    benchmark.add_argument(
        "--blind-manifest-sha256",
        help="pre-rating coordinator-manifest commitment for lock-responses",
    )
    benchmark.add_argument(
        "--blind-scalar", type=Path, help="locked blind scalar responses for score"
    )
    benchmark.add_argument(
        "--blind-pairwise", type=Path, help="blind pairwise responses for unblind"
    )
    benchmark.add_argument(
        "--pairwise-output", type=Path, help="unblinded pairwise judgment output"
    )
    benchmark.add_argument("--output", type=Path)

    schema = commands.add_parser("schema", help="list or export versioned JSON Schemas")
    schema.add_argument("name", nargs="?", choices=sorted(SCHEMA_MODELS))
    schema.add_argument("--output", type=Path)
    return parser


def _command_check() -> int:
    payload = {
        "status": "ok",
        "version": __version__,
        "python": ".".join(map(str, sys.version_info[:3])),
        "schemas": sorted(SCHEMA_MODELS),
        "sources": sorted(SOURCE_FUNCTIONS),
        "credentials": {
            "openalex": bool(os.environ.get("OPENALEX_API_KEY")),
            "semantic_scholar": bool(os.environ.get("SEMANTICSCHOLAR_API_KEY")),
        },
    }
    print(json.dumps(payload, indent=2))
    return EXIT_OK


def _command_search(args: argparse.Namespace) -> int:
    if args.manifest and not args.output:
        raise InputError("--manifest requires --output")
    if args.manifest and args.legacy:
        raise InputError("replay manifests require canonical PaperRecord output, not --legacy")
    requested = args.source or ["arxiv"]
    sources = list(SOURCE_FUNCTIONS) if "all" in requested else list(dict.fromkeys(requested))
    failure_log = args.failure_log
    if failure_log is None and args.output:
        failure_log = args.output.with_suffix(args.output.suffix + ".failures.jsonl")
    records, failures = search_sources(
        args.query,
        sources,
        args.max_results,
        failure_log,
        arxiv_start=args.start,
        arxiv_sort_by=args.sort_by,
        arxiv_sort_order=args.sort_order,
    )
    if failures and failure_log is None:
        for failure in failures:
            print(
                f"warning: {failure['source']} retrieval failed: {failure['error']}",
                file=sys.stderr,
            )
    if args.legacy:
        lines = (json.dumps(item, ensure_ascii=False) for item in as_legacy_records(records))
        text = "\n".join(lines) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    else:
        text = write_jsonl(records, args.output)
        if not args.output:
            print(text, end="")
        else:
            manifest_path = args.manifest or args.output.with_suffix(
                args.output.suffix + ".manifest.json"
            )
            if failure_log is None:
                raise AssertionError("file output must have a failure log")
            create_search_manifest(
                args.query,
                sources,
                args.max_results,
                args.output,
                failure_log,
                manifest_path,
                records,
                failures,
                args.start,
                args.sort_by,
                args.sort_order,
            )
            print(f"Replay manifest: {manifest_path}", file=sys.stderr)
    return EXIT_OK


def _command_replay(args: argparse.Namespace) -> int:
    manifest, records, failures = replay_search(args.manifest)
    text = write_jsonl(records, args.output)
    if not args.output:
        print(text, end="")
    print(
        f"Replayed {len(records)} records and verified {len(failures)} failures "
        f"for {manifest.query!r}",
        file=sys.stderr,
    )
    return EXIT_OK


def _command_retrieval_benchmark(args: argparse.Namespace) -> int:
    topics = validate_jsonl(args.topics, RetrievalBenchmarkTopic)
    sources = args.source or list(SOURCE_FUNCTIONS)
    report = run_retrieval_benchmark(
        topics, sources, args.max_results, args.output_dir
    )
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    return EXIT_OK if report.get("publishable") is True else EXIT_GATE_FAILURE


def _command_normalize(args: argparse.Namespace) -> int:
    markdown = to_markdown(load_jsonl(args.input))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return EXIT_OK


def _command_validate(args: argparse.Namespace) -> int:
    if args.schema:
        records = validate_jsonl(args.input, SCHEMA_MODELS[args.schema])
        print(f"Valid {args.schema} records: {len(records)}")
        return EXIT_OK
    result = validate_report(args.input.read_text(encoding="utf-8"), args.paper_mode)
    if result.missing:
        print("Missing required sections:")
        for item in result.missing:
            print(f"- {item}")
    else:
        print("All required sections found.")
    if result.warnings:
        print("\nWarnings:")
        for item in result.warnings:
            print(f"- {item}")
    return EXIT_OK if result.ok else EXIT_GATE_FAILURE


def _command_schema(args: argparse.Namespace) -> int:
    if not args.name:
        print("\n".join(sorted(SCHEMA_MODELS)))
        return EXIT_OK
    payload = SCHEMA_MODELS[args.name].model_json_schema()
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return EXIT_OK


def _command_fulltext(args: argparse.Namespace) -> int:
    papers = validate_jsonl(args.papers, PaperRecord)
    failure_log = args.failure_log or args.output.with_suffix(
        args.output.suffix + ".failures.jsonl"
    )
    documents, failures = build_fulltext_ledger(
        papers,
        args.cache_dir,
        failure_log,
        workers=args.workers,
        checkpoint_path=args.output,
    )
    print(
        json.dumps(
            {
                "documents": len(documents),
                "failures": len(failures),
                "output": str(args.output),
                "failure_log": str(failure_log),
            },
            ensure_ascii=False,
        )
    )
    return EXIT_OK


def _command_ledger(args: argparse.Namespace) -> int:
    claims = validate_jsonl(args.claims, ClaimEvidence)
    papers = validate_jsonl(args.papers, PaperRecord)
    documents = validate_jsonl(args.fulltext, FullTextDocument)
    result = validate_ledger(papers, documents, claims)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print(f"Valid claim-evidence records: {len(claims)}")
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_lineage(args: argparse.Namespace) -> int:
    graph = LineageGraph.model_validate(json.loads(args.graph.read_text(encoding="utf-8")))
    papers = validate_jsonl(args.papers, PaperRecord)
    claims = validate_jsonl(args.claims, ClaimEvidence)
    result = validate_lineage(graph, papers, claims)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print(
            f"Valid lineage graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges, "
            f"{len(graph.saturation)} saturation records"
        )
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_collision(args: argparse.Namespace) -> int:
    batch = CollisionBatch.model_validate(json.loads(args.audits.read_text(encoding="utf-8")))
    ideas = validate_jsonl(args.ideas, IdeaCandidate)
    papers = validate_jsonl(args.papers, PaperRecord)
    claims = validate_jsonl(args.claims, ClaimEvidence)
    result = validate_collision_batch(batch, ideas, papers, claims)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print(f"Valid collision audits: {len(batch.audits)}")
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_gap(args: argparse.Namespace) -> int:
    gaps = validate_jsonl(args.gaps, GapRecord)
    papers = validate_jsonl(args.papers, PaperRecord)
    claims = validate_jsonl(args.claims, ClaimEvidence)
    result = validate_gaps(gaps, papers, claims)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print(f"Valid evidence-backed gaps: {len(gaps)}")
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_idea(args: argparse.Namespace) -> int:
    ideas = validate_jsonl(args.ideas, IdeaCandidate)
    gaps = validate_jsonl(args.gaps, GapRecord)
    papers = validate_jsonl(args.papers, PaperRecord)
    result = validate_ideas(ideas, gaps, papers)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print(f"Valid idea portfolio: {len(ideas)}")
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_reviewer(args: argparse.Namespace) -> int:
    batch = ReviewerBatch.model_validate(json.loads(args.audits.read_text(encoding="utf-8")))
    ideas = validate_jsonl(args.ideas, IdeaCandidate)
    collisions = CollisionBatch.model_validate(
        json.loads(args.collisions.read_text(encoding="utf-8"))
    )
    claims = validate_jsonl(args.claims, ClaimEvidence)
    result = validate_reviewer_batch(batch, ideas, collisions, claims)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print(f"Valid reviewer audits: {len(batch.audits)}")
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_report(args: argparse.Namespace) -> int:
    manifest = ReportManifest.model_validate(
        json.loads(args.manifest.read_text(encoding="utf-8"))
    )
    run_dir = args.run_dir or args.manifest.parent.parent
    result = validate_final_report(manifest, run_dir)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print(f"Valid final report: {manifest.report_path}")
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_release_check(args: argparse.Namespace) -> int:
    result = check_release_claims(args.readme, args.public_evaluation)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    if result.ok:
        print("README effectiveness claims satisfy the release gate")
        return EXIT_OK
    return EXIT_GATE_FAILURE


def _command_benchmark(args: argparse.Namespace) -> int:
    if args.action == "execute":
        if not args.benchmark_seeds or not args.adapters or not args.output:
            raise InputError(
                "benchmark execute requires --benchmark-seeds, --adapters, and --output"
            )
        planned_runs = validate_jsonl(args.input, BenchmarkRun)
        runs = planned_runs
        if args.output.is_file():
            checkpointed = validate_jsonl(args.output, BenchmarkRun)
            resume_errors = validate_resume_matrix(planned_runs, checkpointed)
            if resume_errors:
                raise InputError("cannot resume benchmark: " + "; ".join(resume_errors))
            runs = checkpointed
        seeds = validate_jsonl(args.benchmark_seeds, BenchmarkSeed)
        validation = validate_suite(seeds)
        if not validation.ok:
            for error in validation.errors:
                print(f"error: {error}", file=sys.stderr)
            return EXIT_GATE_FAILURE
        adapters = BenchmarkAdapterSet.model_validate(
            json.loads(args.adapters.read_text(encoding="utf-8"))
        )
        failure_log = args.failure_log or args.output.with_suffix(
            args.output.suffix + ".failures.jsonl"
        )
        execution = execute_run_matrix(
            runs,
            seeds,
            adapters,
            args.results_root,
            failure_log,
            checkpoint_path=args.output,
        )
        write_jsonl(execution.runs, args.output)
        complete_count = sum(run.status == "complete" for run in execution.runs)
        failed_count = sum(run.status == "failed" for run in execution.runs)
        pending_count = sum(run.status == "pending" for run in execution.runs)
        print(
            f"Executed benchmark runs: {complete_count} complete, "
            f"{failed_count} failed, {pending_count} pending"
        )
        return EXIT_OK if execution.ok else EXIT_GATE_FAILURE

    if args.action == "collect":
        runs = validate_jsonl(args.input, BenchmarkRun)
        collection = collect_run_outputs(runs, args.results_root)
        for error in collection.errors:
            print(f"error: {error}", file=sys.stderr)
        if collection.errors:
            return EXIT_GATE_FAILURE
        if not args.output:
            raise InputError("benchmark collect requires --output for the hashed run manifest")
        write_jsonl(collection.runs, args.output)
        print(f"Collected benchmark outputs: {len(collection.runs)}")
        return EXIT_OK

    if args.action == "merge":
        if not args.output:
            raise InputError("benchmark merge requires --output")
        paths = [args.input, *(args.matrix or [])]
        manifests = [validate_jsonl(path, BenchmarkRun) for path in paths]
        merged = merge_run_manifests(manifests)
        merged.errors.extend(validate_executed_run_manifest(merged.runs, args.results_root))
        if merged.errors:
            for error in merged.errors:
                print(f"error: {error}", file=sys.stderr)
            return EXIT_GATE_FAILURE
        write_jsonl(merged.runs, args.output)
        print(f"Merged benchmark outputs: {len(merged.runs)}")
        return EXIT_OK

    if args.action == "blind-pack":
        if not args.output_dir or not args.rater or not args.benchmark_seeds:
            raise InputError(
                "benchmark blind-pack requires --benchmark-seeds, --output-dir, "
                "and repeated --rater"
            )
        runs = validate_jsonl(args.input, BenchmarkRun)
        seeds = validate_jsonl(args.benchmark_seeds, BenchmarkSeed)
        result = create_blind_packages(
            runs,
            seeds,
            args.results_root,
            args.output_dir,
            args.rater,
            rating_design=args.rating_design,
            shared_seed_count=args.shared_seeds,
        )
        print(
            json.dumps(
                {
                    "scalar_assignments": result.scalar_assignments,
                    "pairwise_assignments": result.pairwise_assignments,
                    "key_records": result.key_records,
                    "rating_design": result.rating_design,
                    "shared_seed_count": result.shared_seed_count,
                    "rater_seed_counts": result.rater_seed_counts,
                },
                indent=2,
            )
        )
        return EXIT_OK

    if args.action == "collect-responses":
        if (
            not args.rater_dir
            or not args.blind_manifest_sha256
            or not args.blind_manifest
            or not args.blind_key
            or not args.output
            or not args.pairwise_output
        ):
            raise InputError(
                "benchmark collect-responses requires an input rater directory, repeated "
                "--rater-dir, --blind-manifest-sha256, --blind-manifest, --blind-key, "
                "--output, and --pairwise-output"
            )
        verify_blind_package_manifest(args.blind_key, args.blind_manifest)
        if sha256_file(args.blind_manifest) != args.blind_manifest_sha256:
            raise InputError("blind manifest file does not match its pre-rating commitment")
        expected_rater_root = args.blind_manifest.resolve().parent.parent / "raters"
        rater_dirs = [args.input, *args.rater_dir]
        if any(path.resolve().parent != expected_rater_root for path in rater_dirs):
            raise InputError("collect-responses rater directories must belong to the blind package")
        scalar, pairwise = collect_locked_rater_responses(
            rater_dirs, args.blind_manifest_sha256
        )
        write_jsonl(scalar, args.output)
        write_jsonl(pairwise, args.pairwise_output)
        print(
            json.dumps(
                {
                    "raters": sorted({item.rater_id for item in scalar}),
                    "scalar_responses": len(scalar),
                    "pairwise_responses": len(pairwise),
                    "scalar_output": str(args.output),
                    "pairwise_output": str(args.pairwise_output),
                },
                indent=2,
            )
        )
        return EXIT_OK

    if args.action == "lock-responses":
        if (
            not args.blind_scalar
            or not args.blind_pairwise
            or not args.blind_manifest_sha256
            or not args.output
        ):
            raise InputError(
                "benchmark lock-responses requires --blind-scalar, --blind-pairwise, "
                "--blind-manifest-sha256, and --output"
            )
        lock = lock_rater_responses(
            args.input,
            args.blind_scalar,
            args.blind_pairwise,
            args.blind_manifest_sha256,
            args.output,
        )
        print(
            json.dumps(
                {
                    "rater_id": lock.rater_id,
                    "scalar_responses": lock.scalar_responses,
                    "pairwise_responses": lock.pairwise_responses,
                    "scalar_responses_sha256": lock.scalar_responses_sha256,
                    "pairwise_responses_sha256": lock.pairwise_responses_sha256,
                    "lock_path": str(args.output),
                },
                indent=2,
            )
        )
        return EXIT_OK

    if args.action == "unblind":
        if (
            not args.blind_pairwise
            or not args.blind_key
            or not args.blind_manifest
            or not args.output
        ):
            raise InputError(
                "benchmark unblind requires --blind-pairwise, --blind-key, "
                "--blind-manifest, --output, and --pairwise-output"
            )
        if not args.pairwise_output:
            raise InputError(
                "benchmark unblind requires --blind-pairwise, --blind-key, "
                "--blind-manifest, --output, and --pairwise-output"
            )
        verify_blind_package_manifest(args.blind_key, args.blind_manifest)
        scalar = validate_jsonl(args.input, BlindScalarResponse)
        pairwise = validate_jsonl(args.blind_pairwise, BlindPairwiseResponse)
        keys = validate_jsonl(args.blind_key, BlindOutputKey)
        judgments, pairwise_judgments = unblind_responses(scalar, pairwise, keys)
        write_jsonl(judgments, args.output)
        write_jsonl(pairwise_judgments, args.pairwise_output)
        print(
            f"Unblinded {len(judgments)} scalar and "
            f"{len(pairwise_judgments)} pairwise judgments"
        )
        return EXIT_OK

    if args.action == "score":
        judgments = validate_jsonl(args.input, EvaluationJudgment)
        pairwise_judgments = []
        blind_scalar_responses = []
        blind_pairwise_responses = []
        blind_keys = []
        runs = []
        seed_ids = None
        preflight_errors = []
        artifact_paths = {"scalar_judgments": args.input}
        completed_run_count = 0
        if args.run_matrix:
            runs = validate_jsonl(args.run_matrix, BenchmarkRun)
            manifest_errors = validate_executed_run_manifest(runs, args.results_root)
            preflight_errors.extend(manifest_errors)
            completed_run_count = len(runs) if not manifest_errors else 0
            artifact_paths["run_matrix"] = args.run_matrix
        else:
            preflight_errors.append(
                "--run-matrix is required to bind scores to 240 hash-complete outputs"
            )
        if args.pairwise:
            pairwise_judgments = validate_jsonl(args.pairwise, PairwiseJudgment)
            artifact_paths["pairwise_judgments"] = args.pairwise
        else:
            preflight_errors.append(
                "--pairwise is required for publishable blind pairwise evaluation"
            )
        if args.benchmark_seeds:
            seeds = validate_jsonl(args.benchmark_seeds, BenchmarkSeed)
            validation = validate_suite(seeds)
            preflight_errors.extend(validation.errors)
            seed_ids = [seed.seed_id for seed in seeds]
            artifact_paths["benchmark_seeds"] = args.benchmark_seeds
        else:
            preflight_errors.append(
                "--benchmark-seeds is required to verify publishable 60-seed coverage"
            )
        if args.execution_manifest:
            if args.run_matrix and args.benchmark_seeds:
                preflight_errors.extend(
                    validate_benchmark_execution_manifest(
                        args.execution_manifest,
                        runs,
                        args.benchmark_seeds,
                        args.run_matrix,
                    )
                )
            if args.execution_manifest.is_file():
                artifact_paths["execution_manifest"] = args.execution_manifest
            else:
                preflight_errors.append(
                    f"benchmark execution manifest does not exist: {args.execution_manifest}"
                )
        else:
            preflight_errors.append(
                "--execution-manifest is required to bind scores to runtime provenance"
            )
        if args.blind_scalar:
            blind_scalar_responses = validate_jsonl(args.blind_scalar, BlindScalarResponse)
            artifact_paths["blind_scalar_responses"] = args.blind_scalar
        else:
            preflight_errors.append(
                "--blind-scalar is required to bind scores to locked blind responses"
            )
        if args.blind_pairwise:
            blind_pairwise_responses = validate_jsonl(
                args.blind_pairwise, BlindPairwiseResponse
            )
            artifact_paths["blind_pairwise_responses"] = args.blind_pairwise
        else:
            preflight_errors.append(
                "--blind-pairwise is required to bind scores to locked blind responses"
            )
        if args.blind_key:
            blind_keys = validate_jsonl(args.blind_key, BlindOutputKey)
            artifact_paths["blind_key"] = args.blind_key
        else:
            preflight_errors.append("--blind-key is required to verify the identity mapping")
        if args.blind_manifest:
            if args.blind_key:
                try:
                    verify_blind_package_manifest(args.blind_key, args.blind_manifest)
                except InputError as exc:
                    preflight_errors.append(str(exc))
            if args.blind_manifest.is_file():
                artifact_paths["blind_manifest"] = args.blind_manifest
            else:
                preflight_errors.append(
                    f"blind-package manifest does not exist: {args.blind_manifest}"
                )
        else:
            preflight_errors.append(
                "--blind-manifest is required to verify the locked identity mapping"
            )
        if (
            blind_scalar_responses
            and blind_pairwise_responses
            and blind_keys
            and judgments
            and pairwise_judgments
        ):
            preflight_errors.extend(
                validate_unblinded_responses(
                    blind_scalar_responses,
                    blind_pairwise_responses,
                    blind_keys,
                    judgments,
                    pairwise_judgments,
                )
            )
        aggregation = aggregate_evaluation(judgments, seed_ids, pairwise_judgments)
        errors = preflight_errors + aggregation.errors
        payload = {
            **aggregation.report,
            "publishable": not errors,
            "completed_run_count": completed_run_count,
            "artifacts": {
                name: {
                    "path": (
                        os.path.relpath(path.resolve(), args.output.parent.resolve())
                        if args.output
                        else str(path)
                    ),
                    "sha256": sha256_file(path),
                }
                for name, path in artifact_paths.items()
            },
            "errors": errors,
            "warnings": aggregation.warnings,
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return EXIT_OK if not errors else EXIT_GATE_FAILURE

    seeds = validate_jsonl(args.input, BenchmarkSeed)
    validation = validate_suite(seeds)
    if not validation.ok:
        for error in validation.errors:
            print(f"error: {error}", file=sys.stderr)
        return EXIT_GATE_FAILURE
    if args.action == "validate":
        print(
            json.dumps(
                {
                    "seeds": len(seeds),
                    "case_types": validation.counts,
                    "domains": validation.domains,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return EXIT_OK
    systems = [item.strip() for item in args.systems.split(",") if item.strip()]
    runs = build_run_matrix(seeds, systems)
    if args.output:
        write_jsonl(runs, args.output)
    else:
        print(write_jsonl(runs), end="")
    print(f"Planned benchmark runs: {len(runs)}", file=sys.stderr)
    return EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "check":
            return _command_check()
        if args.command == "search":
            return _command_search(args)
        if args.command == "replay":
            return _command_replay(args)
        if args.command == "retrieval-benchmark":
            return _command_retrieval_benchmark(args)
        if args.command == "normalize":
            return _command_normalize(args)
        if args.command == "validate":
            return _command_validate(args)
        if args.command == "run":
            run_dir = create_run(
                args.topic, args.mode, args.runs_dir, args.model, args.prompt_version
            )
            print(run_dir.resolve())
            return EXIT_OK
        if args.command == "next":
            action = next_action(args.run)
            print(json.dumps(action, indent=2, ensure_ascii=False))
            return EXIT_GATE_FAILURE if action["status"] == "failed" else EXIT_OK
        if args.command == "fulltext":
            return _command_fulltext(args)
        if args.command == "ledger":
            return _command_ledger(args)
        if args.command == "lineage":
            return _command_lineage(args)
        if args.command == "gap":
            return _command_gap(args)
        if args.command == "idea":
            return _command_idea(args)
        if args.command == "collision":
            return _command_collision(args)
        if args.command == "reviewer":
            return _command_reviewer(args)
        if args.command == "report":
            return _command_report(args)
        if args.command == "release-check":
            return _command_release_check(args)
        if args.command == "benchmark":
            return _command_benchmark(args)
        if args.command == "schema":
            return _command_schema(args)
    except RetrievalError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_RETRIEVAL_FAILURE
    except (InputError, ValidationError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_INVALID_INPUT
    except GateError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_GATE_FAILURE
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
