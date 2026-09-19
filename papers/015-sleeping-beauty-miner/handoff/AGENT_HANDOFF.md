# ARIS4C015 · Agent takeover brief

## What this project is

**Sleeping Beauty Miner: An Integrity-Aware, Time-Safe Agent for Discovering Delayed and Under-Recognized Scientific Work**

An open-data-first Sleeping Beauty discovery agent with three separated tracks: robust retrospective SB identification, case-enriched matched-control mechanism analysis, and time-safe prospective rediscovery. Pilot 1 currently includes 200 random historical papers across 10 field/era/seed strata, multiple delayed-recognition outcomes, citation baselines, seed/recognition-floor sensitivity, and a negative lexical-novelty ablation. Mechanism infrastructure now blocks inference when no robust SB cases exist.

## Current state

- Activity: **active**
- Progress: **83%**
- Stage: **Track M · case-definition harmonization rerun**
- Evidence: Track A: 13 retrospective robust-gate candidates/150. Artifact audit found some have high early-attention percentiles; canonical SB now requires robust gate + early-low + late-high versus unselected field/year reference.

## Immediate next action

**Complete corrected canonical-state rerun; only then assess control-support expansion**

## Current blocker / gate

Absolute robust gate and cohort-relative mechanism state must agree before substantive matching

## Canonical files / entry points

- **paper.json:** paper.json
- **process/status or plan:** process/RESEARCH_PLAN.md
- **source:** https://github.com/CochraneK/ARIS4C/tree/main/papers/015-sleeping-beauty-miner

## Before changing anything

1. Read `TODO.md`, `DECISIONS.md`, and the newest entries in `CHATLOG.md` and `SESSION_LOG.md`.
2. Preserve frozen/preregistered design decisions unless the repository explicitly records an authorized amendment.
3. Do not broaden claims beyond the evidence state recorded in the manuscript/process files.
4. Use **Cochrane Kang** for visible author naming.
5. Do not commit secrets, private credentials, hidden chain-of-thought, or unnecessary sensitive personal data.
6. After a material change, update canonical research files first, then continuity files.

## Handoff completion rule

Before ending a substantial session:
- update `TODO.md`;
- append any material research decision to `DECISIONS.md`;
- append a public-safe conversation summary to `CHATLOG.md`;
- append what was executed/validated to `SESSION_LOG.md`.
