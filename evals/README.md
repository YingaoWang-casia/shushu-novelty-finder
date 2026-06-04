# Evals

This folder defines lightweight checks for `shushu-novelty-finder` outputs.

The goal is not to automatically judge scientific truth. The goal is to check whether a run follows the Skill's evidence, novelty-ranking, reviewer-objection, and paper-readiness discipline.

## Files

- `cases/rag-evaluation.md` - Direction Mode eval case for RAG evaluation.
- `cases/seed-paper.md` - Seed Paper Mode eval case.
- `checks/output-checklist.md` - required output checklist.
- `checklist.md` - legacy checklist kept for compatibility.

## Required Checks

A valid output should include:

- input mode;
- Research Scope Card or Seed Paper Card;
- concrete paper names or explicit `placeholder / candidate / unverified` labels;
- Paper Evidence Cards for key papers;
- Claim-Evidence Map for top claims;
- Literature Timeline and Trend Matrix in Research / Paper Mode;
- gap evidence labels;
- weak / medium / strong novelty ranking;
- paper type routing for top ideas;
- minimum experiments;
- baseline decision for top ideas;
- reviewer objection pre-mortem;
- kill / continue criteria;
- risks and reviewer reject reasons;
- paper-readiness verdict.

## Failure Checks

A bad output should be flagged if it:

- claims nobody has done something without search evidence;
- lists papers without explaining their evidence role;
- gives innovation ideas without feasibility or risks;
- ignores baselines;
- treats preprints as accepted papers;
- treats candidate papers as verified support;
- produces a paper plan without a falsifiable claim;
- gives no reviewer objections;
- gives no condition for downgrading or killing the idea;
- uses a seed paper title without extracting task, input, output, dataset, metric, and claim;
- calls an ordinary pipeline a new method without a controlled comparison.

## Usage

Use these checks after generating an output. If any required item is missing, downgrade the answer quality and ask the Skill to repair the missing section instead of accepting the report.
