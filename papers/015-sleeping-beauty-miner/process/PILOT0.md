# ARIS4C015 Pilot 0 — Metric fidelity and time-safety

Updated: 2026-09-18

## Purpose

Pilot 0 is a plumbing and validation study, not a claim that ARIS4C015 can already predict future breakthroughs.

It asks four narrower questions:

1. Can the code reconstruct complete zero-filled annual citation histories from citation edges?
2. Does the deterministic implementation of Beauty Coefficient B and awakening time reproduce values from the same underlying citation history?
3. Does historical-cutoff truncation prevent post-cutoff citation and integrity leakage?
4. Can the agent emit an auditable Candidate Evidence Card while preserving ABSTAIN and ARIS4C011 quarantine semantics?

## Reference cases

`data/known_cases_ke2015.csv` contains literature-derived reference cases from Ke et al. (2015), Table 1.

These are **reference targets**, not new empirical observations from ARIS4C015.

The table includes published B and awakening year for classic delayed-recognition papers such as:

- Freundlich (1906);
- Hummers & Offeman (1958);
- Patterson (1939);
- Cassie & Baxter (1944);
- Turkevich et al. (1951);
- Einstein, Podolsky & Rosen (1935);
- Washburn (1921).

Reference:
Ke Q, Ferrara E, Radicchi F, Flammini A. Defining and identifying Sleeping Beauties in science. PNAS. 2015;112(24):7426–7431. doi:10.1073/pnas.1424329112.

## Pilot 0A — Formula fidelity

### Synthetic unit tests

The repository contains hand-checkable synthetic citation trajectories with known B and awakening-time outputs.

Pass criterion:
- all deterministic tests pass in CI.

### Same-history replication

When a complete annual citation history from the original or equivalent source is available:

1. reconstruct annual citation counts;
2. calculate B and awakening time;
3. compare against values computed independently from the same vector.

Pass criterion:
- numerical equality within floating-point tolerance;
- identical awakening age under the declared tie policy.

## Pilot 0B — Cross-source replication

Reconstruct the seven literature reference cases using SciSciNet-v2/OpenAlex-derived citation edges.

Important limitation:

Ke et al. used Web of Science / APS data. OpenAlex/SciSciNet is a different citation graph. Therefore **the published B value is not expected to match exactly across sources**.

This comparison measures:
- direction and rank stability;
- awakening-year proximity;
- sensitivity to bibliographic coverage;
- identifier/linkage failures.

Report:
- reconstructed B;
- published B;
- absolute and relative difference;
- reconstructed awakening year;
- published awakening year;
- source/snapshot;
- total reconstructed citations;
- coverage warnings.

A difference is not a code failure unless the same citation vector produces inconsistent metrics.

## Pilot 0C — Historical-cutoff leakage test

For each reference paper, define one or more artificial historical cutoffs before its published awakening year.

Examples:
- awakening year - 20;
- awakening year - 10;
- awakening year - 5.

At each cutoff:

1. truncate incoming citation edges;
2. recompute citation-only baseline features;
3. hide later post-publication integrity events;
4. prohibit future patent/review/award information;
5. emit a Candidate Evidence Card.

Pass criterion:
- no output contains citation counts or 011 findings that occur after the cutoff;
- unknown-timestamp integrity findings do not enter prospective scoring.

This demonstrates **time safety**, not predictive success.

## Pilot 0D — Baseline benchmark scaffold

Run transparent baselines:

- current citations;
- recent 3-year momentum;
- recent acceleration;
- partial-trajectory Beauty Coefficient;
- dormancy length.

These establish the minimum benchmark for later models.

No arbitrary weighted "Sleeping Beauty score" is introduced in Pilot 0.

## Pilot 0E — ARIS4C011 integration

Use synthetic and later empirical 011 findings to verify routing:

- no findings / insufficient coverage -> ABSTAIN;
- cutoff-safe checks with no flag -> CLEAR;
- one unresolved flag -> CAUTION;
- at least two independent E1-E3 groups -> QUARANTINE;
- post-cutoff findings -> excluded;
- unknown-time findings in prospective mode -> excluded / ABSTAIN.

QUARANTINE is a review-routing state, not a misconduct judgment.

## Data acquisition order

1. **SciSciNet-v2 local slice**, if a reproducible subset can be queried/exported.
2. OpenAlex bounded API for identifier resolution and smaller validation probes.
3. SciSciNet v1 metrics for cross-checking where compatible.

Do not download the entire SciSciNet-v2 dataset merely for Pilot 0.

## Expected outputs

- `data/known_cases_ke2015.csv`
- reconstructed case-level histories (not committed if too large)
- `data/pilot0_results.csv`
- provenance manifest
- discrepancy report
- Candidate Evidence Card examples
- CI log
- explicit PASS / BLOCKED status per Pilot 0 component

## Promotion gate

ARIS4C015 may move from **agent implementation** to **empirical Pilot 0 complete** only after at least one non-synthetic citation source has been ingested and the discrepancy report is produced.

It may move to **prospective model development** only after:
- historical-cutoff reconstruction works;
- leakage tests pass;
- field/cohort normalization is specified;
- transparent baselines are established.
