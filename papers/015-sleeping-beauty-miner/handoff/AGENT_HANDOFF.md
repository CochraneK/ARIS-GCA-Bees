# ARIS4C015 · Agent takeover brief

## What this project is

**Sleeping Beauty Miner: An Integrity-Aware, Time-Safe Agent for Discovering Delayed and Under-Recognized Scientific Work**

An open-data-first Sleeping Beauty discovery agent with three separated tracks: retrospective robust-SB identification, case-enriched mechanism analysis, and time-safe prospective rediscovery. Track M now uses a frozen three-paper literature-known primary case set, standard event-time incidence-density risk-set semantics, deterministic multi-seed control acquisition, and offline artifact reanalysis. A 603-paper/200-controls-per-known-case acquisition shows full match coverage but persistent observed-covariate imbalance; frozen-case 1:1 max abs SMD is 1.633 and 1:4 worsens to 2.417. Common-support diagnostics isolate the 1921 Washburn stratum as the clearest overlap problem. Mechanism inference remains blocked until complete-frame overlap is assessed and OpenAlex Beauty-Coefficient trajectories are independently calibrated.

## Current state

- Activity: **active**
- Progress: **88%**
- Stage: **Track M · frozen-case common-support gate**
- Evidence: 603-paper deterministic multi-seed acquisition + frozen 3 literature-known primary cases + standard risk-set control reuse + offline reanalysis; 1:1 match rate 1.0 but max abs SMD 1.633; 1:4 worsens to 2.417; Washburn-1921 minimum observed sleep-rate gap 1.180; latest design tests/CI PASS

## Immediate next action

**Enumerate the complete same-field/same-year control frame for the 3 known cases without relaxing SMD<0.10; if overlap still fails, freeze an overlap-limited estimand/unmatched-case rule; independently validate OpenAlex trajectory/B against SciSciNet-v2 or another source**

## Current blocker / gate

Primary risk-set common support remains inadequate, especially Washburn 1921; OpenAlex API live acquisition hit its current rate limit; OpenAlex Beauty-Coefficient calibration remains provisional

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
