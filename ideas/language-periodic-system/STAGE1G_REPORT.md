# Stage-1G · Geographic Collapse Calibration

**Verdict:** `GEOGRAPHIC_HETEROGENEITY_CONFIRMED`

Features: 40 · matched random test sets per block: 8

## Macroarea

| Block | Test n | Geo train↔test Spearman | Matched-random mean | Geo − random |
|---|---:|---:|---:|---:|
| Africa | 102 | 0.083 | 0.337 | -0.254 |
| Australia | 65 | 0.060 | 0.363 | -0.303 |
| Eurasia | 112 | 0.106 | 0.356 | -0.250 |
| North America | 126 | 0.094 | 0.369 | -0.276 |
| South America | 161 | 0.100 | 0.391 | -0.291 |

Across blocks: geographic mean=0.088; matched-random mean=0.363; mean difference=-0.275; fraction geo below random=1.00.

## Spatial clusters

| Block | Test n | Geo train↔test Spearman | Matched-random mean | Geo − random |
|---|---:|---:|---:|---:|
| cluster_0 | 102 | 0.133 | 0.322 | -0.189 |
| cluster_1 | 167 | 0.116 | 0.400 | -0.284 |
| cluster_2 | 145 | 0.138 | 0.377 | -0.239 |
| cluster_3 | 121 | 0.092 | 0.336 | -0.245 |
| cluster_4 | 109 | 0.050 | 0.322 | -0.272 |

Across blocks: geographic mean=0.106; matched-random mean=0.351; mean difference=-0.246; fraction geo below random=1.00.

## Claim boundary

Matched-size random calibration isolates test-set size as a simple alternative explanation, but it does not itself identify causal areal transmission or separate geography from historically correlated population structure.
