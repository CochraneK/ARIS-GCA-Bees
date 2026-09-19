# ARIS4C011 · Agent takeover brief

## What this project is

**Research Forensics at Scale: An Auditable Multi-Evidence Framework for Scientific Integrity Screening**

A cross-disciplinary, auditable framework that routes scientific manuscripts to applicability-aware statistical, numerical, textual, image, citation, provenance, registration, metadata, and corpus-network checks, then fuses findings as an evidence graph for human review without equating anomalies with misconduct.

## Current state

- Activity: **wait**
- Progress: **72%**
- Stage: **Pilot 3 · object-level historical table qualification**
- Evidence: Priority PLOS case has frozen pre-correction t001 wrapper provenance; table-image object qualification is now separated from F3 value extraction

## Immediate next action

**Qualify archived Table-1 image object as SAFE_EXACT, then run F3 content extraction**

## Current blocker / gate

Historical table image replay/qualification remains the object-level gate

## Canonical files / entry points

- **paper.json:** paper.json
- **process/status or plan:** process/RESEARCH_PLAN.md
- **English paper:** manuscript/DRAFT.md
- **source:** https://github.com/CochraneK/ARIS4C/tree/main/papers/011-research-forensics

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
