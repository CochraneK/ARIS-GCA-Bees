# STATUS · ARIS4C013

**Project:** Born to Die? Birth–Death Temporal Coupling  
**Stage:** empirical feasibility / administrative-data acquisition  
**Date:** 2026-09-18

## Completed
- [x] Promoted to ARIS4C slot 013.
- [x] Defined environment → birthday → culture → traditional-calendar hypothesis ladder.
- [x] Seeded birthday-effect and month-of-birth literature.
- [x] Captured the 1993 Chinese-American claim and 2006 failed replication.
- [x] Added multiple-testing, pseudo-calendar and matched-complexity safeguards.
- [x] Distinguished date-only traditional-calendar testing from full Bazi.
- [x] Audited NBER/NVSS 1988 layout: death month/day are present, exact birth day is not; paired exact-date Pilot is **blocked** on this source.
- [x] Ran Wikidata Pilot 0A on 2,953,301 biographies.
- [x] Demonstrated a major precision artifact: 23.9% of eligible births and 24.7% of deaths were recorded on Jan 1; 336,356 records had Jan 1 for both.
- [x] Identified BUNMD/Numident as the primary public administrative source with exact birth and death day fields.

## Pilot 0A result
The naive same-month/day observed/expected ratio was 2.6768. This is **not evidence of a birthday or astrological effect** because the source is dominated by low-precision date heaping. Excluding all records with day-of-month 1 reduced the ratio to 1.8250 but did not remove the anomaly, so further precision filtering is required.

Interpretation: Pilot 0A successfully stress-tested the pipeline and showed why precision metadata and administrative imputation controls are mandatory.

## Open gates
- **A — BUNMD acquisition:** identify the current Harvard Dataverse file IDs and practical download route.
- **B — BUNMD precision audit:** quantify day=1/day=15 imputation and define a frozen clean-date rule before coupling tests.
- **C — Administrative Pilot 1:** run birthday-window/circular-phase analyses in the 1988–2005 high-coverage Numident window.
- **D — Feature freeze:** source and lock deterministic traditional-calendar features before any confirmatory H4 analysis.
- **E — Temporal/geographic replication:** reserve untouched years/regions and seek an independent country/registry.
- **F — Exact-precision Wikidata sensitivity:** optional re-extraction preserving Wikidata timePrecision; Pilot 0A alone is not confirmatory.

## Claim ceiling
**No current claim that astrology or Bazi predicts mortality.**

Current justified claim: apparent birth–death coupling can be extremely large when date precision is mishandled; the hypothesis remains testable using administrative data with explicit date-day fields and prespecified imputation controls.

## Immediate next action
Probe the current BUNMD Harvard Dataverse release, then build the administrative Pilot 1 around the published byear/bmonth/bday/dyear/dmonth/dday fields.
