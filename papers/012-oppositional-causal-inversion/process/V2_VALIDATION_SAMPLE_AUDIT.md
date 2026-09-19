# V2 fresh validation sample audit — ARIS4C012

Frozen: 2026-09-19

## Result

A **fresh 30-record validation sample** is frozen for Schema v2.

- Source frame: 165 reproducible retrieval candidates.
- Pilot 0B records excluded by stable identifier/title: 30.
- Eligible fresh pool after exclusion: 155.
- Six retrieval strata represented: **5 records each**.
- Provider mix in frozen sample: **14 OpenAlex / 16 Crossref**.
- Overlap with Pilot 0B: **0**.

## Selection rule

The draw is deterministic and reproducible:

1. exclude every Pilot 0B record by DOI/provider stable ID/title;
2. within each stratum compute FNV-1a 32-bit over `ARIS4C012-V2-A2B2-20260919|<dedupe_key>`;
3. sort ascending by hash score, then original selection rank;
4. take 5 records per stratum;
5. assign stable IDs `V201`–`V230`.

This is a validation-set construction rule, not an estimate of OCI prevalence.

## Blinding boundary

The frozen sample manifest contains bibliographic selection metadata only. It is **not yet an A2/B2 coding packet**.

Before independent coding:
- materialize identical evidence packets for all 30 records;
- remove prior Pilot 0 labels/adjudication material;
- attach the frozen v2 coding form;
- freeze A2 and B2 input packet hashes separately;
- do not compare labels until both completed coder files are frozen.

## Canonical artifacts

- `data/v2_validation_sample_manifest.csv`
- `process/V2_VALIDATION_SAMPLE_FREEZE.json`
- `code/draw_v2_validation_sample.py`
- `process/SCHEMA_V2_FROZEN.md`

Next gate: evidence-packet materialization and genuinely independent A2/B2 coding.
