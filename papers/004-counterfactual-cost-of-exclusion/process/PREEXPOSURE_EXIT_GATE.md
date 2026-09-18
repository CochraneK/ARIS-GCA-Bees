# PRE-EXPOSURE EXIT GATE — ARIS4C004

Date frozen: 2026-09-18

## Purpose

Prevent the ARIS4C004 feasibility stage from expanding indefinitely.

Once the conditions below are met, the project must stop adding new identity/network infrastructure and advance to mental-health exposure coding under the already frozen `EXPOSURE_CODEBOOK.md`.

## Required conditions

### 1. Full frozen 100-person frame has an identity state

Every candidate in `science_candidates_frozen.csv` must be in one of:

- `VERIFIED_SINGLE`
- `VERIFIED_CLUSTER`
- `NO_GRAPH_RECORD`
- `AMBIGUOUS_COLLISION`
- `EXCLUDED_IDENTITY_ERROR`

No `PROVISIONAL_*` state may remain in the pre-exposure freeze.

### 2. Positive identity mappings are auditable

Every VERIFIED person must have:

- explicit OpenAlex Author ID set;
- canonical-frame person metadata match;
- sufficient bibliographic/authority evidence under `IDENTITY_CODEBOOK.md`;
- provenance to the review packet;
- no unresolved conflicting strong identifier.

### 3. Required second review is complete

Before exposure coding:

- all `VERIFIED_CLUSTER` cases are independently second-reviewed;
- all collision/error cases selected by protocol are second-reviewed;
- the deterministic 25% `VERIFIED_SINGLE` audit is completed or, if operationally staged, enough of it is completed to quantify identity error before confirmatory analysis;
- disagreements are adjudicated.

### 4. Work/network release state exists for every VERIFIED person

Each VERIFIED person must have one of:

- `network_observable=true` with a clean work corpus;
- a documented pre-exposure reason for remaining network-unobservable.

Held cases must not be released by raw OpenAlex `works_count` alone.

### 5. Network observability is characterized

The frozen 100-person frame must report observability by:

- birth cohort;
- visibility stratum;
- region;
- gender;
- FORD broad field;
- source subdomain.

Citation-layer status must be one of:

- citation-rich;
- citation-sparse;
- no-downstream;
- network-unobservable.

### 6. Domain stratification is usable

Every candidate should have either:

- a defensible FORD broad field; or
- explicit `unclassified` status.

Unclassified cases may remain in the frame. They must not be guessed into a field to improve balance.

### 7. No unresolved critical data-integrity blocker

CI must pass for:

- canonical-frame identity joins;
- CSV structural validity;
- work-decision invariants;
- clean-network temporal rules;
- deterministic review sampling.

Known limitations may remain if documented; silent corruption may not.

## Explicit non-requirements

The project does **not** need, before exposure coding:

- 95% OpenAlex coverage;
- every candidate to be network-observable;
- every focal person to be citation-rich;
- a complete second-hop knowledge graph;
- final CPE simulation parameters;
- humanities/arts-specific influence extraction beyond what is needed to classify current network observability.

Those tasks are either later-stage or sensitivity work.

## Exit action

When Conditions 1–7 are satisfied:

1. write `PREEXPOSURE_FRAME_FREEZE.md`;
2. hash/version the identity, work, FORD and network-decision tables;
3. update `STATUS.md` from `pre-exposure scale-up` to `exposure-coding`;
4. apply `EXPOSURE_CODEBOOK.md` without altering the frozen inclusion rules;
5. estimate A1/A2/B1/B2/C/U yield;
6. only then decide whether the final candidate sample must expand beyond 100.

## Expansion beyond 100

Do **not** automatically expand beyond 100 merely because some candidates are unobservable.

Expansion is justified only after the 100-person pre-exposure frame is frozen and exposure yield is measured.

The decision should be driven by the number/precision of analyzable exposed and comparison cases, not by a desire to make OpenAlex coverage look high.
