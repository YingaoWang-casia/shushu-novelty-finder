import pytest

from shushu_novelty.errors import InputError
from shushu_novelty.evaluation.codex_adapter import build_profile_prompt, sha256_text


def test_bare_profile_preserves_seed_prompt_exactly_after_outer_whitespace():
    assert build_profile_prompt("  audit this idea\n", "bare") == "audit this idea"


def test_self_reflection_is_distinct_without_skill_leakage():
    prompt = build_profile_prompt("audit this idea", "self-reflection")

    assert prompt.startswith("audit this idea\n\n")
    assert "privately draft" in prompt
    assert "shushu-skill" not in prompt


def test_v01_and_v02_prompts_are_distinct_and_deterministic():
    v01 = build_profile_prompt("audit this idea", "shushu-v0.1", "PINNED SKILL")
    v02 = build_profile_prompt(
        "audit this idea", "shushu-v0.2", "PINNED SKILL", "ENGINEERING GATES"
    )

    assert "PINNED SKILL" in v01
    assert "ENGINEERING GATES" not in v01
    assert "ENGINEERING GATES" in v02
    assert sha256_text(v01) == sha256_text(v01)
    assert sha256_text(v01) != sha256_text(v02)


def test_shushu_profiles_require_their_pinned_protocols():
    with pytest.raises(InputError, match="pinned Skill"):
        build_profile_prompt("audit this idea", "shushu-v0.1")
    with pytest.raises(InputError, match="engineering protocol"):
        build_profile_prompt("audit this idea", "shushu-v0.2", "PINNED SKILL")
