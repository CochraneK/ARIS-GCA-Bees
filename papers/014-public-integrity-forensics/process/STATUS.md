# Status

## State

**PILOT 0 EXPANDED / LIVE PUBLIC-SOURCE SMOKE PASSED / AGENT SKILL READY / PILOT 1 ASSEMBLY**

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
- [x] implemented OCDS 1.1.x normalization;
- [x] implemented Companies House company-profile / PSC normalization;
- [x] implemented USAspending award normalization;
- [x] implemented explicit procurement -> company -> beneficial owner -> public-office cross-source joins;
- [x] rejected name-only cross-source person joins from high-priority evidence;
- [x] ran a live USAspending public-source smoke test and preserved output as a workflow artifact;
- [x] confirmed live award-only records cause uncovered detector families to ABSTAIN rather than emit false negative PASS results;
- [x] created the formal portable Agent Skill at agent/public-integrity-forensics/SKILL.md;
- [x] created machine-readable finding and report JSON Schemas;
- [x] created a benchmark-case registry schema with source cutoff, outcome classes, matching strata, and leakage audit;
- [x] added a synthetic Track A registry fixture demonstrating post-cutoff outcome exclusion;
- [x] integrated pytest, skill metadata validation, and JSON Schema validation into CI;
- [x] final expanded Pilot 0 / skill / benchmark CI passed on 2026-09-18 (workflow run 35304992483).

## Live-source milestone

USAspending live smoke workflow: 35304795418.

The live query returned three public award records. The adapter preserved stable UEIs and federal agency identifiers where available. Because those rows only supplied procurement-award coverage, the current competition, threshold, incorporation, debarment, and public-office/ownership checks correctly returned ABSTAIN rather than pretending that missing sources were negative evidence. No automated corruption inference was produced.

## Current maturity estimate

**~45%**

The project now has a reproducible executable core, expanded synthetic Pilot 0, three source-normalization surfaces, conservative entity resolution, explicit cross-source joining, a live public-source smoke test, a portable Agent Skill, benchmark registry semantics, and green CI.

The remaining work is dominated by real multi-source Pilot 1 construction, historical snapshots, additional source adapters, calibration/reference populations, benchmark annotation, independent review, and manuscript/results work.

## Immediate next work

1. select and assemble the first real multi-source Pilot 1 jurisdiction, prioritizing identifier joinability and historical source quality rather than perceived corruption prevalence;
2. add an official debarment/sanctions adapter with historical validity dates;
3. add a public-office/PEP source adapter that preserves office-occupancy intervals and identity provenance;
4. build a historical snapshot/cache layer with first_public_at, valid_from, valid_to, retrieved_at, checksum, and parser version;
5. add procurement-document and bidder-network ingestion where public records permit;
6. calibrate supplier concentration / price / graph anomalies against sector, value band, procurement method, and data completeness;
7. populate the real benchmark registry with concluded public cases plus matched no-known-adverse-finding comparators;
8. perform an independent shortcut, temporal-leakage, and identity-resolution audit;
9. freeze the v1 detector taxonomy and priority policy after Pilot 1;
10. begin manuscript methods/results once a preregistered real-data Pilot 1 is reproducible.

## Hard blockers

None at the architecture, Agent Skill, synthetic Pilot 0, or public procurement ingestion level.

The main practical dependencies are access/rate constraints for specific registries, availability of historical ownership/public-office snapshots, and reliable cross-source identifiers. These should produce ABSTAIN or source-specific limitations rather than silent imputation.
