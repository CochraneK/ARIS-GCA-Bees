# PREREGISTRATION AMENDMENT 001 — implementation lock

**Date:** 2026-09-18  
**Outcome status at amendment:** real confirmatory country×discipline outcomes remain unopened.  
**Applies to:** `PREREGISTRATION_DRAFT.md` v0.1.

This amendment records implementation decisions discovered while building and synthetic-testing the pipeline. It is intentionally separate from the original draft so the decision trail remains visible.

## A1. Exposure standardization

The primary former-colony exposure remains `years_colonized_total` from COLDAT/OWID.

For the one-SD coefficient scale, compute the mean and population SD across the **COLDAT current-state source universe after excluding the eight European overseas colonial powers** (Belgium, United Kingdom, France, Germany, Netherlands, Portugal, Spain, Italy), before consulting contemporary disciplinary outcomes.

This source-universe scaling is then applied unchanged to all bibliometric periods. Outcome-dependent sample composition therefore does not redefine what "one SD of colonial duration" means.

The eight current-state ISO3 codes are frozen as:

`BEL, GBR, FRA, DEU, NLD, PRT, ESP, ITA`.

## A2. Country fractional-credit denominator

For a work with `n` distinct identifiable OpenAlex country codes across retained authorships, each identifiable country receives weight `1/n` **before** restriction to the COLDAT-anchored primary sovereign-state universe.

If a work contains an eligible primary-universe country plus a country/territory outside that universe, the eligible country's weight is not renormalized upward.

This rule is implemented in `code/materialize_openalex_cells.py`.

## A3. Dyadic multilateral-work weighting

For the collaboration outcome only, define the eligible country set as the distinct countries on the work that map into the frozen primary country universe.

If there are `n >= 2` mapped eligible countries, the work contributes total dyadic collaboration mass 1, divided equally among all `n(n-1)/2` unordered country pairs:

`pair_weight = 2 / [n(n-1)]`.

This differs intentionally from country-output fractional credit because the estimand is the distribution of collaboration ties **within the eligible dyadic analysis universe**.

The positive observed pair cells are materialized first; the CEPII-eligible pair×discipline×period grid is completed with genuine zeros before PPML.

Implemented in `code/materialize_openalex_dyads.py`.

## A4. OpenAlex schema gate

Before any outcome aggregation, run `code/probe_openalex_schema.py`. It may inspect field names/types and bind nested expressions but may not aggregate contemporary country×discipline performance.

Required nested bindings include:

- `primary_topic.subfield.id`;
- `primary_topic.field.id`;
- `authorships[].countries`;
- `citation_normalized_percentile.is_in_top_10_percent`.

If a future OpenAlex snapshot changes these fields, stop and record a schema amendment before changing extraction logic.

## A5. Hard outcome gate

`code/preoutcome_gate.py --strict` must pass before either OpenAlex outcome materializer runs.

At minimum this requires:

- independent blinded Coder B output;
- adjudicated `IKES_FROZEN.csv` and provenance;
- COLDAT-derived exposure table;
- audited primary country crosswalk;
- source manifest;
- frozen conceptual/discipline protocols;
- synthetic PPML design test.

The gate is an integrity control, not merely documentation.

## A6. IKES freezing rule

Coder A and independent Coder B are compared by `code/adjudicate_ikes.py`.

- Any missing pair or absolute cell disagreement >=2 requires explicit outcome-blind adjudication and a written note.
- Unflagged A/B cells use their arithmetic mean.
- `code/freeze_ikes.py` refuses to generate `IKES_FROZEN.csv` while a flagged cell remains unresolved.
- The frozen matrix receives a SHA-256 provenance record over Coder A, Coder B, adjudication input, and final output.

No contemporary performance data enter this process.

## A7. Inference warning from outcome-blind simulation

Synthetic PPML testing recovered the planted interaction correctly, including with non-integer fractional outcomes. However, the design has only 21 confirmatory discipline clusters.

Therefore:

1. two-way country×discipline cluster-robust uncertainty remains reported;
2. it is not treated as self-sufficient finite-sample calibration;
3. the confirmatory package also reports an IKES-label/discipline permutation falsification distribution and leave-one-discipline-out estimates;
4. imperial-center corroboration additionally uses leave-one-empire-out and no pseudo-large-N inference from repeated discipline observations.

The permutation analysis is described as a finite-field falsification/sensitivity analysis, not as exact randomized-treatment inference.

## A8. Historical dyad construction

CEPII Gravity V202211 is collapsed into an unordered modern-country dyad table after restriction to the primary current-state universe.

Primary historical pair variable: `col_dep_ever` = pair ever had a colonial/dependency relationship, including ties before 1948 according to CEPII documentation.

Preserved secondary variables where present include `sibling_ever`, common language, contiguity, distance, and independence/end-year information. Directional raw identifiers are retained in source provenance but the confirmatory collaboration outcome uses unordered pairs.

## A9. Gate status after this amendment

**Design:** effectively locked for implementation.  
**Outcomes:** remain locked.

External/local steps still required before unlock:

1. run truly independent Coder B in a fresh GPTPage/model context using `IKES_CODER_B_PACKET.md`;
2. adjudicate and freeze IKES;
3. acquire official COLDAT/CEPII/OpenAlex source files locally and record hashes;
4. build exposure and country/dyad crosswalk tables;
5. probe the exact downloaded OpenAlex Parquet schema.

None of these remaining steps justifies inspecting the substantive confirmatory result early.
