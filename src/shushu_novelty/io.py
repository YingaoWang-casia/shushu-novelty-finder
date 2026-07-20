"""Deterministic JSON and JSONL helpers."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel, ValidationError

from shushu_novelty.errors import InputError

ModelT = TypeVar("ModelT", bound=BaseModel)


def load_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InputError(f"file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InputError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InputError(f"expected a JSON object in {path}")
    return value


def load_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise InputError(f"file does not exist: {path}") from exc
    for line_no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InputError(f"invalid JSONL in {path} at line {line_no}: {exc}") from exc
        if not isinstance(value, dict):
            raise InputError(f"expected a JSON object in {path} at line {line_no}")
        yield value


def validate_jsonl(path: Path, model: Type[ModelT]) -> list[ModelT]:
    records: list[ModelT] = []
    for line_no, value in enumerate(load_jsonl(path), 1):
        try:
            records.append(model.model_validate(value))
        except ValidationError as exc:
            message = f"schema validation failed in {path} at line {line_no}: {exc}"
            raise InputError(message) from exc
    if not records:
        raise InputError(f"JSONL file contains no records: {path}")
    return records


def write_jsonl(records: Iterable[BaseModel], path: Path | None = None) -> str:
    text = "\n".join(record.model_dump_json() for record in records)
    if text:
        text += "\n"
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return text


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()
