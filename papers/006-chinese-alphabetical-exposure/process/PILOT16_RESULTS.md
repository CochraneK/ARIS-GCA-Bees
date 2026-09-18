# ARIS4C006 · Pilot 16 — all-field historical coverage

Last updated: 2026-09-19

## Verdict

**PASS. Final primary focal-work window: 2011–2025.**

GitHub Actions run: `35325202486`  
Artifact: `aris4c006-all-field-historical-coverage`

This audit uses:
- all 26 current OpenAlex primary-topic fields;
- `primary_topic.field.id`;
- frozen primary work types `article | conference-paper`;
- reproducible random multi-author samples;
- DOI -> Crossref structured-author reconciliation.

## Prospective global-window rule

Before reading results, select the earliest start in 2010–2018 such that every later year through 2025 has:

1. aggregate DOI coverage >=0.90;
2. Crossref retrieval conditional on DOI >=0.90;
3. strict positional support among same-count records >=0.95;
4. at least 22/26 fields with DOI coverage >=0.75.

## Result

2010 failed:
- aggregate DOI coverage: **86.73%**.

2011 passed:
- aggregate DOI coverage: **92.86%**
- Crossref given DOI: **92.86%**
- strict positional support: **100%**
- 25/26 fields with DOI >=0.75.

Every year **2011 through 2025** continued to satisfy the frozen global rule.

Selected examples:

| Year | DOI | Crossref given DOI | Strict positional support |
|---|---:|---:|---:|
| 2015 | 95.67% | 93.47% | 99.46% |
| 2020 | 99.04% | 97.09% | 99.49% |
| 2023 | 100% | 100% | 100% |
| 2024 | 100% | 100% | 100% |
| 2025 | 100% | 98.56% | 100% |

## Frozen window

**Primary focal works: 2011-01-01 through 2025-12-31.**

2026 is incomplete and excluded.

For the 3-year lagged convention exposure, focal 2011 observations require exposure-building data from 2008–2010 even though focal outcomes begin in 2011.

## Longitudinal consequence

With:
- focal observation window beginning 2011;
- 3-year clean lookback;
- 5-year fixed follow-up;
- last complete outcome year 2025;

the frozen longitudinal entry window **2014–2020** remains internally consistent.

## Gate consequence

**Final all-field historical time-window gate: PASS.**

Pilot 16 supersedes the six-anchor-field Pilot 11 for final time-window selection.
