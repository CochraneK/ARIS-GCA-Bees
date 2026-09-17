# Stage-1C · Pre-defined Domain Test for Local Periodicity

**Overall verdict:** `NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`

Domains are defined from the TLI authors' `grouping` metadata before model comparison; no domain is selected because it happened to look circular.

## Grammar_linear_order

Features: 14 · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.434 ± 0.085 | 0.646 | 0.137 | 0.108 |
| euclidean_connected | 0.256 ± 0.122 | 0.625 | 0.108 | 0.070 |
| tree | 0.435 ± 0.080 | 0.755 | 0.091 | 0.063 |
| circular_equal_spaced | 0.314 ± 0.036 | 0.474 | 0.121 | 0.075 |
| circular_optimized | 0.285 ± 0.134 | 0.539 | 0.118 | 0.079 |

Optimized circular-order stability: 0.790 ± 0.158

## Grammar_other

Features: 38 · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.290 ± 0.049 | 0.788 | 0.071 | 0.042 |
| euclidean_connected | 0.120 ± 0.152 | 0.210 | 0.104 | 0.048 |
| tree | 0.394 ± 0.088 | 0.735 | 0.074 | 0.038 |
| circular_equal_spaced | 0.213 ± 0.011 | 0.292 | 0.102 | 0.048 |
| circular_optimized | 0.138 ± 0.049 | 0.352 | 0.100 | 0.049 |

Optimized circular-order stability: 0.516 ± 0.165

## Grammatical_categories

Features: 23 · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | -0.009 ± 0.000 | 0.565 | 0.083 | 0.059 |
| euclidean_connected | 0.304 ± 0.000 | 0.336 | 0.058 | 0.029 |
| tree | -0.085 ± 0.000 | 0.673 | 0.049 | 0.031 |
| circular_equal_spaced | 0.212 ± 0.000 | 0.253 | 0.059 | 0.029 |
| circular_optimized | 0.083 ± 0.000 | 0.239 | 0.060 | 0.034 |

Optimized circular-order stability: 0.149 ± 0.000

## Lexical

Features: 18 · domain verdict: `AMBIGUOUS_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.153 ± 0.000 | 0.886 | 0.063 | 0.040 |
| euclidean_connected | 0.286 ± 0.000 | 0.380 | 0.089 | 0.044 |
| tree | 0.389 ± 0.000 | 0.807 | 0.057 | 0.033 |
| circular_equal_spaced | 0.236 ± 0.000 | 0.407 | 0.088 | 0.043 |
| circular_optimized | 0.346 ± 0.000 | 0.533 | 0.083 | 0.040 |

Optimized circular-order stability: 0.371 ± 0.000

## Phonology

Features: 40 · domain verdict: `NONPERIODIC_DOMAIN`

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.218 ± 0.026 | 0.243 | 0.057 | 0.035 |
| euclidean_connected | 0.207 ± 0.080 | 0.173 | 0.044 | 0.023 |
| tree | 0.257 ± 0.036 | 0.348 | 0.043 | 0.022 |
| circular_equal_spaced | 0.127 ± 0.017 | 0.144 | 0.045 | 0.024 |
| circular_optimized | 0.158 ± 0.031 | 0.183 | 0.044 | 0.023 |

Optimized circular-order stability: 0.452 ± 0.091

## Interpretation rule

A `LOCAL_PERIODIC_CANDIDATE` is only a candidate module for confirmatory testing. It requires periodic Spearman ≥ 0.15, within 0.03 of the best non-periodic baseline, and circular-order stability ≥ 0.40. This deliberately does not call a domain periodic merely because a circular fit is non-zero.

## Claim boundary

This is exploratory module-level screening. Multiple-domain testing, geography, full phylogenetic dependence, circular-seriation goodness-of-fit, and replication must be handled before a local-periodicity claim enters a paper.
