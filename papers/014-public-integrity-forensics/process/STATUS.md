# Status

## State

**PILOT 1A UK SOURCE FEASIBILITY FROZEN / AGENT CORE + EVIDENCE GRAPH READY / OWNERSHIP ENRICHMENT NEXT**

Date: 2026-09-18

## Completed

- [x] separated 014 from 011 while explicitly inheriting 011 forensic architecture;
- [x] defined OpenIntegrity as a public-data integrity-triage agent;
- [x] froze the principle that anomalies are review leads, not corruption findings;
- [x] defined Track A temporally blind screening and Track B open-world triage;
- [x] defined canonical entities, source coverage, temporal semantics, and evidence graph;
- [x] defined 11 detector families and E0-E5 evidence semantics;
- [x] implemented PASS / FLAG / ABSTAIN / ERROR semantics;
- [x] hard-coded detector and report-level corruption_inference = false;
- [x] implemented single-case detectors for single bidder, threshold proximity, newly incorporated supplier, in-force debarment, and public-office/ownership links;
- [x] implemented cross-contract detectors for configured split-award patterns, supplier concentration, and shared-address bidders;
- [x] added benign-offshore and name-collision negative controls;
- [x] implemented conservative entity resolution with stable-ID, official-cross-ID, multi-attribute, possible, abstain, and conflict states;
- [x] implemented explicit source_coverage semantics so missing source families ABSTAIN rather than PASS;
- [x] implemented OCDS release and lifecycle-record normalization, including legacy list-shaped record responses;
- [x] implemented Companies House company-profile / PSC normalization;
- [x] implemented USAspending award normalization;
- [x] implemented explicit procurement -> company -> beneficial owner -> public-office cross-source joins;
- [x] implemented dated debarment enrichment with explicit identity proof and source-scan coverage semantics;
- [x] rejected name-only cross-source person/company/debarment joins from high-priority evidence;
- [x] implemented immutable-style raw source snapshots with SHA-256 plus Track A publication-time gates;
- [x] implemented a descriptive Evidence Graph and standard report builder;
- [x] report finding IDs and graph finding IDs are now canonical and identical;
- [x] created the formal portable Agent Skill at agent/public-integrity-forensics/SKILL.md;
- [x] created machine-readable finding and report JSON Schemas;
- [x] created a benchmark-case registry schema with source cutoff, outcome classes, matching strata, and leakage audit;
- [x] locked a UK identifier-first Pilot 1 protocol;
- [x] completed live USAspending, Find a Tender, FTS lifecycle, and Contracts Finder engineering smokes;
- [x] froze UK Pilot 1A collection window at 2026-09-01T00:00:00Z to 2026-09-17T23:59:59Z;
- [x] completed frozen Pilot 1A public-source collection;
- [x] preserved raw release packages and per-release SHA-256 manifest in workflow artifact;
- [x] all current OpenIntegrity tests, Agent Skill validation, and JSON Schema validation pass in CI.

## Pilot 1A frozen result

Canonical result record: `process/PILOT1_RESULTS.md`.

Frozen collection workflow: **35305663110**  
Artifact: `aris4c014-pilot1-uk-p1a-v0`  
Artifact digest: `sha256:400d7843872a75271ba13d7da8df38d0d4af0fa886962c56289e67c16b982473`

Fixed bounded collection:

- Find a Tender: 100 releases -> 119 award cases -> 32 direct `GB-COH` join candidates (26.9%);
- Contracts Finder: 100 releases -> 104 award cases -> 57 direct `GB-COH` join candidates (54.8%);
- raw total: 223 award cases, 89 direct company-identifier join candidates;
- competition-covered award cases: 0.

The raw total is not de-duplicated across sources and the percentages are not population estimates.

The zero competition coverage is treated as a source limitation. Single-bidder/competition checks remain ABSTAIN rather than being imputed.

## Current maturity estimate

**~55%**

OpenIntegrity now has:

- a tested forensic core;
- formal Agent Skill;
- source adapters;
- conservative entity resolution;
- explicit source-coverage semantics;
- cross-source enrichment contracts;
- debarment enrichment;
- temporal leakage controls;
- snapshot hashing;
- Evidence Graph and report builder;
- a frozen real-data UK Pilot 1A procurement artifact.

The main missing empirical layer is authenticated corporate/beneficial-ownership enrichment of the identifier-first subset, followed by calibration, historical outcome cases, independent review, and manuscript/results work.

## Immediate next work

1. enrich the 89 direct `GB-COH` candidate cases with Companies House company profiles and PSC/control records using authenticated API access;
2. preserve retrieved_at, notified_on/ceased_on, raw checksum, parser version, and source IDs for each ownership record;
3. run newly-incorporated-supplier and ownership-graph detectors only where their data are actually covered;
4. add a vetted public-office source adapter with occupancy intervals and conservative identity resolution;
5. add an official/approved debarment-source ingestion adapter without relying on undocumented dynamic endpoints;
6. de-duplicate FTS/Contracts Finder procurement overlap by OCID/award identity before any prevalence/yield statistic;
7. construct historical Track A benchmark cases with outcome-independent source cutoffs;
8. calibrate supplier concentration and other E4 signals against relevant reference populations;
9. run an independent shortcut, temporal-leakage, entity-resolution, and defamation-language audit;
10. begin manuscript methods/results after enriched Pilot 1 is reproducible.

## Hard blockers

No blocker remains for the architecture, Agent Skill, public procurement collection, Evidence Graph, or frozen Pilot 1A source feasibility.

**Current external dependency:** live Companies House Public Data API enrichment requires authenticated API access. The key must be provided through secure runtime configuration; it must not be committed to the repository.

Until authenticated ownership enrichment is available, missing ownership/PSC data remain ABSTAIN and cannot be treated as evidence of absence.
