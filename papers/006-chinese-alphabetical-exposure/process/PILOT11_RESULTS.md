# ARIS4C006 · Pilot 11 — annual primary-field coverage sweep

Last updated: 2026-09-18

## Verdict

**Primary work-level focal window: 2011–2025.**

GitHub Actions run: `35301293322`  
Artifact: `aris4c006-annual-coverage`

This is the corrected sweep using `primary_topic.field.id`.

## Prospective window rule

Before reading annual results:

Choose the earliest start year in 2010–2018 such that **every subsequent year through 2025** satisfies:

1. aggregate DOI coverage >= 0.90;
2. Crossref retrieval conditional on DOI >= 0.90;
3. strict positional support among same-count OpenAlex/Crossref records >= 0.95;
4. at least 5 of 6 anchor fields have DOI coverage >=0.80.

## Result

2010 failed the aggregate DOI threshold:

- DOI coverage: **88.89%**

2011 passed and **every year 2011–2025 remained above all prospective thresholds**.

Therefore the rule-selected start is:

**2011**

and the primary focal work window is:

**2011–2025**

## Selected annual metrics

| Year | DOI | Crossref given DOI | Strict position support |
|---|---:|---:|---:|
| 2011 | 95.41% | 95.19% | 100% |
| 2015 | 92.50% | 94.59% | 100% |
| 2020 | 100% | 94.17% | 100% |
| 2024 | 100% | 99.17% | 99.14% |
| 2025 | 98.33% | 100% | 99.15% |

All six anchor fields met the per-field DOI >=0.80 condition in every year from 2011 onward.

## Interpretation

The date window is selected from bibliographic measurement coverage only.

No surname × exposure or career outcome estimate was opened.

## Lagged exposure

For focal year `t`, primary exposure uses `t-3...t-1`.

Field-year observations still require the frozen LOAO effective-information threshold `D^{-i}_{ct} >= 50`.

A field can therefore be absent in an early focal year if its historical convention window is too sparse, without changing the global 2011–2025 focal work window.

## Longitudinal cohort consequence

To keep the entry cohort wholly inside the high-coverage focal era while allowing:

- 3-year clean lookback; and
- 5-year fixed follow-up through the last complete year 2025,

the candidate longitudinal entry window becomes:

**2014–2020**

This entry window is frozen separately in the cohort protocol before distal outcomes are estimated.

## Gate consequence

**Time-window coverage: PASS.**

Primary work-level frame: **2011–2025**.
