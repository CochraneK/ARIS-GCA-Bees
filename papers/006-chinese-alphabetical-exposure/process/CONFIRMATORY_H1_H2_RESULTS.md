# ARIS4C006 · Confirmatory H1/H2 results

Last updated: 2026-09-19

## Preregistration provenance

- Lock label: `ARIS4C006-prereg-v1`
- Lock SHA-256: `c416b84523d30346a46e5779fb55393af63bae0f578ca71a19c4671325e21ffd`
- Confirmatory unlock verified before outcome access.
- GitHub Actions run: `35424741506`
- Artifact: `aris4c006-confirmatory-h1h2`
- Frozen source aggregate run: `35424125236`
- Analysis script: `code/30_confirmatory_h1_h2.R`
- Exact LOAO frame builder: `code/29_build_confirmatory_loao_frame.py`

## Confirmatory frame

- focal rows input: **75,413**
- focal rows retained after exact LOAO `D^{-i} >= 50`: **75,205**
- exclusions for low LOAO information: **208**
- works: **15,410**
- canonical authors: **68,176**
- primary-field × year clusters: **386**

## H1 — normalized listed byline position

Frozen model:

`ListedPositionNorm_iw = WorkFE_w + beta1 RelAlphaRank_iw + beta2(RelAlphaRank_iw × LOAOExposure_ict) + error_iw`

Primary estimand `beta2`:

- estimate: **+0.6479808**
- SE: **0.1228913**
- 95% CI: **[0.4071182, 0.8888434]**
- two-sided p: **1.3436 × 10^-7**

Under the frozen coding, positive `beta2` means that as independently measured prior alphabetical-authorship exposure rises, an author's within-team alphabetical surname position becomes substantially more predictive of a later listed byline position.

This is the preregistered primary confirmatory result.

## H2 — first-listed authorship

Frozen linear-probability work-FE model using the same predictor, exposure, work frame and three-way clustering.

Interaction estimate:

- estimate: **−0.6280066**
- SE: **0.1408537**
- 95% CI: **[−0.9040748, −0.3519384]**
- raw two-sided p: **8.2507 × 10^-6**

Negative interaction is directionally consistent with the same mechanism: under stronger prior alphabetization regimes, alphabetically later within-team surnames are less likely to be listed first.

**Multiplicity note:** H2 is one member of the frozen two-test secondary family. Its final Holm-adjusted p-value must be computed jointly with H3 after the frozen H3 structural gate and confirmatory H3 execution. Until then, only the raw H2 p-value is reported.

## Interpretation boundary

These results support the preregistered institutional byline-order mechanism. They do not establish that surname letters affect ability, intelligence, personality, or scientific contribution quality, and they do not treat surname position as randomized in China.

No post-result design change was used to obtain these estimates.
