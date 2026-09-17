# PILOT RESULTS — ARIS4C004

Last updated: 2026-09-18

This file is the canonical record of **pre-exposure science-pilot results**. No mental-health evidence was used to select or resolve candidates in these runs.

## Pilot purpose

Before coding any mental-health exposure, test whether a mental-health-independent historical science candidate frame can be linked to a sufficiently reproducible scholarly network.

The pilot is deliberately staged:

1. candidate-frame construction;
2. identity-resolution leads;
3. OpenAlex author/work observability;
4. author-fragment / name-collision review;
5. only after a network analytic frame is frozen: mental-health evidence coding.

## Candidate-frame result

Source: Laouenan et al. cross-verified notable-people dataset, verified mirror SHA-256:

`fe44aa6f97cf9f6c12d040137f92a9f4d0fd1f50e28f7f5d80eeae29b487828d`

Eligibility filter produced **108,626 Discovery/Science candidates** before pilot sampling.

The pilot sampled **100 candidates** with fixed seed `20260918`, balanced across 20 birth-cohort × visibility strata: 5 candidates per stratum.

### Sample composition

- Europe: 68
- America: 22
- Asia: 7
- Africa: 1
- missing region: 2
- Academia: 92
- Explorer/Inventor/Developer: 8

Interpretation: deterministic stratification by cohort × visibility worked, but the source frame remains heavily Europe-weighted. This is a property to measure and potentially re-stratify, not evidence that the historical contributor population was actually distributed this way.

## Identifier-lead result

For the 100 frozen candidates:

- Wikidata QID: 100/100
- ORCID lead found through Wikidata: 1/100
- OpenAlex author-ID lead found through Wikidata: 0/100

Conclusion: **Wikidata external identifiers are insufficient as the primary historical person → OpenAlex bridge.** The project must solve entity resolution rather than rely on identifier joins.

## OpenAlex pilot evolution

### Pilot v1 — identifier-only

The initial resolver required an existing OpenAlex ID or ORCID.

Result on first 30 candidates:

- resolved: 0/30
- resolution rate: 0%

Interpretation: design failure of the resolver, not evidence that OpenAlex lacks historical records.

Corrective action: add conservative name search plus lifetime/publication plausibility scoring while preserving unresolved/ambiguous states.

### Pilot v2 — evidence-scored name resolution

GitHub Actions run: `35272905327`

First 30 frozen candidates:

- automatically accepted top records: 17/30 = **56.7%**
- ambiguous: 1/30
- unresolved: 12/30
- accepted candidates with at least one work in 1900–2000: 14/30 = **46.7%**
- works acquired: 306
- API key: none / keyless pilot

This demonstrated that OpenAlex contains usable records for a substantial subset, but audit inspection identified two major problems:

1. some source names were mojibaked by a global Latin-1 decode;
2. one historical person is often split across multiple OpenAlex Author IDs.

Examples found during audit included James S. Albus, Erika Greber, Ottomar Rosenbach, Fritz Strassmann, Hilario Hernández Gurruchaga, and others with multiple highly similar OpenAlex author records. These examples are identity-resolution diagnostics only; they have no mental-health role in the study.

### Encoding correction

A strict UTF-8 decode of the 250MB source mirror failed, showing that the file is not clean global UTF-8. The pipeline now:

1. decodes bytes losslessly as Latin-1;
2. performs **cell-level reversible UTF-8 mojibake repair** only where the Latin-1 text round-trips as UTF-8;
3. leaves genuine Latin-1 strings unchanged when repair is invalid.

Regression examples:

- `HernÃ¡ndez` → `Hernández`
- genuine `Föhl` remains `Föhl`

No `errors=ignore` decoding is used.

### Pilot v3 — repaired names

GitHub Actions run: `35273279428`

First 30 frozen candidates:

- automatically accepted top records: 19/30 = **63.3%**
- ambiguous: 1/30
- unresolved: 10/30
- accepted candidates with at least one work in 1900–2000: 15/30 = **50.0%**
- works acquired: 311
- resolver errors: 0

The encoding repair therefore improved apparent automatic resolution from 56.7% to 63.3% and observed-work coverage from 46.7% to 50.0% in this bounded pilot.

**Important:** these numbers are not final identity accuracy because OpenAlex fragmentation can make a high-scoring top hit incomplete or misleading.

## Identity-resolution correction: coverage ≠ precision

The original feasibility gate "95% of sampled candidates resolve" was too coarse. Two distinct quantities are now required.

### Candidate-frame network coverage

Question:

> What fraction of a mental-health-independent historical candidate frame has enough scholarly-network information to support the planned analysis?

This quantity can legitimately be below 95%, but missingness must be characterized by era, region, visibility, discipline, gender, and other available frame variables.

Current bounded estimate from the first 30 candidates, using accepted single top records only: **50% had at least one acquired 1900–2000 work**.

This is a provisional lower-ish operational estimate because fragmented author records are not yet clustered.

### Analytic-frame identity precision

Question:

> For people who enter the final network analytic frame, how certain are we that all included OpenAlex records belong to the intended historical person and that important fragments have not been omitted?

Target:

- **near-100% externally auditable identity decisions for the final analytic frame**;
- no automatic top-hit acceptance is considered final verification;
- multiple plausible OpenAlex IDs trigger cluster review rather than silent top-hit selection;
- conflicting ORCIDs or other strong identity evidence prohibit blind merging.

This precision gate is more important than maximizing raw candidate-frame coverage.

## OpenAlex fragmentation review

A dedicated script now converts the raw search audit into an `identity_review_queue.csv` and classifies candidates as:

- `no_openalex_search_hit`
- `single_plausible_author_record`
- `single_low_confidence_record`
- `possible_author_fragmentation`
- `possible_name_collision_conflicting_orcid`
- `name_collision_or_low_similarity`

All rows begin with `identity_verified=false`.

GitHub Actions run `35273825936` is the first real-data pilot including this explicit fragmentation stage. Its result should be appended here once completed.

## Current science feasibility interpretation

**Continue.** The science route has passed the minimal "data exist and can be programmatically connected" test, but has **not** passed the final identity/network analytic-frame gate.

The major bottleneck has shifted from general data availability to:

1. historical person ↔ OpenAlex author-cluster validation;
2. selection bias induced by OpenAlex observability;
3. network sufficiency after verified clusters are assembled;
4. only then, Tier-A/Tier-B mental-health evidence yield.

## Revised order of operations

1. Finish author-fragment review on the first 30.
2. Define external/manual identity-validation rules.
3. Estimate coverage and fragmentation by cohort/visibility/region.
4. Expand identity pilot beyond 30 only after precision rules are stable.
5. Freeze a **network-observable analytic frame without using mental-health information**.
6. Begin exposure coding under `EXPOSURE_CODEBOOK.md`.
7. Measure Tier-A/Tier-B yield.
8. Decide final sample expansion and simulation-based precision target.

No mental-health outcome or CPE comparison should be run before step 5–6 is frozen.
