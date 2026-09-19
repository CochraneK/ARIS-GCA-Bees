# ARIS4C014 · Agent takeover brief

## What this project is

**Public Integrity Forensics: An Auditable Multi-Source Agent for Corruption-Risk Screening from Open Data**

ARIS4C014 is the scientific parent of **OpenIntegrity**, an evidence-first, auditable public-integrity agent for multi-source open-data screening and human review.

## Current state

- Activity: **wait / ready for next implementation session**
- Portfolio progress: **69%**
- Scientific stage: **China Pilot 1 · conservative cross-source entity layer**
- Proven evidence: CCGP/CAS/USCC live pipeline + final-vs-candidate semantics + stable-ID-only cross-source identity rules under CI
- New architecture decision: split reusable implementation into a standalone **OpenIntegrity** repository; keep ARIS4C014 as the scientific parent; keep **repo-auditor** independent.
- New institution decision: model China organizations with **legal/organizational identity × functional domain**, not one flat institution list.

## Immediate next action

**Bootstrap standalone OpenIntegrity from the working ARIS4C014 implementation, verify CI parity, then continue exact-stable-ID cross-source enrichment.**

Do not delete working code from ARIS4C014 until the extracted repository passes parity tests.

## Current blocker / gate

Authoritative stable identifiers and source coverage vary by organization type. Treat unavailable/interactive sources as coverage gaps and do not bypass CAPTCHAs, authentication or anti-automation controls.

## Canonical files / entry points

- `paper.json`
- `process/STATUS.md`
- `process/CHINA_PILOT0_RESULTS.md`
- `process/CHINA_INSTITUTION_ONTOLOGY.md`
- `process/REPOSITORY_ARCHITECTURE.md`
- `handoff/TODO.md`
- `handoff/DECISIONS.md`
- source: https://github.com/CochraneK/ARIS4C/tree/main/papers/014-public-integrity-forensics

## Non-negotiable safeguards

1. Anomaly != corruption.
2. Missing source coverage != PASS.
3. Name-only entity matching cannot auto-merge organizations.
4. Public office/PEP status is context, not wrongdoing.
5. Institution category, ownership form, religion, advocacy, nationality, foreign links and organization mission are not suspicion features.
6. Distinguish allegation, investigation, audit finding, discipline sanction, administrative penalty and court judgment.
7. Preserve publication/retrieval time and temporal validity; do not leak future outcomes into temporal screening.
8. Keep `corruption_inference=false` for automated findings and resolution objects.
9. Minimize unnecessary personal/contact data in public artifacts.
10. Use **Cochrane Kang** for visible author naming.

## Handoff completion rule

Before ending a substantial session:
- update canonical process/results files first;
- update `TODO.md`;
- append material decisions to `DECISIONS.md`;
- append a public-safe conversation summary to `CHATLOG.md`;
- append executed/validated work to `SESSION_LOG.md`.
