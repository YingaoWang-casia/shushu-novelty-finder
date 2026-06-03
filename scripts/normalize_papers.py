#!/usr/bin/env python3
"""Normalize paper metadata into Paper Evidence Cards.

This script is intentionally lightweight. It does not search the web.
It converts a JSONL file of paper records into a Markdown evidence table.
"""

import argparse
import json
from pathlib import Path

FIELDS = [
    "title",
    "year",
    "venue_or_source",
    "paper_type",
    "url_or_identifier",
    "task",
    "dataset",
    "metric",
    "main_contribution",
    "why_relevant",
    "evidence_role",
    "confidence",
]


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at line {line_no}: {exc}") from exc


def normalize(record):
    return {field: str(record.get(field, "unknown")).replace("\n", " ") for field in FIELDS}


def to_markdown(records):
    lines = []
    lines.append("# Paper Evidence Cards")
    lines.append("")
    for idx, record in enumerate(records, 1):
        card = normalize(record)
        lines.append(f"## Paper {idx}: {card['title']}")
        lines.append("")
        for field in FIELDS:
            label = field.replace("_", " ").title()
            lines.append(f"- **{label}:** {card[field]}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Input JSONL file")
    parser.add_argument("--output", type=Path, default=None, help="Output Markdown file")
    args = parser.parse_args()

    records = list(load_jsonl(args.input))
    markdown = to_markdown(records)

    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
