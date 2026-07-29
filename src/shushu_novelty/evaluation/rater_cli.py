"""Identity-neutral command used by human raters before unblinding."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from shushu_novelty.errors import EXIT_INVALID_INPUT, EXIT_OK, InputError
from shushu_novelty.evaluation.blinding import (
    initialize_rater_response_drafts,
    lock_rater_responses,
    rater_response_draft_status,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blind-eval-lock",
        description="validate and lock a complete anonymous human-rating submission",
    )
    parser.add_argument("rater_dir", type=Path)
    parser.add_argument("--scalar", type=Path, required=True)
    parser.add_argument("--pairwise", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def build_workflow_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blind-eval",
        description="prepare, inspect, and lock anonymous human-rating responses",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="create assignment-bound response drafts")
    init.add_argument("rater_dir", type=Path)
    init.add_argument("--experience-years", type=float, required=True)
    status = commands.add_parser("status", help="report response completion without editing files")
    status.add_argument("rater_dir", type=Path)
    lock = commands.add_parser("lock", help="validate and lock a complete response set")
    lock.add_argument("rater_dir", type=Path)
    lock.add_argument("--scalar", type=Path, required=True)
    lock.add_argument("--pairwise", type=Path, required=True)
    lock.add_argument("--manifest-sha256", required=True)
    lock.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        lock = lock_rater_responses(
            args.rater_dir,
            args.scalar,
            args.pairwise,
            args.manifest_sha256,
            args.output,
        )
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_INVALID_INPUT
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


def workflow_main(argv: Sequence[str] | None = None) -> int:
    args = build_workflow_parser().parse_args(argv)
    try:
        if args.command == "init":
            result = initialize_rater_response_drafts(
                args.rater_dir, args.experience_years
            )
            payload = {
                "rater_id": result.rater_id,
                "scalar_responses": result.scalar_responses,
                "pairwise_responses": result.pairwise_responses,
                "scalar_path": str(result.scalar_path),
                "pairwise_path": str(result.pairwise_path),
            }
        elif args.command == "status":
            payload = rater_response_draft_status(args.rater_dir)
        else:
            lock = lock_rater_responses(
                args.rater_dir,
                args.scalar,
                args.pairwise,
                args.manifest_sha256,
                args.output,
            )
            payload = {
                "rater_id": lock.rater_id,
                "scalar_responses": lock.scalar_responses,
                "pairwise_responses": lock.pairwise_responses,
                "scalar_responses_sha256": lock.scalar_responses_sha256,
                "pairwise_responses_sha256": lock.pairwise_responses_sha256,
                "lock_path": str(args.output),
            }
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_INVALID_INPUT
    print(json.dumps(payload, indent=2))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
