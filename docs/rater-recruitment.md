# Recruiting the two human research raters

This evaluation cannot be completed by an LLM pretending to be a person. Use two independent
research-experienced raters and pay for both screening/pilot work and the full assignment. The
current balanced-overlap pack reduces duplicate work while preserving all 60 benchmark seeds and
a preregistered agreement subset.

## Required profile

Recruit two people who meet all of the following:

- current or prior graduate-level research experience in computer science, AI, information
  retrieval, data mining, or a closely related field;
- experience reading research papers and checking citations, baselines, novelty, and experimental
  claims;
- no involvement in this repository, its outputs, or the four evaluated system configurations;
- no coordination with the other rater before both response files are locked;
- willingness to report actual research-experience years and any conflicts of interest.

A degree title alone is not sufficient. Screen with one paid pilot seed and inspect whether the
candidate verifies literature evidence, distinguishes metadata/abstract/full text, and applies the
rubric consistently.

## Workload to disclose before hiring

The retained `balanced-overlap` design assigns each rater:

- 36 of the 60 seeds;
- 144 scalar output assessments (four per seed);
- 216 pairwise decisions (six per seed);
- approximately 188,000–190,000 words of supplied system output in the current packs, before any
  external paper verification.

Do not advertise this as a short survey. Run a paid pilot, measure real completion time, and agree
on an hourly contract or milestones from that evidence. Do not use an unpaid expertise screener.

## Suggested recruitment routes

- A research-participant platform with paid custom screening, such as
  [Prolific custom screening](https://researcher-help.prolific.com/en/articles/445155-how-to-use-custom-screening-to-recruit-specific-participants),
  can locate a narrow participant profile. The screen must not disclose system identities.
- A specialist marketplace, such as
  [Upwork academic research freelancers](https://www.upwork.com/hire/academic-research-freelancers/),
  can be used for a paid pilot followed by hourly or milestone work.
- A university lab mailing list or direct professional referral is acceptable if conflicts are
  disclosed and the work is compensated.

The platform is not part of the evidence. The locked response files, experience disclosure,
package commitment, and preregistered protocol are the evidence.

## Copy-ready role brief

> We are recruiting a computer-science research reviewer for a blinded evaluation of research-
> audit outputs. You will independently assess 36 fixed research prompts, four anonymous outputs
> per prompt, and six anonymous pairwise comparisons per prompt. The work requires literature
> search, citation verification, novelty assessment, and consistent use of a supplied rubric. A
> paid one-seed pilot is required before the full assignment. You must have research-paper review
> experience, disclose years of research experience and conflicts, avoid identifying the systems,
> and work independently until responses are cryptographically locked. Please quote an hourly rate
> and describe relevant research/review experience.

## Coordinator procedure

1. Keep `coordinator/`, the completed run matrix, execution checkpoints, and system-labelled
   outputs private.
2. Send each person only their own `raters/<id>/` directory and the manifest SHA-256 commitment.
3. Use a duplicated pilot pack derived from a shared seed; do not reuse the pilot response in the
   final locked files unless the pilot was declared in advance and followed the final protocol.
4. Require each rater to run `blind-eval init`, complete every assigned row, inspect progress with
   `blind-eval status`, and run `blind-eval lock` before returning files.
5. Run `shushu benchmark collect-responses` with both rater directories, the coordinator manifest,
   key, and pre-rating commitment. It verifies both locks and writes the only combined response
   files allowed for unblinding; do not concatenate JSONL manually.
6. Report pre-adjudication scalar and pairwise Cohen's kappa on the 12 shared seeds. Any later
   adjudication is separate and cannot replace those agreement statistics.

The current local pack is `evals/blind-balanced-v1/`. Its coordinator-manifest commitment is
`552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40`. Regenerate and publish a new
commitment if any rater-side file changes before recruitment.
