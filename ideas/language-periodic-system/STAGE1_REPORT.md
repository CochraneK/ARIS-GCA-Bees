# Stage-1 Report · Periodic vs Non-Periodic Geometry

**Verdict:** `REFRAME_NONPERIODIC_GEOMETRY`

This is a **screening model competition**, not a confirmatory periodicity claim.

## Data and target

Languages: 644 · features: 60

Each model is fit to the feature-feature NMI matrix computed in training languages and predicts the independently computed NMI matrix in held-out languages.

## Random language splits

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| null | 0.000 | 0.000 | 0.042 | 0.021 |
| lowrank2 | 0.172 | 0.398 | 0.043 | 0.026 |
| euclidean2d | 0.122 | 0.138 | 0.042 | 0.021 |
| tree | 0.199 | 0.530 | 0.037 | 0.020 |
| graph | 0.205 | 0.364 | 0.040 | 0.022 |
| circular | 0.122 | 0.169 | 0.042 | 0.022 |

Circular-order stability vs full-data reference: 0.654 ± 0.094

## Family-held-out splits

Entire top-level Glottolog families are assigned to test when sampled, reducing direct genealogical leakage.

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| null | 0.000 | 0.000 | 0.045 | 0.023 |
| lowrank2 | 0.150 | 0.344 | 0.046 | 0.028 |
| euclidean2d | 0.150 | 0.144 | 0.044 | 0.023 |
| tree | 0.178 | 0.477 | 0.040 | 0.022 |
| graph | 0.163 | 0.319 | 0.043 | 0.024 |
| circular | 0.109 | 0.163 | 0.044 | 0.023 |

Circular-order stability vs full-data reference: 0.542 ± 0.139

## Automated interpretation

- Circular Spearman: random=0.122, family-held-out=0.109.
- Best non-periodic family-held-out Spearman=0.178; null=0.000.
- Mean circular-order stability under family-held-out resampling=0.542.

## Claim boundary

A circular model performing well here would show that a simple periodic representation captures reproducible association structure. It would still **not** establish a chemical-style periodic table, linguistic atoms, causal universals, or independence from geography. A confirmatory paper would need capacity checks, geographic controls, source-domain replications, stronger family/phylogenetic treatment, and an independent ARIS review.

## Prior-art boundary

Persistent H1 loops are not treated as novelty because Port et al. (2018, 2022) already applied persistent topology to syntactic-parameter data. The intended novelty is explicit predictive model competition for the periodic-table hypothesis on modern curated global data.
