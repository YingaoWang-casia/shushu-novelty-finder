#!/usr/bin/env python3
"""Fail if release archives expose dynamic pre-unblinding evaluation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
import zipfile
from pathlib import Path

FORBIDDEN = (
    "/evals/results/",
    "/evals/execution/",
    "/evals/blind-",
    "/evals/completed-run-matrix.jsonl",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_archive(path: Path) -> dict[str, object]:
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            entry_points = "\n".join(
                archive.read(name).decode("utf-8")
                for name in names
                if name.endswith(".dist-info/entry_points.txt")
            )
    else:
        with tarfile.open(path) as archive:
            names = archive.getnames()
        entry_points = ""
    normalized = ["/" + name.lstrip("/") for name in names]
    leaked = [name for name in normalized if any(item in name for item in FORBIDDEN)]
    if leaked:
        raise SystemExit(f"forbidden dynamic evaluation artifacts in {path}: {leaked[:5]}")
    if not any(name.endswith(("/LICENSE", "/licenses/LICENSE")) for name in normalized):
        raise SystemExit(f"license is missing from {path}")
    if path.suffix == ".whl" and not {
        "blind-eval",
        "blind-eval-lock",
        "shushu",
        "shushu-codex-adapter",
    }.issubset(set(entry_points.split())):
        raise SystemExit(f"required console entry points are missing from {path}")
    return {
        "path": str(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "entries": len(names),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dist", type=Path)
    args = parser.parse_args()
    archives = sorted(
        [*args.dist.glob("*.whl"), *args.dist.glob("*.tar.gz")], key=lambda item: item.name
    )
    if len(archives) != 2:
        raise SystemExit(f"expected exactly one wheel and one sdist in {args.dist}")
    print(json.dumps([inspect_archive(path) for path in archives], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
