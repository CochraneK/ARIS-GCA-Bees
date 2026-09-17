# Stage-0 Pilot Report · Language Periodic System

**Verdict:** `MIXED_SIGNAL`

This is a prerequisite test, **not evidence of periodicity by itself**.

## Data

TLI-statistical densified-small from Graff et al. (2025), combining cross-linguistic structural information curated to reduce logical and very strong statistical feature dependencies.

## Compression test

Languages: 644 · selected features: 120

| Components | Observed cumulative variance | Null mean | Observed − null |
|---:|---:|---:|---:|
| 10 | 0.344 | 0.199 | +0.145 |
| 20 | 0.510 | 0.362 | +0.148 |
| 50 | 0.783 | 0.700 | +0.083 |

## Residual association test

Feature pairs tested: 3143

| Statistic | Observed NMI | Permutation null |
|---|---:|---:|
| Median | 0.007 | 0.003 |
| 90th percentile | 0.037 | 0.016 |
| 99th percentile | 0.119 | 0.039 |

## Interpretation

- 20-component compression exceeds shuffled-null mean by 0.148.
- 90th-percentile residual NMI (0.037) is not clearly separated from null (0.016).

Even a strong Stage-0 result would only justify Stage 1: explicit held-out comparison of periodic/circular/toroidal models against factor, hierarchy, graph/manifold, and null alternatives, ideally with phylogenetic and geographic controls.

## Caveats

The compression analysis uses mode imputation and is sensitive to missing-data structure. Pairwise NMI does not control for genealogical or geographic non-independence. These are deliberate screening tests; confirmatory claims require the later controlled analysis.
