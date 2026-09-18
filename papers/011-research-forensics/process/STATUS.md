# STATUS — ARIS4C011

Updated: 2026-09-18

## State

**RESEARCH DESIGN + BENCHMARK SPECIFICATION LOCKED**

The project is promoted as ARIS4C011. It is not yet an empirical paper and no performance claims are permitted until Benchmark v0 is materialised and evaluated.

## Locked decisions

- Unit of truth: issue-level evidence, not author-level misconduct labels.
- Primary benchmark: content-only blind Track A.
- Secondary benchmark: open-world triage Track B.
- Primary endpoint: eligible issue-type recall at a prespecified false-alert burden.
- Core comparison: integrated framework vs detector families vs LLM-only reviewer.
- Required analysis: leave-one-family-out ablation.
- Evidence fusion: evidence graph / review-priority output, not a fraud probability.
- Applicability/abstention must be measured.
- Fairness audit required; geographic or language identity cannot be a suspicion feature.
- Known-notice comparator language: "no-known-integrity-concern", not "clean".

## Gates

### Gate 1 — benchmark provenance
Required before corpus construction is considered complete:
- DOI/source provenance for every labelled paper;
- notice/correction reason mapped to a controlled issue taxonomy;
- distinction between confirmed problem, correction/error, and no-known-concern comparison;
- duplicate manuscripts and multiple notices deduplicated.

### Gate 2 — leakage
Required before model training:
- family/group split for related paper-mill clusters, duplicated templates, author networks, and article families;
- no post-publication notice input in Track A;
- no direct use of outcome-defining retraction reason text as a feature;
- temporal holdout.

### Gate 3 — detector validity
Every detector must document:
- applicability conditions;
- failure modes;
- abstention rule;
- output semantics;
- calibration evidence if probabilistic;
- evidence class.

### Gate 4 — confirmatory freeze
Before final benchmark scoring:
- primary and secondary metrics frozen;
- alert burden threshold frozen;
- detector versions/hashes frozen;
- matching strategy frozen;
- subgroup/fairness analyses frozen.

## Next execution

1. Materialise Benchmark v0 manifest from Crossref/Retraction Watch plus correction/error and comparator sets.
2. Implement deterministic statistical checks first.
3. Add bibliographic verification and post-publication notice adapters.
4. Add text/paper-mill and image modules only after detector contracts are explicit.
5. Run Pilot 0 and update the design only for implementation defects, not outcome-driven optimisation.
