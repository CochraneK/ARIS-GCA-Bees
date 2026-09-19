# ARIS4C006 · Main tables

Last updated: 2026-09-19

## Table 1. Frozen data sources and operational definitions

| Component | Frozen source / rule | Role |
|---|---|---|
| Chinese surname population | ChineseNames 2025.8 official source package | Population counts and surname inventory |
| Surname pronunciation/order | Pinned CCNC surname lexicon, commit `a14520b9cc8bd6b251aeb4a7453ab1a45f23aa15` | Surname-specific canonical Pinyin ordering |
| Scholarly works/authorships | OpenAlex | Work type, author order, primary-topic field, CN affiliation, canonical authors |
| Structured bibliographic family name | Crossref | Tier-1B family-name evidence after positional reconciliation |
| Primary work types | `article`, `conference-paper` | Main mechanism frame and convention estimator |
| Focal work window | 2011–2025 | All 26 OpenAlex primary-topic fields |
| Primary context | primary-topic field × prior 3 complete years | Institutional alphabetization exposure |
| Exposure | exact chance-corrected LOAO | `(N_ct-N_ict)/(D_ct-D_ict)`, require `D^-i>=50` |
| Focal predictor | `RelAlphaRank` | Within-team alphabetical family-name midrank |
| Primary outcome | `ListedPositionNorm` | 0 first to 1 last |
| Primary inference | work FE + 3-way clustered SE | author + work + primary-field×year |

## Table 2. Outcome-blind materialization quality

| Metric | Value |
|---|---:|
| Planned field-year cells | 390 |
| Cells meeting target | 383 |
| Cells retained below target | 6 |
| Cells excluded below minimum | 1 |
| Retained works before LOAO | 15,487 |
| Focal authorship rows before LOAO | 75,413 |
| Unique canonical authors before LOAO | 68,363 |
| Field-year clusters before LOAO | 389 |
| Exact-LOAO retained rows | 75,205 |
| LOAO exclusions, `D^-i<50` | 208 |
| Exact-LOAO retained works | 15,410 |
| Exact-LOAO canonical authors | 68,176 |
| Exact-LOAO field-year clusters | 386 |
| Primary Romanized surname route | 75,412 rows before LOAO |
| Direct-Han route | 1 row before LOAO |

## Table 3. Confirmatory estimands

| Hypothesis | Outcome | Interaction estimate | SE | 95% CI | Raw p | Holm p | Status |
|---|---|---:|---:|---:|---:|---:|---|
| H1 | Normalized listed position | **+0.647981** | 0.122891 | [0.407118, 0.888843] | 1.344e-7 | — | Primary confirmatory; opened |
| H2 | First-listed probability | **−0.628007** | 0.140854 | [−0.904075, −0.351938] | 8.251e-6 | **Pending H3** | Secondary confirmatory; opened |
| H3 | Observed five-year publication persistence | **Pending frozen structural gate and outcome opening** | — | — | — | **Pending H3** | Not yet opened |

H1 is not part of the secondary multiplicity family. H2 and H3 receive the frozen Holm adjustment jointly only if H3 passes its preregistered structural adequacy gate and is estimable.

## Table 4. Mandatory robustness and falsification

| Check | Estimate / diagnostic | 95% CI / reference | p / status |
|---|---:|---:|---:|
| Primary H1 | +0.647981 | [0.407118, 0.888843] | 1.344e-7 |
| Focal works with 3+ authors | +0.555993 | [0.345570, 0.766416] | 2.234e-7 |
| Exposure estimated from 3+ author convention works | +0.763033 | [0.496646, 1.029420] | 1.976e-8 |
| Both 3+ restrictions | +0.653907 | [0.427290, 0.880523] | 1.554e-8 |
| Low-alphabetization contexts (`ExcessAlpha<=0`) | −0.000851 surname-position slope | [−0.014347, 0.012646] | 0.902 |
| Future-exposure placebo | Pending official falsification artifact | — | Pending |
| Team-preserving surname-order permutation | Pending official falsification artifact | — | Pending |
| H3 low-identity-risk sensitivity | Pending H3 structural gate | — | Pending |
| H3 ORCID-anchored sensitivity | Pending H3 structural gate | — | Pending |

## Reporting note

Values above are copied only from committed GitHub Actions artifacts or frozen outcome-blind materialization manifests. Pending cells must not be filled from exploratory/local calculations when a canonical Actions result is specified by the analysis workflow.
