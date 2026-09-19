# ARIS4C014 · Agent takeover brief

## What this project is

**Public Integrity Forensics: An Auditable Multi-Source Agent for Corruption-Risk Screening from Open Data**

An auditable multi-source public-integrity agent that mines structured and web-native public records across government, hospitals, SOEs, research institutes, universities, NGOs/social organizations and suppliers, builds a time-aware evidence graph, and produces reproducible human-review leads without equating anomalies, public-office status, organizational identity or web allegations with corruption.

## Current state

- Activity: **wait**
- Progress: **69%**
- Stage: **China Pilot 1 · conservative cross-source entity layer**
- Evidence: CCGP/CAS/USCC live graph + stable-ID-only auto-merge resolver under CI

## Immediate next action

**Run cross-source enrichment with exact stable IDs; route name-only matches to review**

## Current blocker / gate

Authoritative stable identifiers and source coverage vary by organization type

## Canonical files / entry points

- **paper.json:** paper.json
- **process/status or plan:** process/RESEARCH_PLAN.md
- **source:** https://github.com/CochraneK/ARIS4C/tree/main/papers/014-public-integrity-forensics

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
