# Pilot 3C — third pre-outcome real true-positive

Updated: 2026-09-19

## Case

- target DOI: 10.1371/journal.pone.0180906
- publication: 2017-07-21
- correction DOI: 10.1371/journal.pone.0192570
- correction: 2018-02-05

## Time-safe artifact

Wayback captured the PLOS publisher HTML on 2017-07-24:

- timestamp: 20170724151640
- digest: MTJNXHVAUJZCTOAR47PRAO7AVYGIDJ7O
- roles: body_text, table_caption
- qualification: SAFE_EXACT

## Pre-outcome inconsistency

Within the same historical page:

- the Results text explicitly reports multiple-analysis household findings and points to Table 1;
- the Table 1 caption describes only univariate logistic regression analysis.

The F8 `cross_section_scope_coherence` detector consumes source-verified canonical scope labels and checks whether the caption covers the analysis scopes that the body explicitly attributes to that table.

Result:

- body scope: multiple_logistic_regression
- caption scope: univariate_logistic_regression
- missing caption scope: multiple_logistic_regression
- **FLAG**
- evidence class: E1
- review priority: MODERATE
- misconduct inference: false

The 2018 PLOS correction later independently states that the Table 1 caption was erroneous and supplies a corrected caption covering univariate and logistic regression analysis. The correction is ground truth only.

## Boundary: missing columns are not claimed as detected

The same correction says that two columns were missing from Table 1B. That is a separate sub-issue.

The 2017 historical HTML preserves the Table 1 link and caption, but not the table image object itself. Exact image CDX queries returned no pre-correction capture and timestamped replay returned 404.

Therefore:

- caption/scope sub-issue: SAFE_EXACT_READY → FLAG
- missing-columns sub-issue: BLOCKED_REQUIRED_ROLE

This is deliberate issue decomposition, not partial credit hidden inside one correction label.

## Why this matters

Pilot 3C establishes a third pre-outcome evidence route:

1. table ↔ cited source;
2. table ↔ deposited raw data;
3. body ↔ table caption / cross-section scope coherence.

Three development examples still do not estimate sensitivity or precision.
