#!/usr/bin/env python3
"""Backward-compatible arXiv search entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shushu_novelty.errors import RetrievalError  # noqa: E402
from shushu_novelty.io import write_jsonl  # noqa: E402
from shushu_novelty.retrieval.arxiv import as_legacy_records, search_arxiv  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Search arXiv and output JSONL paper records.")
    parser.add_argument("query")
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument(
        "--sort-by", default="relevance", choices=["relevance", "lastUpdatedDate", "submittedDate"]
    )
    parser.add_argument("--sort-order", default="descending", choices=["ascending", "descending"])
    parser.add_argument(
        "--canonical", action="store_true", help="emit v1 canonical PaperRecord JSONL"
    )
    args = parser.parse_args()
    try:
        records = search_arxiv(
            args.query, args.max_results, args.start, args.sort_by, args.sort_order
        )
    except RetrievalError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    if not records:
        print("arXiv returned zero results", file=sys.stderr)
        return 3
    if args.canonical:
        print(write_jsonl(records), end="")
    else:
        for record in as_legacy_records(records):
            print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
