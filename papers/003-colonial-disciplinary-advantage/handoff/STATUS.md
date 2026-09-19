# ARIS4C003 · Current status

- **Title:** Colonial Legacies and the Global Geography of Disciplinary Advantage
- **Project status:** analysis-running
- **Activity:** ready-to-resume
- **Portfolio progress:** 70%
- **Current stage:** Outcome materialization recovery · deterministic 32-way sharded fallback
- **Evidence established:** COLDAT + CEPII audited · Qoder/Qwen Flash 3.8 confirmatory Coder B passed both blind declarations · 12-cell outcome-blind adjudication complete · IKES frozen with SHA-256 provenance · strict gate = DESIGN_LOCKED / OUTCOME_UNLOCKED
- **Outcome inspection state:** No confirmatory coefficient/p-value/ranking result has been inspected; no FIRST_RESULT_LOCK exists yet.
- **Failed run:** monolithic OpenAlex materialization run 35423271792 failed after ~73 minutes in the country job because of invalid DuckDB `WITH ... COPY` syntax; panel build was skipped.
- **Repair:** country materializer syntax fixed in commit `fe82cb54af0c1c0f349d7dfbf16f5eaf636627c3`; real-shard validation still pending.
- **Next gate:** Dispatch and validate `.github/workflows/aris4c003-openalex-sharded-fallback.yml`. On success the existing `aris4c003-models.yml` auto-chain should create panels, run 3 headline PPMLs + 3×999 permutations + LOO + temporal/imperial corroboration, then hash-lock the first result package.
- **Blocker:** No conceptual/design blocker. Engineering validation of the repaired materializer on real OpenAlex shards remains.

## Source of truth

Read, in order:

1. `../STATUS.md`
2. `PRE_DELETE_CHECKPOINT_2026-09-19.md`
3. `../process/PREOUTCOME_GATE_UNLOCKED.json`
4. `../process/IKES_FROZEN.provenance.json`
5. `../process/IMPLEMENTATION_CORRECTION_001.md`
6. `TODO.md` and `DECISIONS.md`

Do not rerun Coder B, alter frozen IKES, switch headline models, or inspect
partial substantive results before the first result package is hash-locked.
