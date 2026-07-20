"""Cross-record idea-portfolio checks."""

from __future__ import annotations

from dataclasses import dataclass

from shushu_novelty.schemas import GapRecord, IdeaCandidate, PaperRecord


@dataclass(frozen=True)
class IdeaValidation:
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_ideas(
    ideas: list[IdeaCandidate], gaps: list[GapRecord], papers: list[PaperRecord]
) -> IdeaValidation:
    errors = []
    idea_ids = [item.idea_id for item in ideas]
    if len(idea_ids) != len(set(idea_ids)):
        errors.append("idea IDs must be unique")
    gap_ids = {item.gap_id for item in gaps}
    paper_ids = {item.paper_id for item in papers}
    for idea in ideas:
        unknown_gaps = set(idea.gap_ids) - gap_ids
        if unknown_gaps:
            errors.append(
                f"idea {idea.idea_id} references unknown gaps: "
                + ", ".join(sorted(unknown_gaps))
            )
        unknown_papers = set(idea.closest_prior_work) - paper_ids
        if unknown_papers:
            errors.append(
                f"idea {idea.idea_id} references unknown closest papers: "
                + ", ".join(sorted(unknown_papers))
            )
    return IdeaValidation(errors=errors)
