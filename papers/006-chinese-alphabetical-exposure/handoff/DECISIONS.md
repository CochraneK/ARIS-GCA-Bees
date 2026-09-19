# ARIS4C006 · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
- Validate Chinese surname identity/romanization before testing alphabetical exposure.
- Model alphabetical-authorship regime as an exposure context rather than assuming all fields order authors alphabetically.

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.

## 2026-09-19 · Pre-delete synchronization from the ARIS4C006 design/analysis chat

**Decision:** Git canonical state supersedes stale chat/dashboard snapshots.

**Why:** This chat began while ARIS4C006 was still in feasibility/research-design work, but repository automation/parallel agents subsequently advanced the project through all outcome-blind gates, preregistration lock/unlock, H1/H2 confirmatory execution, and H1 robustness. Deleting this chat must not roll the project back.

**Current frozen decisions to preserve:**
- primary field assignment is `primary_topic.field.id`;
- all 26 OpenAlex fields are globally eligible;
- focal work window is 2011–2025;
- primary work types are article + conference-paper;
- primary exposure is exact-LOAO primary-field × prior-3-year alphabetization exposure;
- raw source-level exposure is not primary;
- focal surname forms use ChineseNames population counts + pinned CCNC surname-specific Romanization;
- raw embedded OpenAlex author IDs are canonicalized before longitudinal joins;
- H1 is the within-work `RelAlphaRank × LOAOExposure` mechanism with work FE and three-way clustering;
- H3 is a 2014–2020 entry cohort with 3-year clean lookback, 5-year follow-up, and observed five-year publication persistence;
- locked files stay byte-for-byte stable unless a formal amendment is made.

**Confirmatory state:** H1 PASS; H2 raw result opened; H3 structural cohort gate pending/running. H2 final Holm status waits for H3.

**Affected continuity files:** handoff/AGENT_HANDOFF.md, STATUS.md, TODO.md, CONTEXT.md, DECISIONS.md, CHATLOG.md, SESSION_LOG.md, plus deletion checkpoint.
