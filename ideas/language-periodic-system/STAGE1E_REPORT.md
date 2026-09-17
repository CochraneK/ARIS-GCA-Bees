# Stage-1E · Geography-Aware Validation

**Verdict:** `MIXED_GEOGRAPHIC_GENERALIZATION`

Two outcome-blind geographic partitions are used: Glottolog Macroareas and five latitude/longitude clusters on the unit sphere. `geo_plus_family` additionally removes from training every top-level family represented in the test block.

## macroarea

| Block | Test n | Geo-only? | Joint geo+family? |
|---|---:|---:|---:|
| Africa | 102 | yes | yes |
| Australia | 65 | yes | yes |
| Eurasia | 112 | yes | yes |
| North America | 126 | yes | yes |
| South America | 161 | yes | yes |

### geo_only

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.043 ± 0.059 | 0.026 | 0.207 | 0.116 |
| euclidean_connected | 0.006 ± 0.122 | 0.008 | 0.203 | 0.111 |
| tree | 0.032 ± 0.029 | 0.111 | 0.203 | 0.111 |
| graph | 0.051 ± 0.028 | 0.081 | 0.204 | 0.112 |
| circular_optimized | 0.008 ± 0.090 | 0.005 | 0.203 | 0.111 |

### geo_plus_family

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.043 ± 0.060 | 0.026 | 0.207 | 0.116 |
| euclidean_connected | 0.003 ± 0.123 | 0.008 | 0.203 | 0.111 |
| tree | 0.056 ± 0.048 | 0.109 | 0.204 | 0.111 |
| graph | 0.056 ± 0.025 | 0.079 | 0.204 | 0.112 |
| circular_optimized | -0.000 ± 0.097 | 0.011 | 0.203 | 0.111 |

## spatial_cluster

| Block | Test n | Geo-only? | Joint geo+family? |
|---|---:|---:|---:|
| cluster_0 | 102 | yes | yes |
| cluster_1 | 167 | yes | yes |
| cluster_2 | 145 | yes | yes |
| cluster_3 | 121 | yes | yes |
| cluster_4 | 109 | yes | yes |

### geo_only

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.082 ± 0.091 | 0.040 | 0.120 | 0.043 |
| euclidean_connected | 0.077 ± 0.091 | 0.034 | 0.116 | 0.038 |
| tree | 0.059 ± 0.056 | 0.117 | 0.116 | 0.038 |
| graph | 0.051 ± 0.032 | 0.072 | 0.117 | 0.040 |
| circular_optimized | 0.042 ± 0.064 | 0.045 | 0.116 | 0.038 |

### geo_plus_family

| Model | Spearman | Pearson | RMSE | MAE |
|---|---:|---:|---:|---:|
| lowrank2 | 0.085 ± 0.079 | 0.039 | 0.120 | 0.043 |
| euclidean_connected | 0.070 ± 0.096 | 0.024 | 0.116 | 0.038 |
| tree | 0.061 ± 0.058 | 0.120 | 0.116 | 0.038 |
| graph | 0.049 ± 0.047 | 0.071 | 0.117 | 0.040 |
| circular_optimized | 0.039 ± 0.062 | 0.032 | 0.116 | 0.038 |

## Automated interpretation

- macroarea_geo: circular=0.008; best non-periodic=graph 0.051; blocks=5.
- macroarea_joint: circular=-0.000; best non-periodic=graph 0.056; blocks=5.
- spatial_geo: circular=0.042; best non-periodic=lowrank2 0.082; blocks=5.
- spatial_joint: circular=0.039; best non-periodic=lowrank2 0.085; blocks=5.

## Claim boundary

Macroarea and coordinate-cluster hold-outs reduce direct areal leakage but do not model contact networks or phylogenetic covariance explicitly. The joint geo+family split is deliberately severe and may reduce training diversity. These are confirmatory-style robustness screens, not a full spatiophylogenetic model.
