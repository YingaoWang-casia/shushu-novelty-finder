# ADR 0003: Comparative claims require human-primary public evidence

- Status: accepted
- Date: 2026-07-16

## Context

Structural checks and LLM judges can detect omissions, but they cannot independently prove that a
research-idea system is more novel, more accurate, or better calibrated than a baseline. Unbound
metrics can also be detached from the model outputs they supposedly evaluate.

## Decision

Comparative README claims require all 240 fixed system runs, two research-experienced human raters,
complete scalar and six-way pairwise coverage, agreement statistics, and every required metric
family. The public result binds the benchmark seeds, provenance-complete run matrix, scalar
judgments, and pairwise judgments by path and SHA-256. Release and final-report gates re-read those
files. LLM judgments remain auxiliary and are excluded from primary metrics.

System labels are hidden through opaque per-rater assignments and randomized pair order. The
coordinator key is joined only after responses are locked.

## Consequences

Engineering alpha releases can ship without comparative claims. Stable quality claims remain
blocked until external human evidence exists; synthetic ratings or a correctly shaped JSON file
cannot satisfy the release gate.
