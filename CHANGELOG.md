# Changelog

All notable changes are recorded here. This project uses semantic versioning; alpha releases do
not imply completed comparative effectiveness evidence.

## [Unreleased]

- Completed the fixed 60-seed, four-system Codex benchmark: 240 hash-verified outputs, a completed
  execution manifest, retained failure provenance, and two hash-bound opaque human-rater packs.
- Benchmark execution now preserves the diagnostic stderr tail and circuit-breaks a queue after
  quota, login, or HTTP 429 failures instead of marking every remaining run failed.
- Blind rater packs now include hash-bound identity-free scoring guidance and response schemas;
  contextual leakage detection distinguishes system-profile disclosure from research terminology.
- Added an identity-neutral rater-side response-lock command that verifies complete coverage,
  immutable anonymous assignments, copied-output hashes, and consistent rater metadata before
  committing both human-response hashes.
- Public scoring now verifies the declared adapter file and completed run-matrix path in addition
  to their hashes, and rejects drift between locked blind responses and unblinded judgments.
- Human-primary blind evaluation, credentialed live retrieval, and remote pull-request CI evidence
  remain release gates for a stable comparative release.

## [0.2.0a1] - 2026-07-16

### Added

- Installable Python 3.9+ `src/` package and `shushu` CLI.
- Resumable, hash-bound P0–P9 lineage-first workflow with strict schemas and fail-closed gates.
- arXiv, OpenAlex, Semantic Scholar, and OpenReview retrieval with retry, durable failures,
  cross-source deduplication, provenance, and offline replay manifests.
- PDF/HTML full-text acquisition and a page-located Claim-Evidence Ledger.
- Lineage, contribution-saturation, gap, idea-portfolio, six-axis novelty collision, reviewer-audit,
  and final-report validation.
- Fixed 60-seed benchmark, external adapter execution, resumable 240-run matrix, human-primary
  metrics, blind-pack generation, unblinding, and public-claim release gates.
- Three offline-verifiable real-paper P0–P9 known-scoop examples.
- Python 3.9/3.12 GitHub Actions workflow and a hash-locked development/build environment.

### Compatibility

- Retained the three v0.1 script entry points as tested wrappers.
- Added migration guidance in `docs/migration-v0.2.md`.

### Known limitations

- OpenAlex live access requires `OPENALEX_API_KEY`; reliable Semantic Scholar benchmarking may
  require `SEMANTICSCHOLAR_API_KEY`.
- There are no public comparative effectiveness claims until all 240 model runs and two-person
  blind human evaluation are complete and the aggregate artifacts pass the release gate.

[Unreleased]: https://github.com/YingaoWang-casia/shushu-novelty-finder/compare/v0.2.0a1...HEAD
[0.2.0a1]: https://github.com/YingaoWang-casia/shushu-novelty-finder/releases/tag/v0.2.0a1
