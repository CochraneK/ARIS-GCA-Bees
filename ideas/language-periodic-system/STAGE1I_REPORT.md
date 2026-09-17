# Stage-1I · WALS External Sanity Replication

**Verdict:** `WALS_TREE_OVER_CIRCULAR`

Languages in pivot: 2659 · best-covered parameters used: 30

## Family-held-out

| Model | Spearman mean ± SD |
|---|---:|
| lowrank2 | 0.468 ± 0.034 |
| tree | 0.603 ± 0.026 |
| circular_optimized | 0.410 ± 0.050 |

Tree − circular: **0.193**; tree win fraction **1.00** across 8 valid splits.

## Macroarea association transfer

| Macroarea | Test n | Train↔test Spearman | Common pairs |
|---|---:|---:|---:|
| Africa | 604 | 0.686 | 406 |
| Australia | 183 | 0.563 | 249 |
| Eurasia | 658 | 0.613 | 434 |
| North America | 396 | 0.575 | 435 |
| Papunesia | 560 | 0.758 | 412 |
| South America | 258 | 0.606 | 380 |

Mean macroarea transfer: **0.634 ± 0.075**.

## Claim boundary

WALS is highly sparse and not dependency-curated like TLI/GBI. This stage tests qualitative direction only; estimates are not directly comparable in magnitude to earlier stages.
