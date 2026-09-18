# ARIS4C006 · Pilot 6 — exposure-variance feasibility

Last updated: 2026-09-18

## Verdict

**Field/year exposure variance: PASS.**  
**Source-level exposure: not yet adequately supported by the random pilot; targeted source sampling required.**

GitHub Actions run: `35298012471`  
Artifact: `aris4c006-exposure-variance-pilot`

This pilot used reproducible OpenAlex random samples and Crossref structured family names. It did not use focal surname rank or career outcomes.

## Design

- Years: 2020 and 2024
- Fields: Economics, Mathematics, Business, Psychology, Medicine, Engineering
- Requested random multi-author works: 60 per field/year cell
- High-confidence valid author-order works: **670**
- Work-level chance correction:
  - `I_alpha = 1` for lexicographically non-decreasing family-name order
  - `p_chance = prod(m_j!)/n!` with surname ties
  - `ExcessAlpha = sum(I_alpha - p_chance) / sum(1 - p_chance)`

## Field/year results

Observed field/year `ExcessAlpha` range:

**−0.0290 to +0.2093**

SD across the 12 field/year cells:

**0.0733**

Selected estimates:

| Field | 2020 | 2024 | 2020 (3+ authors) | 2024 (3+ authors) |
|---|---:|---:|---:|---:|
| Economics | +0.043 | −0.008 | +0.069 | +0.057 |
| Mathematics | **+0.176** | **+0.209** | **+0.193** | **+0.130** |
| Business | +0.053 | +0.085 | +0.076 | +0.088 |
| Psychology | −0.011 | +0.040 | −0.001 | −0.016 |
| Medicine | −0.029 | +0.009 | −0.018 | −0.001 |
| Engineering | +0.012 | −0.023 | +0.024 | −0.005 |

## Interpretation

The institutional moderator is not degenerate.

Most importantly:

- Mathematics remains strongly positively alphabetized in both periods.
- Business shows moderate positive excess alphabetization.
- Medicine and Engineering are near the random-order benchmark.
- Psychology is near zero in the 3+ author analysis.
- The qualitative high/low contrast survives the mandatory 3+ author restriction.

This is enough to support a measured **field/year exposure gradient** rather than a categorical literature-based field label.

## Why source-level exposure is not yet frozen

The random 60-work cells were too sparse within individual sources.

Only **14** source × field × year contexts reached even `n >= 4`, and some provisional cells carried `NO_SOURCE`. The source-context score range was wide, but at these cell sizes that width is mostly an instability warning rather than evidence of reliable journal-level heterogeneity.

Therefore:

- `source × field × year` is **not** yet accepted as the primary context;
- `NO_SOURCE` must never be an eligible source context;
- a targeted source pilot will identify high-volume sources independently using OpenAlex `group_by` counts and then sample convention works within those sources.

## Exposure architecture after Pilot 6

Current hierarchy:

1. **field × lag-window exposure** — feasible;
2. **source × field × lag-window exposure** — preferred if targeted source reliability passes;
3. broader field long-run exposure — fallback / robustness only.

The confirmatory estimator will continue to use lagging and author-level cross-fitting / leave-one-author-out rules to prevent the focal observation from defining its own moderator.

## Gate consequence

**Exposure variation exists: PASS.**  
**Granularity/reliability gate: still OPEN at the source level.**

A null source-level reliability result would not kill the project; it would freeze field/year exposure as the primary measured moderator and demote journal/source heterogeneity to exploratory analysis.
