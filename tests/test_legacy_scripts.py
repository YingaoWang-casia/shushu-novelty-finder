import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_legacy_arxiv_wrapper_has_stable_cli():
    result = run_script("scripts/search_arxiv.py", "--help")

    assert result.returncode == 0
    assert "--canonical" in result.stdout


def test_legacy_normalizer_wrapper_renders_cards(tmp_path):
    source = tmp_path / "papers.jsonl"
    output = tmp_path / "cards.md"
    source.write_text(json.dumps({"title": "Fixture Paper"}) + "\n", encoding="utf-8")

    result = run_script(
        "scripts/normalize_papers.py",
        str(source),
        "--output",
        str(output),
    )

    assert result.returncode == 0
    assert "Fixture Paper" in output.read_text(encoding="utf-8")


def test_legacy_report_validator_accepts_complete_example():
    result = run_script(
        "scripts/validate_report.py",
        "examples/runs/rag-known-scoop/report/report.md",
        "--paper-mode",
    )

    assert result.returncode == 0
    assert "All required sections found" in result.stdout
