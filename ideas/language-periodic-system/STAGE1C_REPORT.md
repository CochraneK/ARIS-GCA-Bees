# Stage-1C · Pre-defined Domain Test for Local Periodicity

**Overall verdict:** `NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`

Domains are defined from the TLI authors' `grouping` metadata before model comparison; no domain is selected because it happened to look circular.

Every reported domain contains exactly 4 valid family-held-out runs. Invalid draws with too few jointly observed feature pairs are rejected and resampled rather than silently reducing the replicate count.

## Grammar_linear_order

Features: 14 · valid splits: 4/20 attempts · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.493 ± 0.137 | 0.658 | 0.137 | 0.110 |
| euclidean_connected | 0.351 ± 0.214 | 0.658 | 0.108 | 0.071 |
| tree | 0.494 ± 0.134 | 0.755 | 0.092 | 0.064 |
| circular_equal_spaced | 0.396 ± 0.166 | 0.536 | 0.120 | 0.076 |
| circular_optimized | 0.401 ± 0.256 | 0.592 | 0.113 | 0.076 |

Optimized circular-order stability: 0.811 ± 0.136

## Grammar_other

Features: 38 · valid splits: 4/4 attempts · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.243 ± 0.125 | 0.732 | 0.064 | 0.039 |
| euclidean_connected | 0.028 ± 0.056 | 0.098 | 0.098 | 0.047 |
| tree | 0.313 ± 0.071 | 0.713 | 0.067 | 0.036 |
| circular_equal_spaced | 0.153 ± 0.078 | 0.286 | 0.096 | 0.045 |
| circular_optimized | 0.253 ± 0.075 | 0.412 | 0.092 | 0.045 |

Optimized circular-order stability: 0.274 ± 0.237

## Grammatical_categories

Features: 23 · valid splits: 4/8 attempts · domain verdict: `AMBIGUOUS_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.125 ± 0.052 | 0.307 | 0.091 | 0.061 |
| euclidean_connected | 0.181 ± 0.036 | 0.291 | 0.070 | 0.039 |
| tree | 0.229 ± 0.076 | 0.485 | 0.062 | 0.036 |
| circular_equal_spaced | 0.152 ± 0.085 | 0.304 | 0.070 | 0.039 |
| circular_optimized | 0.252 ± 0.114 | 0.378 | 0.069 | 0.038 |

Optimized circular-order stability: 0.373 ± 0.170

## Lexical

Features: 18 · valid splits: 4/13 attempts · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.220 ± 0.096 | 0.693 | 0.098 | 0.056 |
| euclidean_connected | 0.162 ± 0.093 | 0.284 | 0.122 | 0.057 |
| tree | 0.269 ± 0.088 | 0.680 | 0.096 | 0.045 |
| circular_equal_spaced | 0.126 ± 0.027 | 0.256 | 0.122 | 0.058 |
| circular_optimized | 0.142 ± 0.074 | 0.298 | 0.120 | 0.058 |

Optimized circular-order stability: 0.057 ± 0.101

## Phonology

Features: 40 · valid splits: 4/4 attempts · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.215 ± 0.022 | 0.331 | 0.052 | 0.033 |
| euclidean_connected | 0.171 ± 0.078 | 0.167 | 0.043 | 0.023 |
| tree | 0.229 ± 0.066 | 0.366 | 0.041 | 0.022 |
| circular_equal_spaced | 0.100 ± 0.018 | 0.170 | 0.043 | 0.023 |
| circular_optimized | 0.151 ± 0.018 | 0.228 | 0.042 | 0.023 |

Optimized circular-order stability: 0.550 ± 0.092

## Interpretation rule

A `LOCAL_PERIODIC_CANDIDATE` is only a candidate module for confirmatory testing. It requires periodic Spearman ≥ 0.15, within 0.03 of the best non-periodic baseline, and circular-order stability ≥ 0.40. This deliberately does not call a domain periodic merely because a circular fit is non-zero.

## Claim boundary

This is exploratory module-level screening. Multiple-domain testing, geography, full phylogenetic dependence, circular-seriation goodness-of-fit, and replication must be handled before a local-periodicity claim enters a paper.
