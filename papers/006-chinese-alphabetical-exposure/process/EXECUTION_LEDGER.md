# ARIS4C006 · Execution gate ledger

Last updated: 2026-09-19

This file tracks outcome-blind execution only. It contains no H1/H2/H3 effect estimates.

## Probe gates

### OpenAlex author batch canonicalization
- workflow run: `35406519582`
- result: PASS
- 7/7 sampled raw IDs singleton-resolved;
- batch `openalex:<pipe-separated IDs>` endpoint supported;
- batch result covered all singleton canonical IDs;
- singleton fallback remains mandatory for returned/missing alias cases.

### Final convention probe — Mathematics
- workflow run: `35406709768`
- result: PASS
- annual cells: 17/17;
- annual information target met: 17/17;
- rolling focal contexts: 15/15;
- primary rolling support: 15/15;
- 3+ author rolling support: 15/15;
- valid convention works: 1,265;
- unique canonical authors: 3,418;
- outcomes opened: false.

### Primary-frame probe — Mathematics
- workflow run: `35407076891`
- result: PASS
- focal field-years: 15/15;
- target 40 informative works reached in every field-year;
- retained works: 600;
- focal authorship rows: 1,642;
- unique focal authors: 1,572;
- effect/p-value computation: false.

## Full builds now running

### 26-field final convention
- workflow: `.github/workflows/aris4c006-full-convention.yml`
- run: `35417181411`
- 26 fields × 2008–2024 convention measurement;
- matrix max parallel: 6;
- aggregate is validated by `code/23_aggregate_final_convention.py`.

### 26-field primary frame
- workflow: `.github/workflows/aris4c006-full-primary-frame.yml`
- run: `35417184958`
- 26 fields × 2011–2025 outcome-locked structural frame;
- target 40 informative works per field-year;
- minimum 20 to retain below target;
- no effect/p-value calculation;
- aggregate is validated by `code/25_aggregate_primary_frame.py`.

### Longitudinal identity-risk prevalence
- workflow: `.github/workflows/aris4c006-identity-risk.yml`
- run: `35417251968`
- random 2014–2020 candidate-author QA;
- reports only identity-risk prevalence;
- explicitly does not compute five-year persistence or any surname × exposure effect.

## Preregistration prelock

- workflow run: `35417307896`
- expected result: BLOCKED / failure
- blockers:
  1. prereg still contains unchecked execution checklist;
  2. missing final convention materialization PASS gate;
  3. missing primary-frame materialization PASS gate;
  4. missing longitudinal identity-risk QA PASS gate.

All other required design gates were PASS/pass-like at this audit.

## Unlock rule

Do not generate `PREREGISTRATION_LOCK.json`, do not set `paper.json.status = preregistered`, and do not set `confirmatory_outcomes_unlocked = true` until all three full execution gates above are recorded as PASS and the prelock audit returns zero errors.
