# Status

## State

**PILOT 0 CORE PASSED / SOURCE-ADAPTER PHASE**

Date: 2026-09-18

## Completed

- [x] separated 014 from 011 while explicitly inheriting 011 forensic architecture;
- [x] defined OpenIntegrity as a public-data integrity-triage agent;
- [x] froze the principle that anomalies are not corruption findings;
- [x] defined Track A temporally blind screening and Track B open-world triage;
- [x] defined first-pass canonical entities and evidence graph;
- [x] identified initial public-data backbone;
- [x] drafted 11 detector families;
- [x] drafted entity-resolution and temporal-leakage rules;
- [x] created initial executable core contract;
- [x] implemented deterministic Pilot 0 detectors for single-bidder, threshold proximity, newly incorporated suppliers, in-force debarment, and public-office/ownership links;
- [x] implemented PASS / FLAG / ABSTAIN / ERROR semantics;
- [x] hard-coded detector and report-level corruption_inference = false;
- [x] added tests for name-only collision abstention and future-outcome leakage;
- [x] added GitHub Actions CI;
- [x] Pilot 0 core CI passed on 2026-09-18 (workflow run 35304088390).

## Current maturity estimate

**~28%**

The project has moved beyond a concept-only design: the core detector contract, evidence semantics, review-priority logic, temporal safeguards, and initial synthetic invariants execute successfully in CI. Real public-data adapters, richer synthetic fixtures, benchmark cases, calibration, and manuscript work remain.

## Immediate next work

1. implement OCDS normalized importer and fixture corpus;
2. implement at least one official procurement adapter (TED, USAspending, or a joinable OCDS publisher);
3. implement Companies House / BODS-compatible corporate and beneficial-ownership joins;
4. add an explicit entity-resolution scorer with calibrated abstention;
5. expand Pilot 0 to split-contract, supplier concentration, shared-address competitor, benign-offshore, and dependency-group cases;
6. freeze detector taxonomy after expanded Pilot 0;
7. create benchmark-case registry with source-time cutoffs;
8. run independent shortcut/leakage audit;
9. construct real-data Pilot 1.

## Hard blockers

None at design or executable-core level.

Real-data Pilot 1 depends on source-specific joins, historical snapshots, and rate/access constraints, not on new conceptual decisions from the user.
