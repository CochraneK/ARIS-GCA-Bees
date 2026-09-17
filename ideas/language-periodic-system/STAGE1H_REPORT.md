# Stage-1H · GBI Curation Replication

**Verdict:** `TREE_REPLICATES_OVER_CIRCULAR__WEAK_CROSS_MACROAREA_TRANSFER`

Languages: 1140 · selected features: 60

## Family-held-out model comparison

| Model | Spearman mean ± SD |
|---|---:|
| lowrank2 | 0.098 ± 0.034 |
| tree | 0.122 ± 0.038 |
| euclidean_connected | 0.035 ± 0.023 |
| circular_optimized | 0.073 ± 0.036 |

Tree − circular mean difference: **0.049**; tree win fraction: **1.00**.

## Macroarea association transfer

| Macroarea | Test n | Train↔test association Spearman |
|---|---:|---:|
| Africa | 212 | 0.132 |
| Eurasia | 301 | 0.097 |
| North America | 213 | 0.118 |
| Papunesia | 177 | 0.207 |
| South America | 172 | 0.165 |

Mean cross-macroarea association transfer: **0.144 ± 0.043**.

## Claim boundary

GBI is an alternative dependency-curation/representation, not a fully independent typological source from TLI. Agreement strengthens robustness to curation choice but does not constitute external-dataset replication.
