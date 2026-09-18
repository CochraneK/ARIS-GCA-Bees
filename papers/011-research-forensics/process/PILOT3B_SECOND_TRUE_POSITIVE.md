# Pilot 3B — second pre-outcome real true-positive

Updated: 2026-09-18

## Target

- DOI: 10.1371/journal.pone.0293412
- publication: 2023-10-26
- later correction: 10.1371/journal.pone.0317174, published 2025-01-03

## Time-safe target artifact

Humboldt-Universität zu Berlin's institutional repository stores `journal.pone.0293412.pdf` under a record dated 2023-10-26, the article publication date, and links the publisher DOI.

The stored publisher PDF is 893,239 bytes and has SHA-256:

`95460abea1594e8f8f1aec4e8fb029df0e0faacf4e7244ba7ddb25dc7eefe60b`

On 2026-09-18 the PLOS printable PDF had exactly the same byte length and SHA-256. The publication-day repository copy is therefore qualified as SAFE_EXACT for the Table 1 role.

Historical Table 1 reports Survey 1 Mexico as:

- count = 16
- proportion = 4.5%

## Contemporaneous raw data

The public OSF node `nf4x7` contains `survey1_ratings.csv` (GUID `t5muj`).

OSF metadata:
- current version: 1
- created: 2023-07-28T22:30:28.355281Z
- last modified: 2023-07-28T22:30:28.355281Z
- rows: 353
- SHA-256: `90f86ae54abb67e980a3379bfc95ab796fb9ebfe1ea9580fa4afde8743a035bb`

The complete country frequency table contains 64 distinct raw strings and sums to N=353.

## Prespecified recomputation

The detector uses only a minimal normalization:
- Unicode NFKD decomposition;
- remove diacritics;
- collapse whitespace;
- casefold.

For the explicit alias `mexico`, the raw values are:
- Mexico = 11
- México = 5
- MÉXICO = 1

Therefore:
- recomputed count = 17
- recomputed proportion = 17 / 353 = 4.8% to one decimal place

Historical table:
- 16 / 4.5%

Result:
- **FLAG**
- evidence class: E1
- review priority: MODERATE
- misconduct inference: false

The 2025 correction later independently states that Mexico should be 17 / 4.8% and Other should be 87. The correction is ground truth only; it is not detector input.

## Compensating-error finding

The historical table itself does not expose the error through ordinary arithmetic:
- displayed counts sum to 353;
- displayed percentages sum to 100.0%.

Mexico is lower by one while Other is higher by one. The paired errors compensate, so an internal table-sum detector can PASS.

This makes the case a real demonstration of detector complementarity: raw-data-to-table consistency identifies an issue that within-table arithmetic does not.

## Deliberate abstention from full recoding

We do not infer the full country-grouping rule. Obvious UK variants in the raw field sum to 78 whereas the historical table reports 79, implying at least one undocumented grouping choice. Rather than guess which value was grouped into the UK category, the confirmatory check is restricted to the unambiguous Mexico variants.

## Interpretation

This is the second development-stage pre-outcome true-positive and the first one based on deposited raw data. Together with Pilot 2B, it shows two different time-safe evidence routes:

1. target table ↔ contemporaneous cited paper;
2. target table ↔ contemporaneously deposited raw data.

Two cases are still insufficient for any sensitivity, precision, or superiority estimate.
