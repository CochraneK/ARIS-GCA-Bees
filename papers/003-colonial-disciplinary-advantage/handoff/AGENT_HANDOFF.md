# ARIS4C003 · Agent takeover brief

## What this project is

**Colonial Legacies and the Global Geography of Disciplinary Advantage**

A locked, outcome-unblinded cross-national and cross-disciplinary test of whether historical colonial exposure interacts with independently coded discipline-level imperial/colonial knowledge entanglement to predict contemporary scientific output, normalized impact, and former-colonial collaboration networks.

## Current state

- Activity: **active**
- Progress: **78%**
- Stage: **Confirmatory model execution · FIRST_RESULT_LOCK gate**
- Evidence: Outcome materialization PASS under DESIGN_LOCKED/OUTCOME_UNLOCKED: exact 32-way country + dyad aggregation, design_changed=false, no modern effects inspected; zero-filled country panel 15,540 rows / 148 countries / 21 concepts / 5 periods and dyad panel 1,269,450 rows / 12,090 pairs / 21 concepts / 5 periods; distributed confirmatory models are now running

## Immediate next action

**Complete core PPML, D01–D21 LOO and 3×999 fixed-seed IKES permutations; aggregate components and create FIRST_RESULT_LOCK.json before any human interpretation of headline coefficients**

## Current blocker / gate

No current engineering blocker; confirmatory model matrix is executing. Interpretation remains procedurally blocked until FIRST_RESULT_LOCK.json exists.

## Canonical files / entry points

- **paper.json:** paper.json
- **process/status or plan:** process/RESEARCH_PLAN.md
- **source:** https://github.com/CochraneK/ARIS4C/tree/main/papers/003-colonial-disciplinary-advantage

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
