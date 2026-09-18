# STATUS — ARIS4C011

Updated: 2026-09-18

## State

**RESEARCH DESIGN LOCKED · BENCHMARK V0 REAL-DATA SEED MATERIALISED**

ARIS4C011 is promoted on main. The framework and benchmark protocol are locked. A first three-record real-data seed has now been used to validate source relationships, label heterogeneity, and metadata-leakage gates. No empirical detector-performance claims are permitted yet.

## Completed

- 10-family detector taxonomy.
- Evidence-class and evidence-graph semantics.
- Track A content-only vs Track B open-world benchmark split.
- Issue-level ground-truth tiers.
- Shortcut-stress-test plan including BMMDetect-like retraction classifiers.
- Pilot 0 deterministic GRIM-style and N-consistency checks.
- Benchmark-v0 manifest builder.
- Crossref assertion/event adapter.
- Live Crossref target-metadata resolution audit.
- Real-data seed with three heterogeneous official retraction cases.
- Metadata-leakage guard for `RETRACTED:` / `RETRACTED ARTICLE:` title markers.
- Track A changed from deny-list projection to an explicit manifest/feature allow-list.
- Track A now fails closed until both title-history and document-safety gates pass.

## Critical empirical design finding

A current bibliographic record can already contain the later outcome. Therefore "content-only" evaluation must be defined by **time-safe artifacts**, not merely by excluding a `retraction_reason` column.

The real seed also demonstrates that official retractions can concern manuscript validity, authorship, or peer-review/editorial processes. Retraction status cannot serve as a single issue label.

## Locked decisions

- Unit of truth: issue-level evidence, not author-level misconduct labels.
- Primary benchmark: time-safe content-only blind Track A.
- Secondary benchmark: open-world triage Track B.
- Primary endpoint: eligible issue-type recall at a prespecified false-alert burden.
- Core comparison: integrated framework vs detector families vs LLM-only reviewer.
- Required analysis: leave-one-family-out ablation.
- Evidence fusion: evidence graph / review-priority output, not a fraud probability.
- Applicability/abstention must be measured.
- Fairness audit required; geographic or language identity cannot be a suspicion feature.
- Known-notice comparator language: "no-known-integrity-concern", not "clean".
- Crossref top-level work metadata must never be assumed to describe `update-to` target works.
- Current target metadata cannot enter Track A wholesale.
- Publisher and Retraction Watch assertions are preserved separately before event-level collapse.

## Gates

### Gate 1 — benchmark provenance
- target DOI/source provenance for every labelled paper;
- assertion vs event separation;
- target metadata resolved independently of notice metadata;
- notice/correction reason mapped to a controlled issue taxonomy;
- distinction between confirmed problem, correction/error, and no-known-concern comparison;
- duplicate manuscripts and multiple notices deduplicated without deleting provenance.

### Gate 2 — time-safe / leakage-safe Track A
- no post-publication notice or outcome field;
- clean historical-equivalent title/document;
- no label-bearing filenames/paths;
- grouped family split;
- temporal holdout;
- explicit feature allow-list.

### Gate 3 — detector validity
Every detector documents applicability, failure modes, abstention, output semantics, calibration (if probabilistic), and evidence class.

### Gate 4 — confirmatory freeze
Before final scoring: metrics, alert threshold, detector versions, matching strategy, split, and subgroup analyses are frozen.

## Next execution

1. Scale the real-data seed while retaining assertion/event/target separation.
2. Add correction/corrigendum cases as the essential honest-error stress stratum.
3. Acquire time-safe manuscript artifacts for a pilot subset and quantify how often historical equivalence is achievable.
4. Run deterministic statistical/table checks on eligible full texts.
5. Construct no-known-concern comparators only after target metadata completeness and time-safety rates are measured.
