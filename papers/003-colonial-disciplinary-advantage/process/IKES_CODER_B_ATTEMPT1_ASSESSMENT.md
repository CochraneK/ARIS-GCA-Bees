# IKES CODER B ATTEMPT 1 — PROCEDURAL ASSESSMENT

**Date:** 2026-09-18  
**Raw response:** `process/gptpage/2026-09-18_ikes-coder-b-raw.md`  
**Confirmatory admissibility:** **FAIL — do not use to unlock outcomes**

## Why this attempt is not the confirmatory Coder B

The WorkBuddy response explicitly states that, during task triage, the same
context viewed the paper-root `STATUS.md` and `README.md`.

That access violates the pre-existing whitelist-only blind-bundle rule, which
required WorkBuddy to read only the files pinned under
`process/coder_b_blind/` plus independently discovered historical scholarly
evidence.

The response also states that it did **not** see Coder A scores or contemporary
confirmatory outcomes. Therefore this is not treated as evidence of substantive
outcome contamination. However, confirmatory Coder B was defined more strictly:
procedural isolation from the surrounding ARIS4C003 context.

For that reason this attempt is preserved as a **non-confirmatory sensitivity
coding / pilot second coding pass**, not silently discarded and not promoted
into `IKES_CODER_B.csv`.

## Diagnostic agreement with Coder A

These diagnostics are computed only to assess the usefulness/stability of the
rubric. They do not cure the blinding violation.

- disciplines: 21
- dimension cells: 231
- missing pairs: 0
- mean absolute A/B cell difference: **0.441558**
- IKES-mean ICC(2,1): **0.754470**
- cells with absolute disagreement >=2: **8**

Quadratic-weighted kappa by dimension:

- D1: 0.714734
- D2: 0.668580
- D3: 0.747922
- D4: 0.847273
- D5: 0.747495
- D6: 0.753769
- D7: 0.757225
- D8: 0.726257
- D9: 0.601367
- D10: 0.871795
- D11: 0.692683

Cells that would have required adjudication had the pass been admissible:

| concept | dimension | A | attempt-1 B | abs diff |
|---|---:|---:|---:|---:|
| D02 Archaeology | D1 | 1 | 3 | 2 |
| D10 Political Science / IR | D3 | 2 | 0 | 2 |
| D11 Law | D9 | 2 | 0 | 2 |
| D13 Public Administration / Social Policy | D2 | 2 | 0 | 2 |
| D13 Public Administration / Social Policy | D3 | 3 | 1 | 2 |
| D13 Public Administration / Social Policy | D9 | 2 | 0 | 2 |
| D16 Demography / Population Studies | D9 | 2 | 0 | 2 |
| D19 Chemistry | D9 | 2 | 0 | 2 |

## Interpretation

The attempt is useful evidence that the rubric yields substantial rather than
arbitrary agreement across two different coding processes. The weakest
dimension is D9 (collections/archives/specimens), which is also where five of
the eight large disagreements occur. This should be remembered for later
measurement discussion.

It must **not** be used to choose or alter the confirmatory rubric, field set,
weights, exposure, or outcome model.

## Required next action

Run a fresh WorkBuddy/model context that has not opened the ARIS4C003 paper root.
It must use only the pinned blind-bundle files and independently retrieved
historical sources.

The fresh response must explicitly declare both:

`BUNDLE_ACCESS_STATUS: PASS`

and

`INDEPENDENCE_STATUS: PASS`

before it can become canonical `IKES_CODER_B.csv`.
