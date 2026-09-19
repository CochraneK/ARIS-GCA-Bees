# Confirmatory feasibility frame v0

Updated: 2026-09-19

## State

**FEASIBILITY ONLY — NOT CONFIRMATORY**

This checkpoint freezes a detector-output-blind acquisition/adjudication frame. It is not a benchmark result and cannot be used for sensitivity, specificity, threshold tuning, or confirmatory hypothesis testing.

## Frozen frame

- 80 unique target works / papers.
- 20 balanced calendar-year × update-type strata: 2016–2025 × correction/retraction.
- 4 papers per stratum.
- 42 development-exposed DOIs excluded by the development exclusion registry.
- 80/80 unique target DOIs and 80/80 unique target-notice event keys after the deduplication hardening.
- Selection is deterministic within each stratum and does not use detector output or review priority.
- All 80 rows remain issue-adjudication **UNASSESSED**, required-artifact-role **UNASSESSED**, and artifact-state **UNASSESSED**.

## Acquisition-feasibility signals

These fields are workload/provenance signals only:

- Crossref full-text link present: **79 / 80**.
- Crossref abstract present: **37 / 80**.
- Current title contains a correction/retraction/status marker: **28 / 80**.
- Current Crossref metadata has an updated-by relation: **80 / 80**.
- Crossref work type: **79 journal-article + 1 proceedings-article**.
- Distinct containers: **71**.
- Target publication years represented: **2000–2025**.

The 28 current-title status markers are direct evidence that current metadata cannot be treated as Track-A-safe. Historical version qualification and the existing Track-A allowlist remain mandatory.

## Allowed uses

- Estimate acquisition workload.
- Estimate issue-adjudication workload.
- Estimate historical-artifact availability / missingness after required-role qualification.
- Inform confirmatory sample-size planning without detector-effect peeking.

## Forbidden uses

- Detector performance estimation.
- Threshold tuning.
- Sensitivity or specificity estimation.
- Confirmatory hypothesis testing.

## Next gate

Create manager-only issue-adjudication packets for this frozen 80-record frame, assign issue family and required artifact role without detector output, then measure SAFE_EXACT / PROXY_ONLY / BLOCKED attrition. Only after corpus composition and attrition are frozen should grouped/temporal split values, detector versions/applicability, thresholds, leakage audit, and human-review protocol be closed.
