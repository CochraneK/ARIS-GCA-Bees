# Status

## State

**INITIAL DESIGN + AGENT SKELETON**

Date: 2026-09-18

## Completed

- [x] separated 014 from 011 while explicitly inheriting 011 forensic architecture;
- [x] defined OpenIntegrity as a public-data integrity-triage agent;
- [x] froze the principle that anomalies are not corruption findings;
- [x] defined Track A temporally blind screening and Track B open-world triage;
- [x] defined first-pass canonical entities and evidence graph;
- [x] identified initial public-data backbone;
- [x] drafted detector families;
- [x] drafted entity-resolution and temporal-leakage rules;
- [x] created initial executable core contract.

## Current maturity estimate

**~22%**

This percentage means the conceptual architecture is usable, but real source adapters, Pilot 0 fixtures, benchmark cases, calibration, and manuscript work remain.

## Immediate next work

1. build synthetic Pilot 0 fixtures and tests;
2. implement OCDS normalized importer;
3. implement at least one official procurement adapter;
4. implement corporate/beneficial-ownership join;
5. add entity-resolution scorer with explicit abstention;
6. freeze detector taxonomy after Pilot 0;
7. create benchmark-case registry with source-time cutoffs;
8. run independent shortcut/leakage audit.

## Hard blockers

None at design level.

Real-data Pilot 1 depends on source-specific joins and rate/access constraints, not on new conceptual decisions from the user.
