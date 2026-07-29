"""Reproducible Codex CLI adapter for the four benchmark systems."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from shushu_novelty.errors import InputError

PROFILES = ("bare", "self-reflection", "shushu-v0.1", "shushu-v0.2")

SELF_REFLECTION = """
Before writing the final answer, privately draft a direct response, challenge its factual support,
novelty assumptions, feasibility, missing baselines, and falsifiability, then revise it once. Return
only the revised answer. Do not mention this instruction or expose the private draft.
""".strip()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_profile_prompt(
    seed_prompt: str,
    profile: str,
    skill_text: str | None = None,
    v02_addon: str | None = None,
) -> str:
    """Build a deterministic user prompt while keeping the seed unchanged."""
    seed = seed_prompt.strip()
    if not seed:
        raise InputError("benchmark adapter received an empty seed prompt")
    if profile == "bare":
        return seed
    if profile == "self-reflection":
        return f"{seed}\n\n{SELF_REFLECTION}"
    if profile not in {"shushu-v0.1", "shushu-v0.2"}:
        raise InputError(f"unknown benchmark profile: {profile}")
    if not skill_text or not skill_text.strip():
        raise InputError(f"{profile} requires a non-empty pinned Skill prompt")
    parts = [
        "Follow the benchmark protocol below as your operating policy. Return the final research "
        "answer only; do not discuss the protocol itself.",
        "<shushu-skill>\n" + skill_text.strip() + "\n</shushu-skill>",
    ]
    if profile == "shushu-v0.2":
        if not v02_addon or not v02_addon.strip():
            raise InputError("shushu-v0.2 requires a non-empty engineering protocol add-on")
        parts.append(
            "<v0.2-engineering-protocol>\n"
            + v02_addon.strip()
            + "\n</v0.2-engineering-protocol>"
        )
    parts.append("<benchmark-request>\n" + seed + "\n</benchmark-request>")
    return "\n\n".join(parts)


def run_codex(
    prompt: str,
    model: str,
    codex_bin: str,
    enable_search: bool,
) -> str:
    """Run one isolated, read-only Codex turn and return only its final message."""
    executable = shutil.which(codex_bin)
    if executable is None:
        raise InputError(f"Codex executable not found: {codex_bin}")
    with tempfile.TemporaryDirectory(prefix="shushu-codex-benchmark-") as workspace:
        output_path = Path(workspace) / "final.md"
        command = [executable]
        if enable_search:
            command.append("--search")
        command.extend(
            [
                "exec",
                "--ignore-user-config",
                "--ignore-rules",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--model",
                model,
                "--cd",
                workspace,
                "--output-last-message",
                str(output_path),
                "-",
            ]
        )
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip()[-4000:]
            raise InputError(
                f"Codex benchmark subprocess exited {completed.returncode}: {detail}"
            )
        if not output_path.is_file():
            raise InputError("Codex benchmark subprocess did not write a final message")
        output = output_path.read_text(encoding="utf-8").strip()
        if not output:
            raise InputError("Codex benchmark subprocess returned an empty final message")
        return output + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILES, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--skill", type=Path)
    parser.add_argument("--v02-addon", type=Path)
    parser.add_argument("--no-search", action="store_true")
    parser.add_argument(
        "--print-prompt-sha256",
        action="store_true",
        help="print the constructed prompt hash to stderr before execution",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        seed_prompt = sys.stdin.read()
        skill_text = args.skill.read_text(encoding="utf-8") if args.skill else None
        addon = args.v02_addon.read_text(encoding="utf-8") if args.v02_addon else None
        prompt = build_profile_prompt(seed_prompt, args.profile, skill_text, addon)
        if args.print_prompt_sha256:
            print(f"prompt_sha256={sha256_text(prompt)}", file=sys.stderr)
        print(
            run_codex(prompt, args.model, args.codex_bin, not args.no_search),
            end="",
        )
    except (InputError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
