# Stage-1B Robustness · Is the Circular Model a Strawman?

**Verdict:** `MIXED_ROBUSTNESS`

This analysis gives the periodic hypothesis a more favorable/fair test before interpreting Stage 1's negative screen.

## What changed

- A tiny positive affinity floor forces the spectral graph to be connected.
- A directly optimized circular model learns one angular coordinate per feature and refits a two-harmonic circular kernel.
- Fits use only training-language associations; test-language associations are used only for evaluation.
- Results are repeated at two feature counts under top-level Glottolog family hold-out.

## 40 features

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.223 ± 0.039 | 0.303 | 0.053 | 0.028 |
| euclidean_connected | 0.217 ± 0.070 | 0.157 | 0.041 | 0.020 |
| tree | 0.178 ± 0.008 | 0.349 | 0.041 | 0.019 |
| circular_connected | 0.183 ± 0.043 | 0.178 | 0.041 | 0.020 |
| circular_optimized | 0.179 ± 0.025 | 0.216 | 0.041 | 0.020 |

Optimized circular-order stability: 0.419 ± 0.112

## 60 features

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.153 ± 0.035 | 0.326 | 0.045 | 0.027 |
| euclidean_connected | 0.102 ± 0.049 | 0.125 | 0.042 | 0.022 |
| tree | 0.147 ± 0.036 | 0.446 | 0.039 | 0.021 |
| circular_connected | 0.106 ± 0.020 | 0.170 | 0.042 | 0.022 |
| circular_optimized | 0.105 ± 0.021 | 0.167 | 0.042 | 0.022 |

Optimized circular-order stability: 0.628 ± 0.081

## Automated interpretation

- 40 features: optimized circular Spearman=0.179, tree=0.178, connected Euclidean=0.217, circular stability=0.419.
- 60 features: optimized circular Spearman=0.105, tree=0.147, connected Euclidean=0.102, circular stability=0.628.

## Claim boundary

A negative verdict here strengthens—but does not complete—the case against a simple global periodic geometry. Geographic blocking, stronger phylogenetic treatment, model-capacity analysis, and replication remain necessary before manuscript-level rejection. A positive verdict would only reopen the periodic hypothesis; it would not establish a chemical-style periodic table.
