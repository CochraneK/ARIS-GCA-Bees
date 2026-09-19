# Pilot 3 — reproducible correction-candidate expansion

Updated: 2026-09-19

## Why this stage exists

After the first real pre-outcome true-positive, manually searching correction notices one at a time became the next bottleneck. Pilot 3 converts candidate selection into an auditable queue.

This queue is **not** the confirmatory benchmark. It is an acquisition-enrichment device used to decide where historical-object recovery effort is most likely to produce valid Track A cases. Later correction text may guide acquisition priority, but it is never exposed to Track A detectors.

## Priority dimensions

Candidates are scored on five dimensions:

1. **artifact state** — SAFE_EXACT material already known is favoured;
2. **verification mode** — deterministic/internal checks are favoured over re-analysis;
3. **required role** — tables/text/references are generally easier to recover than image-only or raw-data cases;
4. **scientific-content relevance** — substantive errors outrank formatting-only corrections;
5. **publication-to-correction window** — longer windows improve the chance that a clean historical object was archived.

Completed true-positive cases are removed from active acquisition. Formatting-only cases are explicitly routed to CONTROL even if the historical object is excellent.

## Current queue

The queue is now regenerated from `data/pilot/pilot3_correction_candidates.csv`; completed and blocked cases no longer remain artificially at the top.

### COMPLETE

**10.1371/journal.pone.0258910** — completed F5 cross-source true-positive calibration case.

**10.1371/journal.pone.0180906** — completed F3 table-schema true-positive.
- original PMC record: PMC5521765;
- SAFE_EXACT preserved-original Table 1;
- section A detected result columns: 5;
- section B detected result columns: 2;
- content-only detector: `F3_TABLE_SCHEMA_COLUMN_DROP_V1`;
- detector output: `FLAG`;
- manager-held 2018 correction label: documented two-column omission;
- outcome/correction metadata visible to detector: **false**;
- misconduct inference: **false**.

### ACTIVE / SECONDARY

1. **10.1371/journal.pone.0180395** — corrected two-tailed p-values plus table-schema changes.
   - potential F1/F3 case;
   - requires contemporaneously recoverable source statistics/table evidence.

2. **10.1371/journal.pone.0293412** — Table 1 country counts/proportions.
   - historical table wrapper is SAFE_EXACT;
   - required table image has no independently verified pre-correction capture;
   - current object-level status: `NO_PRE_EVENT_OBJECT` / BLOCKED for table-content F3;
   - keep available for future archival recovery, but do not score it now.

3. **10.1371/journal.pone.0163749** — corrected Brodmann-area table entries.
   - potential F3 structural/token anomaly case;
   - historical table object still required.

### CONTROL

**10.1371/journal.pone.0263337** — decimal-separator formatting case.
- SAFE_EXACT pre-correction PDF;
- retained as a formatting/honest-error control, not a scientific contradiction.

### DEFER

- 10.1371/journal.pone.0075637 — requires re-analysis/model specification rather than a cheap deterministic manuscript check.
- 10.1371/journal.pone.0142234 — very short correction window and mostly statement/heading changes.

## Selection-bias rule

Pilot 3 is allowed to be enriched for recoverable, detector-compatible cases because its purpose is pipeline development.

No confirmatory sensitivity, precision, or comparative-performance claim may be calculated from this queue. A later confirmatory cohort must be selected under a frozen, broader sampling protocol independent of whether a detector is expected to succeed.
