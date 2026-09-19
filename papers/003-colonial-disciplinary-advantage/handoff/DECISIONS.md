# ARIS4C003 · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
- Broaden disciplines and outcomes beyond a single ranking metric.
- Freeze outcome-blind coding/design before confirmatory outcome analysis.

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.


## 2026-09-19 · Confirmatory Coder B and IKES freeze

**Decision:** Accept the second fresh blind coding pass produced in Qoder using
the user-reported Qwen Flash 3.8 model as confirmatory Coder B because its raw
response declared both `BUNDLE_ACCESS_STATUS: PASS` and
`INDEPENDENCE_STATUS: PASS`, and the machine ingest accepted the complete
21×11 matrix plus 21 evidence sections.

**Result:** A/B agreement flagged 12 missing/abs-difference>=2 cells. Exactly
those 12 were adjudicated outcome-blind using historical evidence; all other
cells remained immutable A/B means. `IKES_FROZEN.csv` and SHA-256 provenance
were created. The strict gate became `DESIGN_LOCKED / OUTCOME_UNLOCKED`.

**Canonical files:** `process/gptpage/2026-09-19_ikes-coder-b-qoder-raw.md`,
`process/IKES_CODER_B.csv`, `process/ikes_adjudication/ADJUDICATION_MEMO.md`,
`process/IKES_FROZEN.csv`, `process/IKES_FROZEN.provenance.json`,
`process/PREOUTCOME_GATE_UNLOCKED.json`.

## 2026-09-19 · Dyad implementation correction before first results

**Decision:** Enforce the already frozen rule that multilateral pair weights use
the number of **all identifiable OpenAlex countries on the work** before
restricting endpoints to the 159-country analysis universe.

**Why:** The earlier implementation counted only mapped analysis-universe
countries, which would renormalize retained pair mass upward when a work also
contained an out-of-universe country.

**Status:** Corrected before any modern effect estimate was inspected and
documented in `process/IMPLEMENTATION_CORRECTION_001.md`.

## 2026-09-19 · OpenAlex materialization recovery path

**Decision:** Do not rerun the failed monolithic OpenAlex workflow as the
canonical recovery route. Use the deterministic 32-way manifest-balanced
sharded fallback and exact sufficient-statistic aggregation.

**Why:** Run `35423271792` spent about 73 minutes in the country extraction
then failed because the country materializer generated invalid DuckDB syntax
(`WITH ... COPY (...)`). The parser construction was fixed in commit
`fe82cb54af0c1c0f349d7dfbf16f5eaf636627c3`, but that repair remains to be
validated on a real shard.

**Canonical recovery workflow:**
`.github/workflows/aris4c003-openalex-sharded-fallback.yml`.

**Downstream workflow:** `.github/workflows/aris4c003-models.yml` must run
only after successful materialization and must create
`process/FIRST_RESULT_LOCK.json` before human interpretation.
