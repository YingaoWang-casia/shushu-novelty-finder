#!/usr/bin/env python3
"""Backward-compatible structural report validator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shushu_novelty.evaluation.structural import validate_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--paper-mode", action="store_true")
    args = parser.parse_args()
    result = validate_report(args.report.read_text(encoding="utf-8"), args.paper_mode)
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
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
