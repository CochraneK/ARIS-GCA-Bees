# ARIS4C014 · Research context

## Project

**Public Integrity Forensics: An Auditable Multi-Source Agent for Corruption-Risk Screening from Open Data**

## Compact scope

An auditable multi-source public-integrity agent that mines structured and web-native public records across government, hospitals, SOEs, research institutes, universities, social organizations, suppliers and additional public-interest institution classes, builds a time-aware evidence graph, and produces reproducible human-review leads without equating anomalies, public-office status, organizational identity or web allegations with corruption.

## Current scientific state

- China Pilot 0 procurement / institution-source feasibility is frozen.
- CCGP live discovery, award-detail normalization, candidate-vs-final semantics and supplier USCC parsing are proven in bounded live workflows.
- Exact stable IDs can support cross-source organization identity; name-only identity remains source-local or review-only.
- CAS official research-unit seeds are available in the current universe adapter; unavailable sources remain coverage gaps rather than negative evidence.
- Current portfolio handoff stage: China Pilot 1 · conservative cross-source entity layer.

## Institution-universe model

The target China ontology is now **two-axis**:

1. legal / organizational identity;
2. functional domain.

Canonical design: `../process/CHINA_INSTITUTION_ONTOLOGY.md`.

High-value missing modules include rural collective economic organizations, local SOEs/LGFVs, government investment/guidance funds, primary/secondary/vocational education, professional intermediaries, and research peripheral/commercialization entities.

## Repository architecture

Canonical decision: `../process/REPOSITORY_ARCHITECTURE.md`.

- **ARIS4C014:** scientific parent, methods, pilots, validation, papers and frozen interpretation.
- **OpenIntegrity:** planned standalone reusable implementation / agent repository.
- **repo-auditor:** independent repository quality/safety/release auditor.

As of 2026-09-19, the standalone OpenIntegrity repository is planned but not yet present in the connected GitHub installation.

## Construct / claim discipline

- Public-data anomalies are auditable leads, never automatic corruption findings.
- Missing source coverage != negative evidence.
- Public office/PEP status is context, not wrongdoing.
- Investigations, allegations, audit findings, sanctions, administrative penalties and court judgments remain distinct classes.
- Institution type, ownership form, organization mission, religion, advocacy position, nationality and foreign links are not suspicion features.
- Named outputs remain human-review oriented with `corruption_inference=false`.

## Where to continue

1. Read `AGENT_HANDOFF.md`, `TODO.md`, `DECISIONS.md`, newest `CHATLOG.md` and `SESSION_LOG.md`.
2. Read `../process/STATUS.md` and `../process/CHINA_PILOT0_RESULTS.md`.
3. Read `../process/CHINA_INSTITUTION_ONTOLOGY.md` and `../process/REPOSITORY_ARCHITECTURE.md`.
4. Bootstrap OpenIntegrity, establish CI parity, then continue exact-stable-ID China source expansion.
