#!/usr/bin/env python3
"""Backward-compatible Paper Evidence Card renderer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shushu_novelty.io import load_jsonl  # noqa: E402
from shushu_novelty.normalization import to_markdown  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    markdown = to_markdown(load_jsonl(args.input))
    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
