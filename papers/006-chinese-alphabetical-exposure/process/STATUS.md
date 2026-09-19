# ARIS4C006 STATUS

Last updated: 2026-09-19

## Current state

**RESEARCH-DESIGN — all outcome-blind execution gates passed; preregistration lock ready**

The scientific design has passed feasibility/identification gates and `paper.json` is now `research-design`.

**Confirmatory outcomes remain locked.** No focal surname × outcome coefficient may be inspected until the remaining outcome-blind implementation gates pass and the preregistration lock/hash is created.

## Canonical question

Within China's research system, does an author's relative alphabetical surname position become more predictive of listed byline position specifically when the field has a stronger independently measured prior convention of alphabetical authorship?

## Frozen design

- Primary mechanism unit: focal authorships within the same eligible multi-author work.
- Primary population language: CN-affiliated authorships with validated ChineseNames × CCNC focal surname forms; no nationality/ethnicity inference.
- Work types: `article` + `conference-paper`.
- Time window: **2011–2025**.
- Field assignment: OpenAlex `primary_topic.field.id`.
- Scope: all **26 current OpenAlex fields** globally eligible.
- Primary exposure: primary-topic field × prior 3 complete years.
- Exposure estimator: exact chance correction + exact leave-one-author-out; require `D^{-i}_{ct} >= 50`.
- Raw source/journal exposure: not primary; secondary/exploratory only after shrinkage.
- Primary predictor: within-team `RelAlphaRank`.
- Primary outcome: normalized listed byline position.
- Primary model: work fixed effects with `RelAlphaRank × LOAOExposure`.
- Inference: three-way clustering by canonical author, work, and primary-field × year.
- Surname population weights: ChineseNames 2025.8.
- Surname pronunciation/order authority: pinned CCNC surname lexicon.
- Primary surname map: `aris4c006-surname-map-v2-ccnc`.
- Corrected mapped population denominator: **1,181,331,391 (99.9671%)**.
- Corrected population-weighted initial rank: **16.25491**.
- Longitudinal entry cohort: **2014–2020**, 3-year clean lookback, 5-year follow-up.
- Distal confirmatory endpoint: observed five-year publication persistence.
- Within-author exposure variation gate: passed.

## Major passed gates

- [x] novelty narrowed against Einav & Yariv, Li & Yi, D'Angelo, Crabtree/Holbein/Tsutsui and 2025–2026 adjacent work;
- [x] 1,806-surname population baseline established;
- [x] Crossref structured-family route validated;
- [x] randomized surname measurement gate passed;
- [x] OpenAlex author-ID canonicalization rule validated;
- [x] all-field alphabetization heterogeneity exists;
- [x] raw source-level primary exposure rejected by prospective reliability rule;
- [x] field × prior-3-year exposure frozen as primary;
- [x] all 26 fields passed primary-topic eligibility;
- [x] all-field historical coverage froze 2011–2025;
- [x] within-author exposure variation passed;
- [x] CCNC surname-specific Romanization gate passed;
- [x] corrected CCNC-based population baseline materialized;
- [x] survivor-selected 2024 pilot forbidden as confirmatory cohort;
- [x] entry-based longitudinal cohort/persistence endpoint frozen;
- [x] primary work types, multiplicity and cluster structure frozen;
- [x] machine-readable design/outcome locks exist.

## Remaining outcome-blind execution gates

1. [x] reproduce ChineseNames baseline from the official **2025.8 R-universe source package** (Pilot 18 PASS);
2. [x] materialize final 26-field primary convention/exposure build under article+conference-paper types (PASS under frozen execution thresholds);
3. [x] validate LOAO implementation against synthetic/hand-computed cases (PASS);
4. [x] run a synthetic-only work-FE + interaction + frozen multiway-cluster smoke test (PASS);
5. [x] materialize the primary work frame and report only sample/cluster/exclusion counts, **without estimating H1/H2** (PASS under frozen execution thresholds);
6. [x] finalize deterministic longitudinal identity-risk QA flags and report prevalence only (120/120 hard-QA pass; low-risk=91; ORCID-anchored=92; no persistence/effect opened);
7. [ ] run the now-unblocked preregistration consistency audit, generate lock/hash, then explicitly unlock confirmatory outcomes.

## Hard rules

- Do not use uniform A–Z as a Chinese surname null.
- Do not use legacy ChineseNames `initial` as surname-pronunciation truth.
- Do not use generic pypinyin as confirmatory surname pronunciation.
- Do not use unreviewed Lee/Chan/Wong/etc. aliases in the primary sample.
- Do not use raw embedded OpenAlex author IDs for longitudinal joins; canonicalize first.
- Do not use `topics.field.id` as primary field assignment.
- Do not promote raw source-level exposure because it yields a stronger result.
- Do not use last-token surname heuristics to increase sample size.
- Do not inspect focal surname × outcome coefficients before the preregistration lock is complete.

## Next checkpoint

When all remaining execution gates pass, create a deterministic preregistration lock/hash, update `DESIGN_GATES.json` and `ANALYSIS_SPEC.json`, then promote the project to `preregistered` and only then allow confirmatory H1/H2/H3 execution.
