# ARIS4C003 · PRE-DELETE CHECKPOINT · 2026-09-19

This is the **single-file recovery entry point** after deletion of the originating
ChatGPT conversation.

## 1. Project

**Title:** Colonial Legacies and the Global Geography of Disciplinary Advantage

**Research object:** historical knowledge capital / persistent discipline-specific
institutional and network legacies of empire and colonialism.

**Current project status:** `analysis-running`.

**Frozen headline family:**

1. Former-colony fractional output: HistoricalExposure × IKES.
2. Former-colony Top-10% impact rate: HistoricalExposure × IKES.
3. Former-colonial-tie collaboration: ColonialTie × IKES.

Primary mature window: **2019–2022**.

No ranking/prestige result may replace any of these three headline tests.

## 2. Frozen design state

The strict gate is already closed successfully:

`process/PREOUTCOME_GATE_UNLOCKED.json`

Expected contents:

- `DESIGN_LOCKED`
- `OUTCOME_UNLOCKED`
- `design_problems = []`
- `outcome_problems = []`

Do **not** reopen the design merely because this chat was deleted.

Key frozen inputs include:

- ARIS v0.4.26, commit `951654847b015585385b2448c5667dcd04e7b56b`;
- D01–D21 discipline set and OpenAlex crosswalk;
- 11-dimension IKES rubric;
- COLDAT former-colony exposure;
- CEPII V202211 dyads;
- OpenAlex Works manifest pinned to 2026-06-26;
- 2019–2022 headline window;
- PPML/HDFE model family and clustering;
- fixed permutation seed `20260918`, 999 replications;
- complete D01–D21 leave-one-discipline-out diagnostics;
- period-specific persistence profile.

## 3. Confirmatory Coder B

### Attempt 1

The first WorkBuddy attempt is preserved but **not confirmatory** because its
context opened parent paper README/STATUS files before coding. Never promote it.

Files:

- `process/gptpage/2026-09-18_ikes-coder-b-raw.md`
- `process/IKES_CODER_B_ATTEMPT1_CONTAMINATED.csv`
- `process/IKES_CODER_B_ATTEMPT1_ASSESSMENT.md`

### Confirmatory pass

A fresh Qoder pass using the **user-reported Qwen Flash 3.8** model accessed
only the blind bundle plus external historical scholarship and declared:

- `BUNDLE_ACCESS_STATUS: PASS`
- `INDEPENDENCE_STATUS: PASS`

Canonical raw response:

`process/gptpage/2026-09-19_ikes-coder-b-qoder-raw.md`

Canonical parsed files:

- `process/IKES_CODER_B.csv`
- `process/IKES_CODER_B.md`
- `process/CODER_B_RUN_METADATA_2026-09-19.json`

Agreement summary:

- 21 disciplines / 231 cells;
- 2 missing A/B pairs;
- mean absolute difference = **0.5676855895**;
- IKES-mean ICC(2,1) = **0.6593084418**;
- 12 cells flagged by the frozen missing-or-abs-difference>=2 rule.

Exactly those 12 were adjudicated outcome-blind. See:

- `process/ikes_adjudication/AGREEMENT_SUMMARY.json`
- `process/ikes_adjudication/ADJUDICATION_DECISIONS.csv`
- `process/ikes_adjudication/ADJUDICATION_MEMO.md`
- `process/ikes_adjudication/IKES_DISAGREEMENTS_ADJUDICATED.csv`

Final frozen construct:

- `process/IKES_FROZEN.csv`
- `process/IKES_FROZEN.provenance.json`

The freeze provenance hashes Coder A, Coder B scores, Coder B evidence notes,
untouched raw Coder B output, adjudication table, and final frozen IKES.

**Do not rerun Coder B and do not re-adjudicate based on modern results.**

## 4. Pre-result implementation correction already made

The dyadic fractional-collaboration implementation originally counted only
countries remaining after restriction to the 159-country analysis universe.

That was inconsistent with the frozen rule. It was corrected before substantive
modern outcome inspection so that pair weight uses **all distinct identifiable
OpenAlex countries on the work first**, then retained endpoints are restricted
to the analysis universe.

See:

`process/IMPLEMENTATION_CORRECTION_001.md`

Do not revert this.

## 5. First OpenAlex materialization attempt — FAILED, no result package

Workflow:

`ARIS4C003 materialize OpenAlex outcomes`

Run ID:

`35423271792`

Conclusion:

`failure`

Country job sequence:

1. checkout/install passed;
2. strict gate passed as `DESIGN_LOCKED / OUTCOME_UNLOCKED`;
3. public OpenAlex extraction ran for roughly **73 minutes**;
4. it then failed in DuckDB with:

`Parser Error: syntax error at or near "COPY"`

