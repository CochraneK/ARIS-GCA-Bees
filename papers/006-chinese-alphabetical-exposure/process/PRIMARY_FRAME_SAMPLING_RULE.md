# ARIS4C006 · Frozen primary focal-work sampling rule

Last updated: 2026-09-19

## Purpose

Define the confirmatory work-level analysis frame before any H1/H2 coefficient is calculated.

The complete OpenAlex universe is too large to reconstruct every byline through Crossref. The primary mechanism therefore uses reproducible, field-year-stratified random sampling with fixed structural eligibility rules.

## Strata

Primary strata:

**26 OpenAlex `primary_topic.field.id` fields × focal years 2011–2025**

Total potential strata:

**390 field-year cells**

## Target per stratum

Target:

**40 informative eligible works per field-year**

Target full design size if every cell reaches target:

- 15,600 work clusters;
- at least 31,200 focal authorship rows because each work must contain >=2 focal rows.

This design intentionally prevents the largest publication fields from numerically dominating the cross-field mechanism estimate.

## Reproducible sampling

For each field-year:

- draw OpenAlex random blocks of up to 100 works;
- fixed deterministic seeds derived from paper ID, field, year, and block;
- process blocks in numerical order;
- deduplicate by work ID;
- stop after the first completed block that yields >=40 informative eligible works;
- maximum **5 blocks**.

No surname-effect coefficient or downstream outcome is inspected during sampling.

## Structural work eligibility

A primary work must:

1. be type `article` or `conference-paper`;
2. have at least one CN-affiliated authorship;
3. have the stratum's unique `primary_topic.field.id`;
4. have 2–99 OpenAlex authorships;
5. have a DOI resolving in Crossref;
6. have matching OpenAlex/Crossref author counts;
7. have a reliable whole-team alphabetical ordering key for every listed author;
8. pass strict positional family-name compatibility;
9. have current canonical author IDs for focal authors;
10. contain at least **2 focal CN-affiliated ChineseNames × CCNC surname-mappable authorships**;
11. contain nonzero within-work variation in focal `RelAlphaRank`;
12. later receive a valid frozen LOAO exposure with `D^{-i}_{ct} >= 50` for each retained focal row.

Works with >=100 OpenAlex authorships are excluded because OpenAlex caps the inline authorship list at 100.

## Focal surname eligibility

Primary focal surname map:

`aris4c006-surname-map-v2-ccnc`

A focal row uses:
- direct Han intersection route; or
- exact canonical Romanized surname form route;

under `SURNAME_ROMANIZATION_RULE.md`.

Legacy/regional aliases and last-token guesses remain excluded.

## Relative alphabetical rank

For each focal author, `RelAlphaRank` is calculated against the **entire reconstructed byline**, not only the focal Chinese-surname subset.

Ties use midrank.

A work in which all focal rows have the same relative alphabetical rank provides no within-work mechanism variation and is not counted toward the target 40 informative works.

## Minimum cell support

After 5 blocks:

- **>=40 informative works**: target met;
- **20–39**: retain all available works and flag the cell as below target;
- **<20**: exclude the field-year cell from the primary confirmatory work-FE frame.

The threshold is structural and fixed before H1/H2.

## Weighting / estimand

Primary sampled design is intentionally approximately **field-year balanced**, not publication-volume representative.

Primary interpretation:

> the average within-work institutional alphabetization mechanism across eligible field-year contexts in China's research system.

A publication-volume-weighted estimate may be reported only as a prespecified secondary sensitivity and cannot replace the primary because it is larger or more significant.

## Outcome-blind frame materialization

Before preregistration unlock, materialization may report:

- raw works sampled;
- DOI/Crossref reconstruction coverage;
- eligible informative works per field-year;
- focal rows;
- unique canonical authors;
- team-size distribution;
- field-year cluster count;
- exclusion-reason counts;
- LOAO exposure-support coverage.

It may not report:
- H1/H2 coefficients;
- surname-rank × outcome associations;
- p-values or confidence intervals for focal effects.

## Power safeguard

If the outcome-blind materialized frame has:
- fewer than 250 eligible field-year clusters; or
- fewer than 8,000 informative work clusters; or
- fewer than 16,000 focal rows;

the confirmatory work-level analysis remains locked pending a documented power/design reassessment.

Any sampling increase must be decided using counts/power only, before focal coefficients are opened.
