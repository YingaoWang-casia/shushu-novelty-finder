# v0.2 release checklist

## Published engineering Alpha

- [x] `v0.2.0a1` is published as a GitHub prerelease from main commit
      `2cfa010c24d7bc72ff1686c0383584e71fe95763`;
- [x] the three READMEs show the Alpha evidence boundary before product details;
- [x] the tagged wheel and source distribution passed the distribution audit and expose SHA-256
      digests in the release notes;
- [x] the public wheel was downloaded from GitHub, installed in a clean Python 3.9 environment,
      and passed `shushu --version` and `shushu check`;
- [x] main-branch Python 3.9 and 3.12 CI passed on the Alpha release commit.

## Runtime and compatibility

- [ ] version and changelog are final;
- [x] `requirements-dev.lock` is regenerated from `pyproject.toml`, hash-verified, and unchanged
      after the final clean-environment install;
- [x] legacy wrappers still pass regression tests;
- [x] wheel and source distribution build cleanly with the locked build backend via
      `python -m build --no-isolation`;
- [ ] clean Python 3.9 and 3.12 CI jobs pass on the final tagged release commit; both jobs already
      pass on draft PR #1.

## Evidence and workflow gates

- [x] four connectors pass their contract tests;
- [x] the fixed 20-topic live suite passes all four sources at 100% with zero post-dedup
      duplicates and replay-verifiable manifests;
- [x] full-text and Claim-Evidence Ledger fixtures pass;
- [x] resume, collision, reviewer, and final-report gates pass;
- [x] the 60-seed benchmark composition is unchanged or versioned explicitly;
- [x] retrieval and full-text failure logs are represented in the final report.
- [x] all example P0–P9 states pass replay, auxiliary-bundle, and final-report hash verification;

## Public effectiveness evidence

- [x] all 240 required system runs are complete;
- [x] adapter and prompt provenance hashes are preserved for all 240 runs;
- [x] the completed execution manifest binds model, CLI/runtime version, adapter, benchmark, and
      final run-matrix hashes;
- [x] balanced-overlap blind packs contain 288 opaque scalar and 432 randomized pairwise
      assignments, collectively cover all 60 seeds, share 12 stratified seeds, and withhold the
      coordinator key until response lock;
- [ ] blind responses, coordinator key, and package manifest are hash-bound, and deterministic
      unblinding exactly reproduces the published scalar and pairwise judgments;
- [ ] at least two research-experienced human raters completed blind ratings;
- [ ] agreement (Cohen's kappa) is reported;
- [ ] public metrics cover retrieval, evidence, idea quality, and calibration;
- [ ] the public evaluation is marked `publishable: true` and human-primary;
- [ ] README effectiveness claims exactly match the hashed public report.

Until every public-effectiveness item is checked, the project may publish an alpha engineering
release, but it must not claim comparative quality gains.
