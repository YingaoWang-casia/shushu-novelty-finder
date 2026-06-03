#!/usr/bin/env python3
"""Lightweight validator for shushu-novelty-finder reports.

Usage:
  python scripts/validate_report.py path/to/report.md

This validator does not judge scientific correctness. It checks whether a report
contains the minimum evidence and paper-readiness sections expected by the Skill.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_PATTERNS = {
    "mode": r"(?i)\b(mode|input mode)\b",
    "scope": r"(?i)\b(research scope card|scope card|scope)\b",
    "papers": r"(?i)\b(representative papers|paper evidence|literature timeline|papers)\b",
    "trend": r"(?i)\b(trend matrix|timeline|trend)\b",
    "gap": r"(?i)\b(gap audit|gap type|research gap|gap)\b",
    "novelty": r"(?i)\b(weak|medium|strong)\b.*\b(novelty|idea|candidate)\b",
    "risk": r"(?i)\b(risk|failure|threat)\b",
    "experiment": r"(?i)\b(minimum experiment|experiment card|baseline|ablation)\b",
}

PAPER_MODE_PATTERNS = {
    "paper_thesis": r"(?i)\b(paper thesis|core claim|working title)\b",
    "baseline": r"(?i)\b(baseline|ablation)\b",
    "readiness": r"(?i)\b(paper-readiness|readiness verdict|workshop-ready|main-track|pilot-ready)\b",
}

BAD_PATTERNS = {
    "unsupported_no_one": r"(?i)(no one has|nobody has|has not been studied|never been explored)",
    "vague_novel": r"(?i)\b(novel framework|novel method)\b",
}


def check_patterns(text: str, patterns: dict[str, str]) -> list[str]:
    missing = []
    for name, pattern in patterns.items():
        if not re.search(pattern, text, flags=re.DOTALL):
            missing.append(name)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--paper-mode", action="store_true", help="also require paper-readiness sections")
    args = parser.parse_args()

    text = args.report.read_text(encoding="utf-8")
    missing = check_patterns(text, REQUIRED_PATTERNS)
    if args.paper_mode:
        missing.extend(check_patterns(text, PAPER_MODE_PATTERNS))

    warnings = []
    for name, pattern in BAD_PATTERNS.items():
        if re.search(pattern, text):
            warnings.append(name)

    if missing:
        print("Missing required sections:")
        for item in missing:
            print(f"- {item}")
    else:
        print("All required sections found.")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
