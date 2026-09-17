# Stage-1D · Held-out Circular-Robinson Sensitivity

**Verdict:** `CIRCULAR_ROBINSON_NOT_SUPPORTED`

This test is inspired by the circular-Robinson characterization in Armstrong, Guzmán & Sing-Long (2021): under a compatible cyclic order, each dissimilarity row read around the cycle is unimodal. Because every linear Robinson matrix is also circular Robinson, the report additionally checks whether the wrap-around closure edge is actually supported and compares against a hierarchical-tree order.

Lower unimodality violation is better. A closure ratio near 1 means the wrap-around pair is about as similar as a typical internal adjacent pair.

## 40 features

Valid family-held-out runs: 6/6 attempts

| Diagnostic | Circular order | Tree order | Random order |
|---|---:|---:|---:|
| Mean row-unimodality violation ↓ | 0.222 ± 0.012 | 0.209 ± 0.011 | 0.237 ± 0.009 |
| Closure / internal-adjacent ratio | 0.608 ± 0.764 | 0.133 ± 0.148 | — |

## 60 features

Valid family-held-out runs: 6/6 attempts

| Diagnostic | Circular order | Tree order | Random order |
|---|---:|---:|---:|
| Mean row-unimodality violation ↓ | 0.297 ± 0.009 | 0.284 ± 0.010 | 0.307 ± 0.009 |
| Closure / internal-adjacent ratio | 0.037 ± 0.091 | 1.828 ± 2.646 | — |

## Automated interpretation

- 40 features: circular violation=0.222, tree=0.209, random=0.237; circular closure ratio=0.608.
- 60 features: circular violation=0.297, tree=0.284, random=0.307; circular closure ratio=0.037.

## Claim boundary

This is a noisy-data sensitivity based on the row-unimodality characterization, not an exact strict-circular-Robinson recognition proof. Passing it cannot by itself establish a periodic language system because linear Robinson structure is a subset of circular Robinson structure. Failing it would be stronger evidence against the specific circular-order interpretation used here.
