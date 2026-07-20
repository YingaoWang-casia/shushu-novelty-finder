"""Shared schema behavior."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    """Base model that rejects silent schema drift."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, validate_assignment=True)

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=2) + "\n", encoding="utf-8")

    @classmethod
    def write_json_schema(cls, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = cls.model_json_schema()
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
