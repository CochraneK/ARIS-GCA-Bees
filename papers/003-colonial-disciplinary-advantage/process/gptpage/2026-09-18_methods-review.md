# GPTPage quantitative methods review — 2026-09-18

Stage: statistical design reviewer

Execution mode: ChatGPT web/GPTPage handoff plus outcome-blind synthetic sanity checks.

## Main recommendation

Use **PPML/high-dimensional fixed-effect models on non-negative fractional bibliometric counts as the confirmatory inferential engine**, and treat RCA/SRCA as descriptive/robustness representations of specialization rather than the sole regression outcome.

Why:
- raw RCA is highly skewed and unstable in small cells;
- log RCA requires arbitrary handling of zeros;
- deleting low-count field-country cells conditions the sample on the outcome and can induce selection;
- Poisson pseudo-maximum-likelihood does not require the dependent variable to follow a Poisson distribution or be integer-valued when used as QMLE; robust inference is required;
- PPML naturally retains zero outcomes and models multiplicative relative structure.

This choice is based on estimator properties and simulation before exposure-outcome inspection, not on which method produces a preferred real result.

---

## 1. Primary output-specialization model

Let `P_cdt` be fractional publication output for country c, discipline d, period t.

Candidate confirmatory model:

`E[P_cdt | .] = exp(beta * Exposure_c × IKES_d + FE_country×period + FE_discipline×period)`

Estimate by PPML.

Interpretation:
- country×period fixed effects absorb each country's total publication scale and all other country-period-wide factors;
- discipline×period fixed effects absorb global field size/trends;
- beta captures whether historical exposure predicts a systematically different within-country disciplinary composition along IKES.

This is the multiplicative analogue of a relative-specialization comparison and removes the need to divide noisy small counts by multiple denominators before estimation.

### Descriptive visualization

Compute:

`RCA_cdt = (P_cdt / P_ct) / (P_dt / P_t)`

and preferably bounded symmetric RCA:

`SRCA = (RCA - 1) / (RCA + 1)`

Use SRCA maps/profile plots for interpretability. Do not make SRCA threshold choices the primary inferential engine.

---

## 2. Primary impact model

A useful impact estimand is whether a country-field produces unusually many elite papers conditional on its publication volume.

Let:
- `Top10_cdt` = fractional count of papers in a field/year normalized top 10% citation class;
- `P_cdt` = fractional publication count.

Candidate PPML rate model:

`E[Top10_cdt] = exp(beta * Exposure_c × IKES_d + FE_country×period + FE_discipline×period + offset(log(P_cdt)))`

Use only cells with positive denominator for this rate model. Zero Top10 counts are retained.

Alternative robustness:
- cell-level quasi-binomial/fractional response;
- normalized citation score/MNCS where coverage is reliable.

Top 1% is secondary because its cell-level sparsity is much higher.

---

## 3. Dyadic network model

Rather than normalize coauthorship counts ad hoc, use a structural-gravity-style PPML model.

Let `C_ijdt` be fractional coauthored output between countries i and j in discipline d, period t.

Strong candidate specification:

`E[C_ijdt] = exp(beta * FormerColonialTie_ij × IKES_d + FE_pair + FE_i×d×t + FE_j×d×t)`

Advantages:
- pair FE absorb all time-invariant pair-level baseline affinity such as distance and generic historical closeness;
- origin-field-time and destination-field-time FE absorb each country's size/propensity to publish and collaborate in that discipline and period;
- the interaction asks whether former colonial pairs are *disproportionately* connected in more historically entangled disciplines.

Nested mechanism model:

add `CommonLanguage_ij × IKES_d`.

Because language may be a colonial persistence channel, present models with and without this interaction and interpret attenuation as mechanism decomposition rather than choosing the model with the preferred coefficient.

### Warning

High-dimensional PPML can encounter separation/perfect-prediction issues in sparse dyadic cells. Use an estimator that diagnoses and drops separated fixed-effect groups according to documented rules, and record the dropped observations.

---

## 4. Imperial-center small-N analysis

Do not use the same asymptotic PPML coefficient as headline evidence for the handful of major colonial powers.

Recommended:
- plot each empire's disciplinary profile against IKES;
- estimate within-country profile slopes for descriptive effect size;
- compare slope ordering with empire intensity;
- leave one imperial center out in every iteration;
- use permutation of discipline labels/IKES only as a falsification/exact-style check, with exchangeability caveats.

The independent historical unit is the imperial center, not each field cell.

---

## 5. Inference for the former-colony country×discipline model

The interaction is built from a country-level exposure and a discipline-level moderator, creating cross-classified dependence.

Preferred reporting:
- multiway cluster-robust uncertainty by country and discipline where software supports it;
- because the number of confirmatory disciplines is only 21, supplement asymptotic field-cluster inference with a discipline-level wild/bootstrap or randomization-style sensitivity if defensible;
- report confidence intervals/effect sizes rather than treating p<.05 as the sole decision rule.

Do not cluster by country only and ignore field-level common shocks.

---

## 6. Synthetic sanity check performed before real outcomes

A synthetic country×field×period dataset was generated with:
- 50 countries;
- 21 disciplines;
- 3 periods;
- heterogeneous country scale and field shares;
- a planted exposure×IKES log-relative-specialization coefficient of `0.22`.

A PPML model with country-period and discipline-period fixed effects recovered approximately `0.230` in this single outcome-blind sanity run.

This is **not** a power analysis or proof of unbiasedness. Its purpose was only to verify that the proposed model parameter corresponds to the planted multiplicative disciplinary-composition effect and that the coding logic is sound.

A separate larger synthetic RCA check showed that filtering cells by observed field count can remove a large fraction of cells and changes the estimand/sample composition; this supports avoiding an outcome-based minimum field-count rule for the primary output model.

---

## 7. What still needs simulation before preregistration lock

1. realistic zero/sparsity rates under OpenAlex-like country/field sizes;
2. finite-sample behavior of two-way clustered uncertainty with 21 disciplines;
3. dyadic PPML computational feasibility and separation rate;
4. sensitivity to fractional attribution;
5. country inclusion based on **overall coverage**, not field-specific realized outcomes;
6. behavior under mismeasured IKES and exposure variables.

These simulations can be completed without opening real colonial-effect outcomes.

---

## 8. Ranking/prestige models

Do not regress numeric rank by OLS.

Preferred depending available data:
- component/overall continuous score when methodology supports cardinal interpretation;
- top-N presence / ordered bins;
- rank-censored/ordinal model;
- bibliometric-predicted prestige residual as a secondary descriptive outcome.

Never combine QS, THE, Shanghai, and Leiden into one averaged master score. Disagreement among them is part of the substantive result.

---

## 9. Primary statistical freeze recommendation

### Confirmatory A — output
PPML fractional publication count:

`Exposure × IKES + country×period FE + discipline×period FE`

### Confirmatory B — impact
PPML fractional Top10 count with `log(publication volume)` offset and the same FE structure.

### Confirmatory C — network
PPML fractional dyadic coauthorship:

`FormerColonialTie × IKES + pair FE + origin×discipline×period FE + destination×discipline×period FE`

### Descriptive/robustness
- SRCA profiles;
- full counting;
- alternate field mapping;
- alternate exposure source;
- MNCS/FWCI;
- rankings/prestige.

**Methods gate: GO**, conditional on a final simulation/inference note and software-feasibility test before real outcomes.
