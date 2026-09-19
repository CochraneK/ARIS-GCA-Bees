# ARIS4C006 · Agent takeover brief

Last synchronized: 2026-09-19

## What this project is

**Alphabetical Exposure and Scholarly Credit in China's Research System**

A population-calibrated, all-field study of whether validated Chinese surname position is translated into listed authorship position specifically under independently measured alphabetical-authorship regimes, with a preregistered longitudinal five-year publication-persistence extension.

## Canonical current state

**Stage: ANALYSIS.**

The Git repository is ahead of the older portfolio/dashboard snapshot. For scientific state, read `process/STATUS.md` first; do not infer the current gate from the stale dashboard progress number.

Outcome-blind gates passed, `PREREGISTRATION_LOCK.json` was committed, and a separate matching `CONFIRMATORY_UNLOCK.json` was committed before confirmatory outcome access.

### H1 — primary mechanism: PASS

Frozen confirmatory frame:
- exact-LOAO focal rows: **75,205**
- works: **15,410**
- canonical authors: **68,176**
- primary-field × year clusters: **386**

Primary interaction `RelAlphaRank × LOAOExposure`:
- beta = **+0.6479808**
- SE = **0.1228913**
- 95% CI = **[0.4071182, 0.8888434]**
- two-sided p = **1.3436e-07**

Robustness already passed:
- focal teams 3+ authors;
- exposure estimated from 3+ author convention works;
- both restrictions jointly;
- low-alphabetization negative-control slope approximately zero.

### H2 — first-listed authorship: raw confirmatory result opened

Interaction:
- beta = **−0.6280066**
- SE = **0.1408537**
- 95% CI = **[−0.9040748, −0.3519384]**
- raw two-sided p = **8.2507e-06**

H2 is not yet multiplicity-final. Its Holm-adjusted status is frozen to be computed jointly with H3.

### H3 — longitudinal persistence

H3 is the only remaining confirmatory secondary gate.

Frozen H3 design:
- entry years **2014–2020**;
- 3-year clean lookback;
- 5-year fixed follow-up;
- endpoint = observed five-year publication persistence;
- nested in the already frozen primary-frame authors;
- deterministic 64-shard preoutcome cohort materialization;
- H3 cannot run unless the frozen structural adequacy gate passes.

At the latest canonical checkpoint, the full nested entry-cohort materialization is running / awaiting structural-gate completion. Do not open persistence or estimate H3 before that gate passes.

## Frozen design essentials

- focal work window: **2011–2025**
- primary work types: `article` + `conference-paper`
- field assignment: **OpenAlex `primary_topic.field.id`**
- field scope: all **26 current OpenAlex fields**
- focal population language: **CN-affiliated authorships with validated ChineseNames × CCNC surname forms**; no nationality/ethnicity inference
- Chinese surname population authority: **ChineseNames 2025.8**
- pronunciation/order authority: pinned **CCNC surname-specific Romanization**
- mapped population denominator: **1,181,331,391 (99.9671%)**
- primary exposure: primary-topic field × prior 3 complete years
- estimator: chance-corrected exact **leave-one-author-out**, require `D^{-i}_{ct} >= 50`
- raw source/journal exposure: secondary/exploratory only
- primary predictor: within-team `RelAlphaRank`
- primary outcome: normalized listed byline position
- primary model: work fixed effects
- inference: three-way clustering by canonical author + work + primary-field×year
- raw embedded OpenAlex author IDs must be canonicalized before longitudinal joins
- last-token surname heuristics are forbidden for confirmatory inclusion

## Lock integrity — do not edit casually

The preregistration lock label is:

`ARIS4C006-prereg-v1`

Combined SHA-256:

`c416b84523d30346a46e5779fb55393af63bae0f578ca71a19c4671325e21ffd`

Before any confirmatory runner executes, it must verify:
1. every locked file still matches the committed hashes;
2. `CONFIRMATORY_UNLOCK.json` references the same lock label/hash.

Do **not** edit a locked design file merely to reflect later state. Status/result/handoff files may be updated; locked design files stay byte-for-byte stable unless a formally documented amendment protocol is used.

## Immediate next actions

1. Finish/inspect the H3 preoutcome structural cohort aggregation.
2. If the frozen H3 adequacy thresholds PASS, execute H3 through a lock-verifying confirmatory runner.
3. Compute the frozen joint Holm correction for H2 + H3.
4. Complete remaining preregistered H1 falsification/robustness outputs that are not already materialized.
5. Move to result tables/figures and bilingual EN/ZH manuscripts; preserve confirmatory vs exploratory boundaries.
6. Re-check closest-prior-work publication status before manuscript submission, especially Crabtree–Holbein–Tsutsui.

## Canonical recovery order

Read in this order after a chat/account/device switch:

1. `process/STATUS.md`
2. `process/PREREGISTRATION_LOCK.json`
3. `process/CONFIRMATORY_UNLOCK.json`
4. `process/CONFIRMATORY_H1_H2_RESULTS.md`
5. `process/H1_ROBUSTNESS_RESULTS.md`
6. `process/ANALYSIS_SPEC.json`
7. `process/PREREGISTRATION_DRAFT.md`
8. `process/LONGITUDINAL_SAMPLING_RULE.md`
9. this handoff package

## Before changing anything

- Treat Git as the canonical source of truth, not deleted chat history.
- Preserve locked/preregistered design decisions.
- Do not broaden claims beyond the evidence state.
- Use **Cochrane Kang** for visible author naming.
- Do not commit secrets, private credentials, hidden chain-of-thought, or unnecessary sensitive personal data.
- Update canonical research files first after a material new result, then refresh this handoff package.
