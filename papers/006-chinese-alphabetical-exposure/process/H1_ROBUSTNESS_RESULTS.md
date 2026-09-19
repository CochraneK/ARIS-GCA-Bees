# ARIS4C006 · H1 robustness results

Last updated: 2026-09-19

GitHub Actions run: `35425101408`  
Artifact: `aris4c006-h1-robustness`

All analyses re-verified the committed preregistration lock and matching confirmatory unlock before execution.

## Frozen robustness results

| Analysis | Rows | Works | Interaction / slope | SE | 95% CI | p |
|---|---:|---:|---:|---:|---:|---:|
| Primary reference | 75,205 | 15,410 | +0.64798 | 0.12289 | [0.40712, 0.88884] | 1.34e-7 |
| Focal teams 3+ authors | 71,455 | 13,535 | +0.55599 | 0.10736 | [0.34557, 0.76642] | 2.23e-7 |
| Convention exposure from 3+ author works | 74,924 | 15,315 | +0.76303 | 0.13591 | [0.49665, 1.02942] | 1.98e-8 |
| Both focal team 3+ and convention 3+ | 71,256 | 13,481 | +0.65391 | 0.11562 | [0.42729, 0.88052] | 1.55e-8 |
| Low-alphabetization negative-control slope | 35,451 | 6,666 | −0.00085 | 0.00689 | [−0.01435, 0.01265] | 0.902 |

## Interpretation

The primary interaction is not driven by two-author teams or by chance alphabetical appearance in two-author convention papers.

The low-alphabetization negative control uses the estimator's theoretical zero:
`ExcessAlpha <= 0`.

In those contexts, relative alphabetical surname position has essentially zero association with listed byline position.

This pattern is consistent with the proposed institutional mechanism:
- surname order matters where the field actually uses alphabetical bylines;
- surname order does not show a comparable gradient where the field is no more alphabetical than the chance benchmark.

These robustness analyses do not alter or replace the preregistered H1 primary result.
