# ADR 0004: Balanced overlap for human rating

- Status: accepted
- Date: 2026-07-20

## Context

Complete duplicate rating assigns both people all 60 seeds, 240 scalar rows and 360 pairwise rows
each. The current outputs contain more than 300,000 words before literature verification, making
the 1,200-judgment protocol costly enough to threaten completion. The engineering plan requires at
least two research-experienced blind raters and an agreement statistic; it does not require every
seed to be rated twice.

Removing the second rater, replacing people with LLM judgments, or reducing the collective suite
would weaken the stated acceptance target. Rating a non-preregistered convenience subset would
also make agreement and system comparisons difficult to audit.

## Decision

The recommended design uses exactly two human raters and 12 shared seeds. Shared seeds follow the
60-seed suite's case-type proportions (4 broad-direction, 4 seed-paper, 2 known-scoop, and 2
mechanism-transfer) and cover all eight domains. The other 48 seeds are divided into two disjoint,
jointly case/domain-balanced sets. Each rater therefore receives 36 seeds, all four outputs per
seed, and all six pairwise comparisons per seed.

The union must cover all 60 seeds. The overlap must contain at least 12 complete seeds. Scalar and
pairwise Cohen's kappa use only shared items. Aggregate system metrics normalize human judgments
within each seed/system to total weight one, preventing shared seeds from receiving double weight.
The coordinator manifest commits the complete assignment plan and stratum counts before rating.

The original complete duplicate design remains available through `--rating-design complete`.

## Consequences

The minimum retained design contains 288 scalar and 432 pairwise judgments instead of 480 and 720,
a 40% reduction. Both people are still required, all 60 seeds still contribute to system metrics,
and 48 scalar plus 72 pairwise shared items support agreement reporting. Estimates from a partial
design are less redundant than complete duplicate rating, so the public report must disclose the
design, per-rater seed counts, shared seed IDs, and agreement subset size.
