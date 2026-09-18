# ARIS4C015 SciSciNet-v2 Mechanism Query Protocol

Updated: 2026-09-18

## Goal

Build a large retrospective candidate pool that is enriched for genuine
Sleeping Beauties without pretending that a cheap metric prefilter is already a
confirmed mechanism label.

Official SciSciNet-v2 access currently includes:

- Google BigQuery;
- Cloud Storage;
- Hugging Face;
- approximately 250M papers;
- approximately 2.5B citation edges;
- precomputed science-of-science metrics.

The official BigQuery example uses:

ksm-rch-scisciturbo.sciscinet_v2.sciscinet_papers

Because schema details can change, ARIS4C015 must inspect the live schema before
issuing a mechanism query.

## Step 0 — Schema discovery

Run in BigQuery:

    SELECT
      column_name,
      data_type
    FROM
      `ksm-rch-scisciturbo.sciscinet_v2.INFORMATION_SCHEMA.COLUMNS`
    WHERE
      table_name = 'sciscinet_papers'
      AND column_name IN (
        'paperid',
        'year',
        'SB_B',
        'SB_T',
        'cited_by_count',
        'Citation_Count',
        'C3',
        'C5',
        'C10',
        'reference_count',
        'Reference_Count'
      )
    ORDER BY column_name;

Do not assume that a v1 column name is unchanged in v2 merely because the
metric exists.

## Step 1 — Cheap SB candidate prefilter

If SB_B and cited_by_count are present, an exploratory candidate query is:

    SELECT
      paperid,
      year,
      SB_B,
      SB_T,
      cited_by_count,
      C3,
      C5,
      C10
    FROM
      `ksm-rch-scisciturbo.sciscinet_v2.sciscinet_papers`
    WHERE
      year BETWEEN 1970 AND 1995
      AND SB_B > 33
      AND cited_by_count >= 50
    ORDER BY
      SB_B DESC;

Rationale:

- B > 33 is a SciSciNet-v1 source-calibrated reference corresponding roughly
  to the top 2% SB region in that published corpus;
- cited_by_count >= 50 is a recognition floor;
- neither criterion confirms a Sleeping Beauty.

Before using B > 33 as a v2 mechanism threshold:

1. estimate the v2 B distribution by field/cohort;
2. report how the v1 threshold maps onto v2;
3. run sensitivity around percentile-based and absolute-B definitions.

## Step 2 — Extreme-case calibration set

For a smaller high-confidence audit set:

    SELECT
      paperid,
      year,
      SB_B,
      SB_T,
      cited_by_count
    FROM
      `ksm-rch-scisciturbo.sciscinet_v2.sciscinet_papers`
    WHERE
      year BETWEEN 1970 AND 1995
      AND SB_B > 307.55
      AND cited_by_count >= 50
    ORDER BY
      SB_B DESC;

B > 307.55 is a SciSciNet-v1 high-B reference used for its top-10,000 group.
It is not a universal cutoff.

This set is useful for:
- manual audit;
- implementation checks;
- Prince-case inspection;
- cross-source validation.

It should not replace the broader mechanism cohort.

## Step 3 — Build field/cohort controls

For each candidate field × publication-year stratum, retrieve a sufficiently
large comparison pool without filtering on future trajectory.

Required metadata where available:

- paperid;
- publication year;
- field/subfield;
- reference count;
- author count;
- source/journal ID;
- document type;
- citation-history reconstruction keys.

The controls must include potential:

- FORGOTTEN;
- IMMEDIATE_HIT;
- FADING;
- AMBIGUOUS papers.

Do not select controls by present-day prestige.

## Step 4 — Reconstruct complete annual citation histories

SB_B is only a prefilter.

For every candidate and selected control:

1. retrieve incoming citation edges;
2. join citing paper to publication year;
3. aggregate annual citations;
4. explicitly insert zero-citation years;
5. preserve invalid prepublication edges separately;
6. record source/version/snapshot.

Then run:

- Beauty Coefficient implementation;
- awakening time;
- van-Raan-style sleep/depth/wake gate;
- later-recognition floor;
- robust-SB convergence rule.

Only after this step can a primary mechanism case be labeled
SLEEPING_BEAUTY.

## Step 5 — Normalize trajectory state within field/cohort

For each field × publication-year stratum:

- early attention = first 5-year citation total percentile;
- late attention = final 5-year citation total percentile.

Default states:

- low early / high late + robust SB -> SLEEPING_BEAUTY;
- low early / low late -> FORGOTTEN;
- high early / high late -> IMMEDIATE_HIT;
- high early / low late -> FADING;
- otherwise -> AMBIGUOUS.

A low-early/high-late paper failing the robust gate remains
LOW_EARLY_HIGH_LATE_UNCONFIRMED.

## Step 6 — Mechanism matching

Primary match:

SLEEPING_BEAUTY vs FORGOTTEN

Default:
- same field;
- same publication year;
- early citation percentile caliper;
- nearest reference count;
- nearest author count;
- nearest early citation count;
- no replacement.

Secondary match:

SLEEPING_BEAUTY vs IMMEDIATE_HIT

Same field/year, but do not match away the early-attention contrast.

## Step 7 — Audit before mechanism analysis

Required report:

- candidate count after cheap prefilter;
- robust-SB pass rate;
- SB count by field/cohort;
- number and percentage of unmatched SBs;
- standardized differences / balance on early-life covariates;
- threshold sensitivity;
- source coverage;
- missing metadata;
- self-citation policy when available.

If robust SB count is zero:

mechanism_ready = false

Do not continue to mechanism modeling.

## Step 8 — Mechanism features

Only after the mechanism cohort exists:

- contemporaneous reference combinations;
- bibliographic coupling;
- network brokerage;
- semantic distance to contemporaneous field;
- later field-readiness shift;
- candidate Prince papers;
- co-citation growth;
- patent / technology linkage;
- 011 integrity/provenance state.

Mechanism features are outcomes/explanatory variables for Track M.

When reused as predictors in Track B, they must be reconstructed using only
information available by the historical cutoff.

## Reproducibility manifest

Every exported query/slice should record:

- SciSciNet version;
- BigQuery dataset/table or GCS object;
- query text;
- query date;
- row count;
- field/year filters;
- SB_B threshold;
- recognition floor;
- code commit;
- checksum or stable export identifier where feasible.

## Scale strategy

Do not download the entire 250M-paper / 2.5B-edge lake solely to test the
mechanism code.

Preferred sequence:

1. schema discovery;
2. candidate count query;
3. bounded field/cohort export;
4. robust-SB gate;
5. matching-yield audit;
6. expand only after the bounded cohort works.
