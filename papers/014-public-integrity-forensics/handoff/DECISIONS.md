# ARIS4C014 · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
- Treat public-data anomalies as auditable leads, never as corruption findings.
- Prefer authoritative stable identifiers; route name-only entity matches to human review.

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.


## 2026-09-19 · Two-axis institution ontology

**Decision:** Replace the flat China institution list as the conceptual target with a two-axis ontology: **legal/organizational identity × functional domain**.

**Why:** Hospitals, universities, SOEs, public institutions, funds and affiliated commercial entities overlap if represented as one flat category list. Orthogonal identity and function axes reduce overlap and support stable cross-source entity resolution.

**Priority missing modules:** rural collective economic organizations; local SOEs/LGFVs; government investment/guidance funds; primary/secondary/vocational education; professional intermediaries; research peripheral/commercialization entities.

**Safety invariant:** institution type, ownership form, public-office status, NGO mission, religion, advocacy position, nationality, foreign connection and sector membership are routing/provenance facts, not corruption evidence.

**Canonical file:** `process/CHINA_INSTITUTION_ONTOLOGY.md`.

## 2026-09-19 · Split reusable OpenIntegrity implementation from the paper repository

**Decision:** Keep **ARIS4C014** as the scientific parent/research record, create **OpenIntegrity** as the reusable implementation repository, and keep **repo-auditor** as an independent auditor rather than merging the anti-corruption/public-integrity agent into repo-auditor.

**Why:** The implementation now contains reusable source adapters, identity resolution, Evidence Graph, detectors, tests, workflows and Agent Skill that are larger than a paper appendix and may support multiple future ARIS4C studies.

**Migration discipline:** preserve working ARIS4C014 code until parity tests pass in the standalone repository; keep frozen pilots and scientific interpretation in ARIS4C014; maintain reciprocal links; run repo-auditor after extraction.

**Current state:** no separate `OpenIntegrity` repository was found in the connected GitHub installation at the time of this decision, so the split is **accepted but not yet implemented**.

**Canonical file:** `process/REPOSITORY_ARCHITECTURE.md`.
