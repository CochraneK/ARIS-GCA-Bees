# ARIS4C007 · Agent takeover brief

## What this project is

**Are Animal Years Comparable? Benchmarking Cross-Species Biological Age Equivalence Across Mammals**

A multi-axis benchmark of cross-species age equivalence. Pilot 0 life-history mappings, Pilot 1 independent demography, Pilot 2 held-out homologous events, Pilot 3A universal-clock implementation parity, and Pilot 3B metadata/holdout selection are complete. Pilot 3C is validating a 10-sample/6-species independent raw-IDAT SeSAMe→Universal Clock 2/3 smoke before automatic expansion to the frozen 50-sample non-training holdout.

## Current state

- Activity: **active**
- Progress: **78%**
- Stage: **Pilot 3C · clock-era preprocessing replication gate**
- Evidence: Pilot0 785 mappings + Pilot1 88-species demography + Pilot2 945 held-out events + Pilot3A MMC v3.0.0 parity PASS + Pilot3B frozen 50-sample/6-species pan-clock-training=no holdout. Modern SeSAMe SHCDPB 10-sample smoke resolved IDAT/CRLF/probe-ID layers: Clock2/3 required probe names are 100% present; species-nonmapping 0.5 convention raises usable coverage, but residual QC-missing leaves minimum final coverage 0.8971 / 0.8895, below the frozen 0.95 gate.

## Immediate next action

**Run the same frozen 10-sample set under the 2023 clock-era stack (R 4.3 / Bioconductor 3.17 / SeSAMe 1.18.4 / SHCDPM). If >=95% Clock2/3 input coverage passes, run the frozen 50-sample holdout under the same clock-era preprocessing; preserve modern SHCDPB as a sensitivity/QC route.**

## Current blocker / gate

Method replication gate, not download engineering: modern SHCDPB preprocessing does not reproduce >=95% clock-input coverage for all frozen samples. Clock-era SeSAMe 1.18.4/SHCDPM workflow is implemented and queued; the 0.95 threshold remains unchanged.

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
