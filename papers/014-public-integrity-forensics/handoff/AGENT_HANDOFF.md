# ARIS4C014 · Agent takeover brief

## What this project is

**Public Integrity Forensics: An Auditable Multi-Source Agent for Corruption-Risk Screening from Open Data**

An auditable multi-source public-integrity agent that mines structured and web-native public records across government, hospitals, SOEs, research institutes, universities, NGOs/social organizations and suppliers, builds a time-aware evidence graph, and produces reproducible human-review leads without equating anomalies, public-office status, organizational identity or web allegations with corruption. China Pilot 1 now has a CI-validated exact-CN-USCC cross-source enrichment contract: factual attributes auto-attach only under exact stable-ID equality; name-only matches require review; same-name disjoint IDs are conflicts; inaccessible sources remain coverage gaps. A real lawful second-source corporate enrichment run is still pending.

## Current state

- Activity: **active**
- Progress: **71%**
- Stage: **China Pilot 1 · exact-USCC cross-source enrichment contract validated**
- Evidence: CCGP/CAS/USCC graph + stable-ID-only resolver now extended with a tested cross-source enrichment contract: only exact valid CN-USCC equality can auto-attach allowlisted factual registry attributes; name-only matches are REVIEW_CANDIDATE, same-name disjoint IDs are conflicts, interactive/unavailable sources are COVERAGE_GAP, sensitive contact fields are not propagated, and corruption_inference remains false. ARIS4C014 CI runs 118–119 PASS.

## Immediate next action

**Implement the first lawful second-source organization adapter that exposes exact CN-USCC without bypassing interactive/CAPTCHA controls; run a bounded joinability enrichment and report exact-ID matches, review candidates, conflicts and coverage gaps.**

## Current blocker / gate

No architecture blocker. The primary constraint is lawful machine-readable access to authoritative second-source stable identifiers; interactive/CAPTCHA-protected registries must remain explicit coverage gaps rather than being bypassed.

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
