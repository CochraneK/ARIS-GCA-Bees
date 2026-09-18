# ARIS4C006 · Pilot 11 — anchor-field annual primary-field coverage sweep

Last updated: 2026-09-18

## Verdict

**Six-anchor-field historical coverage: PASS. Candidate global window: 2011–2025.**

GitHub Actions run: `35301293322`  
Artifact: `aris4c006-annual-coverage`

This corrected sweep uses `primary_topic.field.id`.

## Prospective anchor-window rule

Before reading annual results, the pilot selected the earliest start in 2010–2018 such that every subsequent year through 2025 satisfied:

1. aggregate DOI coverage >=0.90;
2. Crossref retrieval conditional on DOI >=0.90;
3. strict positional support among same-count OpenAlex/Crossref records >=0.95;
4. at least 5/6 anchor fields with DOI coverage >=0.80.

## Result

2010 failed aggregate DOI coverage:
- **88.89%**

2011 passed, and every year 2011–2025 continued to satisfy the anchor-field rule.

Thus the six-field rule-selected candidate start is:

**2011**

Selected examples:

| Year | DOI | Crossref given DOI | Strict position support |
|---|---:|---:|---:|
| 2011 | 95.41% | 95.19% | 100% |
| 2015 | 92.50% | 94.59% | 100% |
| 2020 | 100% | 94.17% | 100% |
| 2024 | 100% | 99.17% | 99.14% |
| 2025 | 98.33% | 100% | 99.15% |

## Critical scope correction

The six fields were engineering/contrast anchors:
- Economics
- Mathematics
- Business
- Psychology
- Medicine
- Engineering

Pilot 13 subsequently established that all **26 current OpenAlex primary-topic fields** are globally feasible.

Therefore this pilot **does not by itself freeze the final all-field 2011–2025 window**.

The correct rule is:

- **2011–2025 = candidate global window**
- final global start year requires an all-26-field historical coverage audit using the same primary-topic and primary-work-type rules.

No focal surname-effect or career outcome was inspected in making this correction.

## 2026 handling

2026 is incomplete and is not a confirmatory outcome year.

## Gate consequence

**Historical coverage feasibility: PASS.**  
**Final all-field start year: OPEN pending all-field historical audit.**