Cause:

`materialize_openalex_cells.py` emitted a query structurally equivalent to:

`WITH ... COPY (SELECT ...)`

instead of:

`COPY (WITH ... SELECT ...)`.

Therefore:

- no successful country outcome artifact was produced;
- no usable complete dyad artifact was produced;
- `build-panels` was skipped;
- no PPML headline coefficient was produced;
- no p-value was inspected;
- no `FIRST_RESULT_LOCK.json` exists from this run.

**Do not describe run 35423271792 as successful outcome materialization.**

## 6. Parser repair

The country materializer was corrected on 2026-09-19 in commit:

`fe82cb54af0c1c0f349d7dfbf16f5eaf636627c3`

The output form is now:

`COPY (WITH ... SELECT ...) TO ...`

The code was re-read after the patch and the malformed `WITH ... COPY`
construction is no longer present in the two country-output queries.

However, at this checkpoint the repair has **not yet been validated on a real
OpenAlex shard**. Treat it as code-fixed / integration-unverified.

## 7. Canonical OpenAlex recovery route

Do **not** make the failed monolithic workflow the default retry.

Use:

`.github/workflows/aris4c003-openalex-sharded-fallback.yml`

The fallback:

- reads the pinned official Works manifest;
- deterministically creates **32 size-balanced shards**;
- runs country and dyad extraction independently per shard;
- passes exact public-S3 file lists through `@file` mode;
- aggregates sufficient statistics with
  `code/aggregate_openalex_shards.py`;
- constructs zero-filled confirmatory panels;
- writes `process/OUTCOME_MATERIALIZATION_AUDIT.json`;
- uploads `aris4c003-analysis-panels` as the canonical model input artifact.

Before trusting the full run, verify at least one real shard completes with the
repaired country materializer. If a shard fails, fix the engineering issue
without changing frozen scientific choices.

## 8. Downstream model execution already prepared

Workflow:

`.github/workflows/aris4c003-models.yml`

It is designed to start only after successful materialization or by explicit
dispatch with a successful materialization run ID.

It contains:

- core frozen PPML fits;
- 3 complete LOO jobs (output / impact / dyad);
- 20 permutation shards covering exactly reps 1–999 for each headline model;
- strict aggregation that refuses incomplete/failing sensitivity packages;
- temporal profile;
- small-output/median IKES sensitivities;
- small-N imperial-center corroboration;
- result-package SHA-256 lock.

Required pre-interpretation artifact:

`process/FIRST_RESULT_LOCK.json`

**No human interpretation of headline direction/significance before this file
has been created from a complete package.**

## 9. Manuscript work already safe in Git

Pre-result drafts already exist:

- `manuscript/INTRODUCTION_LOCKED_EN.md`
- `manuscript/INTRODUCTION_LOCKED_ZH.md`
- `manuscript/METHODS_LOCKED_EN.md`
- `manuscript/METHODS_LOCKED_ZH.md`

The repository also contains a pre-result interpretation protocol and frozen
figure/table plan in `process/`. Keep English and Chinese manuscripts aligned
after results.

## 10. Exact next actions

1. Read `../STATUS.md`, this checkpoint, `TODO.md`, and `DECISIONS.md`.
2. Confirm latest pre-outcome/integrity CI remains green after the parser patch.
3. Validate repaired country materializer on a real shard.
4. Dispatch the 32-way sharded fallback.
5. Require exact aggregation + zero-filled analysis panels.
6. Let the distributed model workflow run from the successful materialization.
7. Require `FIRST_RESULT_LOCK.json`.
8. Only then inspect the three headline results and robustness diagnostics.
9. Update Results in English + Chinese; do not “rescue” null results with
   rankings or secondary periods.

## 11. Do-not-change list

Without a clearly dated post-result amendment, do not change:

- D01–D21 membership;
- primary OpenAlex selectors;
- IKES or its dimension weights;
- the 12 historical adjudications;
- COLDAT/CEPII primary exposure definitions;
- country/dyad fractional counting rules;
- the primary 2019–2022 period;
- the three headline models;
- permutation seed/repetition count;
- the rule that failed refits are reported, not silently discarded.

## 12. Continuity rule

Git is the canonical cross-chat/cross-device/cross-agent state. A future agent
must not infer project state from remembered chat fragments when these files are
available.

For the shortest safe restart:

1. `handoff/PRE_DELETE_CHECKPOINT_2026-09-19.md`
2. `STATUS.md`
3. `handoff/TODO.md`
4. `handoff/DECISIONS.md`
5. `process/PREOUTCOME_GATE_UNLOCKED.json`
6. `process/IKES_FROZEN.provenance.json`

This checkpoint is public-safe and contains no secret credentials or hidden
chain-of-thought.
