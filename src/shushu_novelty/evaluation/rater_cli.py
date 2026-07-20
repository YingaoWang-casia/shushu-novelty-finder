"""Identity-neutral command used by human raters before unblinding."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from shushu_novelty.errors import EXIT_INVALID_INPUT, EXIT_OK, InputError
from shushu_novelty.evaluation.blinding import lock_rater_responses


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


if __name__ == "__main__":
    raise SystemExit(main())
