# ARIS4C006 · Frozen inference and multiplicity rule

Last updated: 2026-09-18

## Primary estimand

Primary model:

`ListedPositionNorm_iw = WorkFE_w + beta1 RelAlphaRank_iw + beta2(RelAlphaRank_iw × LOAOExposure_i,c,t) + error_iw`

Primary estimand:

`beta2`

The preregistered directional mechanism predicts `beta2 > 0`, but the formal primary hypothesis test is **two-sided**.

## Primary significance rule

- alpha = **0.05**
- report 95% confidence interval
- report point estimate in interpretable units, including predicted change from low to high measured exposure
- do not convert a non-significant primary result into a positive claim based on a favorable secondary specification

## Cluster-robust inference

Primary standard errors use multiway clustering across:

1. **canonical OpenAlex author ID** — repeated authors across works;
2. **OpenAlex work ID** — dependence among authorships on the same work;
3. **primary-topic field × focal publication year** — shared measured convention exposure and common field-year shocks.

The implementation must support multiway cluster-robust covariance. If the chosen software cannot reproduce the specified three-way clustering, the software is changed; the clustering rule is not weakened after outcome inspection.

## Fixed effects

Primary mechanism model:
- work fixed effects are mandatory.

Because exposure is common at the work/context level apart from LOAO author-specific subtraction, work FE absorb:
- journal/source;
- field;
- publication year/date;
- team size;
- work topic/quality factors shared by listed authors.

Do not add work-level controls redundantly to the work-FE primary model.

## Mandatory inference robustness

Report:

- 3+ total-author works;
- >=3 focal CN-affiliated ChineseNames-mappable authorships where sufficiently powered;
- 3+ author convention-estimation exposure;
- Tier-1 surname-evidence subset;
- low-identity-risk subset;
- alternative two-way cluster combinations as diagnostics, without replacing the frozen three-way primary SE.

A sensitivity may use field-year wild-cluster bootstrap if implementation is validated before focal analysis.

## Multiplicity

### Primary family

There is exactly **one primary estimand**: `beta2` in the normalized-position work-FE model.

No multiplicity correction is applied to this single primary test.

### Secondary confirmatory family

At most **two** secondary outcomes/estimands may remain confirmatory after the remaining outcome-blind gates are frozen.

Secondary confirmatory p-values are adjusted with **Holm's method** at familywise alpha 0.05.

Candidate secondary slots:
1. first-listed authorship probability using the same mechanism predictor/exposure;
2. one longitudinal distal endpoint only if the identity/cohort/exposure-variation gates remain passed.

Any additional citation, mobility, elite-list, source-level, nonlinear-rank, or subgroup result is exploratory unless separately preregistered before outcome inspection.

## Effect hierarchy

Interpretation order is fixed:

1. primary within-work author-position mechanism;
2. first-listed secondary;
3. one longitudinal distal outcome if retained;
4. structural Chinese population-rank model as supportive/secondary evidence;
5. exploratory bibliometric/career extensions.

A downstream association cannot rescue failure of the primary institutional-order mechanism.

## Placebo / randomization diagnostics

Mandatory non-primary diagnostics include:

- future exposure predicting prior listed position;
- surname/order-key permutation preserving team size;
- low-alphabetization field-years;
- single-author outcomes where relevant;
- exposure reconstructed from 3+ author convention works.

These are falsification/robustness tests, not alternative primary tests.

## Reporting

Always report:
- coefficient;
- standard error;
- 95% CI;
- exact p-value where practical;
- number of works;
- number of focal authorships;
- number of canonical authors;
- number of field-year exposure clusters;
- work/team-size distribution.

Do not report only significance stars.


## H3 longitudinal inference

For the frozen secondary longitudinal endpoint:

`logit(Persistence5_i) = alpha + beta1 InitialRankNorm_i + beta2 MeanEarlyExposure_i + beta3(InitialRankNorm_i × MeanEarlyExposure_i) + EntryYearFE + EntryPrimaryFieldFE + log1p(EntryWorkCount_i)`

Frozen rules:
- `EntryWorkCount_i` enters as `log1p(EntryWorkCount_i)`;
- primary H3 estimand is the interaction `beta3`;
- two-sided test;
- covariance is clustered by the composite `EntryPrimaryField × EntryYear`;
- one row per canonical entrant;
- H3 raw p-value is Holm-adjusted jointly with H2 as the two-member secondary confirmatory family.

If the outcome-blind longitudinal structural-adequacy gate in
`LONGITUDINAL_SAMPLING_RULE.md` fails, H3 is removed from the confirmatory
family before Persistence5 is opened. H1/H2 inference is unchanged.
