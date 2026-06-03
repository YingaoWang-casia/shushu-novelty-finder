# Evals

This folder defines lightweight checks for shushu-novelty-finder outputs.

The goal is not to score scientific truth automatically. The goal is to check whether a run follows the Skill's evidence and paper-readiness discipline.

## Required checks

A valid output should include:

- input mode: Lite, Research, or Paper;
- Research Scope Card;
- concrete paper names for trends;
- Paper Evidence Cards for key papers;
- gap evidence labels;
- weak / medium / strong novelty ranking;
- risks and minimum experiments;
- paper-readiness verdict for top ideas in Paper Mode.

## Failure checks

A bad output should be flagged if it:

- claims nobody has done something without search evidence;
- lists papers without explaining their evidence role;
- gives innovation ideas without feasibility or risks;
- ignores baselines;
- treats preprints as accepted papers;
- produces a paper plan without a falsifiable claim.
