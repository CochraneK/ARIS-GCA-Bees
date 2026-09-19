# ARIS4C003 · TODO

## P0 · Next gate

- [x] Confirmatory blind Coder B completed in Qoder using user-reported Qwen Flash 3.8.
- [x] Ingest Coder B, compute A/B agreement, outcome-blind adjudicate exactly 12 flagged cells.
- [x] Freeze `IKES_FROZEN.csv` and full SHA-256 provenance.
- [x] Strict gate reached `DESIGN_LOCKED / OUTCOME_UNLOCKED` with zero problems.
- [x] Correct dyad denominator to use all identifiable countries before analysis-universe restriction.
- [x] Diagnose first monolithic OpenAlex failure (run 35423271792): invalid DuckDB `WITH ... COPY` syntax in country materializer.
- [x] Fix that parser defect in commit `fe82cb54af0c1c0f349d7dfbf16f5eaf636627c3`.
- [ ] Validate the repaired country materializer on a real OpenAlex shard.
- [ ] Dispatch `.github/workflows/aris4c003-openalex-sharded-fallback.yml` (32-way deterministic manifest-balanced country + dyad extraction).
- [ ] Require exact shard aggregation and build zero-filled country/dyad panels.
- [ ] Let `.github/workflows/aris4c003-models.yml` auto-chain only from a successful materialization run.
- [ ] Require `FIRST_RESULT_LOCK.json` before any human interpretation of headline coefficients.
- [ ] After lock: inspect 3 headline PPMLs, complete D01-D21 LOO, 3×999 fixed-seed IKES permutations, temporal profiles, and imperial-center corroboration.

## P1 · Integrity / reporting

- [ ] Keep the failed monolithic run as provenance; do not erase or rewrite it as a successful materialization.
- [ ] Do not modify D01-D21, IKES, COLDAT/CEPII exposures, primary 2019–2022 window, PPML specifications, or permutation seed based on outcomes.
- [ ] Update `STATUS.md`, `AGENT_HANDOFF.md`, `CHATLOG.md`, and `SESSION_LOG.md` after the next material state change.
- [ ] When first results are locked, update manuscript Results without promoting secondary/ranking results over the three confirmatory coefficients.

## P2 · Packaging / optional

- [ ] Generate planned figures/tables only from the locked result package.
- [ ] Maintain English + Chinese manuscript parity and the ARIS4C public-hub/PDF standard.
