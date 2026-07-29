"""Run creation and state persistence."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError

from shushu_novelty.errors import InputError
from shushu_novelty.io import load_json
from shushu_novelty.orchestrator.phases import phases_for_mode
from shushu_novelty.schemas import PhaseRecord, RunState
from shushu_novelty.schemas.run_state import utc_now

RUN_SUBDIRECTORIES = [
    "intake",
    "retrieval",
    "papers",
    "lineage",
    "gaps",
    "ideas",
    "collision",
    "audit",
    "report",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug[:60] or "topic"


def create_run(
    topic: str,
    mode: str,
    runs_root: Path,
    model: str | None = None,
    prompt_version: str | None = None,
) -> Path:
    if mode not in {"lineage", "idea", "full"}:
        raise InputError(f"unsupported run mode: {mode}")
    topic = topic.strip()
    if not topic:
        raise InputError("topic must not be empty")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{slugify(topic)}-{stamp}-{uuid4().hex[:8]}"
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    for child in RUN_SUBDIRECTORIES:
        (run_dir / child).mkdir()

    phases = {phase.code: PhaseRecord(artifact=phase.artifact) for phase in phases_for_mode(mode)}
    state = RunState(
        run_id=run_id,
        topic=topic,
        topic_slug=slugify(topic),
        mode=mode,
        model=model,
        prompt_version=prompt_version,
        phases=phases,
    )
    state.write_json(run_dir / "run.json")
    intake = {
        "schema_version": "1.0",
        "topic": topic,
        "mode": mode,
        "created_at": state.created_at,
    }
    (run_dir / "intake" / "intake.json").write_text(
        json.dumps(intake, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return run_dir


def load_state(run_dir: Path) -> RunState:
    try:
        return RunState.model_validate(load_json(run_dir / "run.json"))
    except ValidationError as exc:
        raise InputError(f"invalid run state in {run_dir / 'run.json'}: {exc}") from exc


def save_state(run_dir: Path, state: RunState) -> None:
    state.updated_at = utc_now()
    state.write_json(run_dir / "run.json")
