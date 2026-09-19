# ARIS4C007 · Agent takeover brief

## What this project is

**Are Animal Years Comparable? Benchmarking Cross-Species Biological Age Equivalence Across Mammals**

A multi-axis benchmark of cross-species age equivalence. Pilot 0 life-history mappings, Pilot 1 independent demography, Pilot 2 held-out homologous events, Pilot 3A universal-clock implementation parity, and Pilot 3B metadata/holdout selection are complete. Pilot 3C is validating a 10-sample/6-species independent raw-IDAT SeSAMe→Universal Clock 2/3 smoke before automatic expansion to the frozen 50-sample non-training holdout.

## Current state

- Activity: **active**
- Progress: **76%**
- Stage: **Pilot 3C · independent raw-IDAT molecular smoke**
- Evidence: Pilot0 785 mappings + Pilot1 88-species demography + Pilot2 945 held-out events + Pilot3A MMC v3.0.0 parity PASS + Pilot3B frozen 50-sample/6-species pan-clock-training=no holdout

## Immediate next action

**Pass 10-sample/6-species SeSAMe SHCDPB Clock2/3 smoke at >=95% CpG coverage, then auto-run frozen 50-sample full holdout**

## Current blocker / gate

Engineering only: latest failed smoke downloaded all 20 IDATs but CRLF in download_manifest.tsv polluted Bash filenames; fix is committed and rerun 35433019496 is in progress

## Canonical files / entry points

- **paper.json:** paper.json
- **process/status or plan:** process/RESEARCH_PLAN.md
- **source:** https://github.com/CochraneK/ARIS4C/tree/main/papers/007-cross-species-age-equivalence

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
