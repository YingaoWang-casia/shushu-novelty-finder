# v0.2 release checklist

## Runtime and compatibility

- [ ] version and changelog are final;
- [x] `requirements-dev.lock` is regenerated from `pyproject.toml`, hash-verified, and unchanged
      after the final clean-environment install;
- [x] legacy wrappers still pass regression tests;
- [x] wheel and source distribution build cleanly with the locked build backend via
      `python -m build --no-isolation`;
- [ ] clean Python 3.9 and 3.12 CI jobs pass on the release commit.

## Evidence and workflow gates

- [x] four connectors pass their contract tests;
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
- [x] blind packs contain 480 opaque scalar and 720 randomized pairwise assignments with the
      coordinator key withheld until response lock;
- [ ] blind responses, coordinator key, and package manifest are hash-bound, and deterministic
      unblinding exactly reproduces the published scalar and pairwise judgments;
- [ ] at least two research-experienced human raters completed blind ratings;
- [ ] agreement (Cohen's kappa) is reported;
- [ ] public metrics cover retrieval, evidence, idea quality, and calibration;
- [ ] the public evaluation is marked `publishable: true` and human-primary;
- [ ] README effectiveness claims exactly match the hashed public report.

Until every public-effectiveness item is checked, the project may publish an alpha engineering
release, but it must not claim comparative quality gains.
