# Paper 002 · Core Results Tables

These tables are manuscript-facing summaries. Source-of-truth numerical outputs remain the stage JSON files under `ideas/language-periodic-system/`.

## Table 1. Repeated TLI family-held-out model comparison

| Model | Spearman mean ± SD | Paired contrast vs optimized circle | Split-bootstrap 95% CI | Win fraction vs circle |
|---|---:|---:|---:|---:|
| Tree | **0.182 ± 0.047** | **+0.073** | **[0.055, 0.092]** | **1.00** |
| Low-rank (rank 2) | 0.155 ± 0.034 | +0.046 | [0.033, 0.061] | 0.95 |
| Euclidean connected | 0.110 ± 0.053 | +0.001 | [−0.020, 0.021] | 0.65 |
| Circular optimized | **0.109 ± 0.030** | reference | — | — |

**Interpretation:** intervals bootstrap split-level paired contrasts; they quantify split sensitivity, not phylogenetic uncertainty.

## Table 2. Cross-representation family-held-out ranking

| Representation | Languages | Features | Tree Spearman | Circular Spearman | Difference | Tree win fraction |
|---|---:|---:|---:|---:|---:|---:|
| TLI | 644 | 60 | **0.182** | 0.109 | +0.073 | 1.00 (20/20) |
| GBI | 1,140 | 60 | **0.122** | 0.073 | +0.049 | 1.00 |
| WALS | 2,659 | 30 | **0.603** | 0.410 | +0.193 | 1.00 (8/8) |

**Do not compare absolute effect magnitudes directly across rows.** Coverage, missingness, feature definitions and curation differ.

## Table 3. Direct circularity diagnostics

| Feature count | Circular row-unimodality violation ↓ | Tree-order violation ↓ | Random-order violation ↓ | Circular closure/internal-adjacency |
|---:|---:|---:|---:|---:|
| 40 | 0.222 ± 0.012 | 0.209 ± 0.011 | 0.237 ± 0.009 | 0.608 ± 0.764 |
| 60 | 0.297 ± 0.009 | 0.284 ± 0.010 | 0.307 ± 0.009 | **0.037 ± 0.091** |

The row-unimodality statistic is a noisy-data sensitivity inspired by circular-Robinson structure, not an exact recognition test. Closure is interpreted only for the circular order.

## Table 4. Predefined TLI domains

| Domain | Features | Tree | Low-rank | Optimized circle | Circle stability | Domain verdict |
|---|---:|---:|---:|---:|---:|---|
| Grammar linear order | 14 | **0.494** | 0.493 | 0.401 | **0.811** | non-periodic |
| Grammar other | 38 | **0.313** | 0.243 | 0.253 | 0.274 | non-periodic |
| Grammatical categories | 23 | 0.229 | 0.125 | **0.252** | 0.373 | ambiguous; below stability gate |
| Lexical | 18 | **0.269** | 0.220 | 0.142 | 0.057 | non-periodic |
| Phonology | 40 | **0.229** | 0.215 | 0.151 | 0.550 | non-periodic |

Local-periodic candidate gate: circle Spearman ≥ 0.15, within 0.03 of best non-periodic baseline, stability ≥ 0.40.

## Table 5. Geographic transfer contradiction

| Representation / test | Association transfer |
|---|---:|
| TLI macroarea geographic blocks | 0.088 |
| TLI matched-random blocks | 0.363 |
| TLI coordinate clusters | 0.106 |
| TLI matched-random coordinate blocks | 0.351 |
| GBI macroarea mean | 0.144 ± 0.043 |
| WALS macroarea mean | **0.634 ± 0.075** |

The WALS result prevents a universal claim that cross-linguistic association geometry necessarily collapses across regions.
