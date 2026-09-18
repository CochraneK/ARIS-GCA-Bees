# ARIS4C006 · Pilot 13 — all-field primary-topic eligibility

Last updated: 2026-09-18

## Verdict

**All 26 current OpenAlex fields pass the prospectively frozen primary-field feasibility gate.**

The six earlier anchor fields remain useful as high/low alphabetization validation settings, but they do **not** define the final disciplinary scope.

GitHub Actions run: `35301344921`  
Artifact: `aris4c006-all-field-eligibility`

## Confirmatory field definition

Field context is defined exclusively by:

`primary_topic.field.id`

not by `topics.field.id`.

A work can carry multiple topics across fields, while the OpenAlex primary-topic field gives one primary field per work.

## Prospective gate

Before reading the artifact, a field was declared primary-frame eligible when all held:

1. China-affiliated primary-field works in 2017–2019 >= 500;
2. China-affiliated primary-field works in 2021–2023 >= 500;
3. pooled random-sample high-confidence structured-order coverage >= 50%;
4. >=8 valid structured-order works in the 2020 sample;
5. >=8 valid structured-order works in the 2024 sample.

## Result

- current OpenAlex fields found: **26**
- fields passing gate: **26 / 26**

No field failed.

## Volume range

Even the lowest-volume field in the pilot exceeded the minimum threshold:

- Veterinary:
  - 2017–2019 CN-affiliated primary-field works: **923**
  - 2021–2023: **1,403**

Examples of larger fields:

- Engineering:
  - 481,198 -> 801,988
- Medicine:
  - 285,456 -> 471,366
- Computer Science:
  - 168,951 -> 296,327
- Environmental Science:
  - 102,114 -> 203,081

Arts and Humanities was also comfortably feasible:

- 7,820 -> 15,635 works.

## Structured-order coverage

Across the two random 15-work field-year samples per field, pooled valid-order coverage ranged from approximately **83.3% to 100%**.

All fields met the predeclared per-year valid-order minimum.

## Exposure heterogeneity

The tiny pilot convention scores are measurement-only and not confirmatory estimates, but they again show substantial field heterogeneity.

For example:
- Mathematics: approximately +0.179 excess alphabetization;
- Psychology: approximately +0.096;
- Economics: approximately +0.069;
- multiple engineering/natural-science fields near zero;
- some fields slightly negative relative to the chance benchmark.

These pilot values are not the final lagged exposure table.

## Scope consequence

The primary work-level study may span **all 26 current OpenAlex primary-topic fields**.

A field can still be absent from a particular focal year if the final LOAO field-window information threshold fails for that year/author, but there is no global field exclusion based on this feasibility gate.

## Naming consequence

Because the final scope includes Arts and Humanities, Social Sciences, Business, Psychology, Nursing, Health Professions, and the natural sciences, wording such as **China-based scholarly system** or **Chinese scholarship** is more accurate than implying a natural-science-only population.

## Gate consequence

**All-field disciplinary scope: PASS.**

Primary disciplinary scope is no longer TBF.
