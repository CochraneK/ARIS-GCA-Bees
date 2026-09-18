# STATUS — ARIS4C011

Updated: 2026-09-18

## State

**RESEARCH DESIGN LOCKED · BENCHMARK SOURCE INGEST IN PROGRESS**

ARIS4C011 is promoted on main. The framework and benchmark protocol are locked; the current work is materialising Benchmark v0 without introducing label leakage or source-schema errors. No empirical performance claims are permitted yet.

## Completed

- 10-family detector taxonomy.
- Evidence-class and evidence-graph semantics.
- Track A content-only vs Track B open-world benchmark split.
- Issue-level ground-truth tiers.
- Shortcut-stress-test plan including BMMDetect-like retraction classifiers.
- Pilot 0 deterministic GRIM-style and N-consistency checks.
- Benchmark-v0 leakage-safe manifest builder.
- Initial 8 unit tests passed before promotion.
- Live Crossref production API source-anatomy audit.
- Crossref assertion/event adapter added after identifying notice-DOI vs target-DOI ambiguity.

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
- Crossref top-level work metadata must never be assumed to describe `update-to` target works.
- Publisher and Retraction Watch assertions are preserved separately before event-level collapse.

## Gates

### Gate 1 — benchmark provenance
Required before corpus construction is considered complete:
- target DOI/source provenance for every labelled paper;
- assertion vs event separation;
- target metadata resolved independently of notice metadata;
- notice/correction reason mapped to a controlled issue taxonomy;
- distinction between confirmed problem, correction/error, and no-known-concern comparison;
- duplicate manuscripts and multiple notices deduplicated without deleting provenance.

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

1. Resolve `target_doi` metadata independently through Crossref.
2. Join Retraction Watch reason text by `record-id` while keeping it outside Track A.
3. Materialise a small adjudication seed across retractions and corrections.
4. Implement deterministic statistical checks against real full-text examples.
5. Add no-known-concern matching only after target metadata completeness is quantified.
