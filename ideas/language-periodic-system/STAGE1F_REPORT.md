# Stage-1F · Repeated Family-Held-Out Uncertainty

**Verdict:** `TREE_ADVANTAGE_STABLE`

Valid splits: 20/20 attempts · features: 60

## Model performance

| Model | Spearman mean ± SD | Range |
|---|---:|---:|
| lowrank2 | 0.155 ± 0.034 | 0.103 to 0.237 |
| tree | 0.182 ± 0.047 | 0.081 to 0.272 |
| euclidean_connected | 0.110 ± 0.053 | 0.015 to 0.212 |
| circular_optimized | 0.109 ± 0.030 | 0.051 to 0.163 |

## Paired contrasts

| Contrast | Mean | 95% bootstrap CI | Win fraction |
|---|---:|---:|---:|
| tree_minus_circular | 0.073 | [0.055, 0.092] | 1.00 |
| lowrank_minus_circular | 0.046 | [0.033, 0.061] | 0.95 |
| euclidean_minus_circular | 0.001 | [-0.020, 0.021] | 0.65 |

The primary contrast is tree minus optimized circular performance on the same held-out-family split. A CI wholly above zero supports a stable tree advantage; a CI crossing zero means the ranking remains split-sensitive.

## Claim boundary

Bootstrap resamples held-out split results, not languages or phylogenetic trees; it quantifies split sensitivity but is not a full phylogenetic uncertainty model.
