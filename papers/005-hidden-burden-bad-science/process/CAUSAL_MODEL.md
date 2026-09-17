# CAUSAL + MEASUREMENT MODEL — ARIS4C005

## 1. Why a measurement model is mandatory

Retraction records are produced by a **detection and correction system**, not by a census of underlying misconduct. The probability that a problematic article is retracted depends on both the underlying problem and the chance that somebody detects, investigates, substantiates, and formally corrects it.

Therefore:

`observed retraction rate != true severe-integrity prevalence`.

The project models the latent scientific state separately from the observation/correction process.

---

# 2. Core variables

For article `i`:

- `Z_i`: latent article integrity state;
- `Q_i`: underlying scientific quality/validity independent of intent;
- `M_i`: misconduct / severe-integrity mechanism if present;
- `D_ij`: detector `j` signal;
- `A_i`: audit/manual-adjudication result;
- `S_i`: scrutiny intensity;
- `G_i`: governance/correction capacity of journal/publisher/institution;
- `R_i`: observed retraction/editorial action;
- `L_i`: correction latency;
- `X_i`: pre-publication article/field/journal covariates;
- `C_i(t)`: downstream material-dependence events over time;
- `F_i(t)`: funding/attention trajectory;
- `Y_i(t)`: downstream knowledge/innovation outcomes.

---

# 3. Detection process

Conceptual DAG:

```text
X ------> Z ------> scientific unreliability ------> downstream dependence C ------> Y
|         |                    |
|         v                    v
|       detector signals D    post-publication scrutiny
|         |                    |
v         v                    v
S ------> detection ----------> investigation ------> formal correction R
           ^                       ^                    |
           |                       |                    v
           +-------- G ------------+              correction visibility
                                                       |
                                                       v
                                             future dependence / decay
```

Additional pathways:

```text
prominence / citations -> scrutiny
prominence / citations -> downstream propagation
journal/publisher      -> scrutiny + governance
field norms            -> detector availability + retraction probability
open/full-text access  -> machine-detection probability
country/institution    -> reporting/investigation systems + publication mix
```

This creates severe selection problems if raw retraction rates are interpreted as misconduct prevalence.

---

# 4. Main biases and controls

## 4.1 Detection bias

High-profile papers may attract more scrutiny and therefore more corrections even if their underlying problem rate is identical.

Mitigation:

- model scrutiny proxies separately;
- stratify/adjust for citation prominence and journal visibility;
- use article-level independent detector sampling not conditioned on retraction;
- random audit from the target publication universe.

## 4.2 Governance/correction bias

Publishers, journals, institutions, and national systems differ in willingness/capacity to investigate and retract.

Mitigation:

- never rank countries by raw retraction rate as if it were fraud prevalence;
- include correction-system covariates and publisher/journal random effects;
- emphasize globally pooled / field-time estimates first;
- country-level outputs, if any, are sensitivity analyses with strong detection-bias caveats.

## 4.3 Open-access / machine-readable selection

Image/text/statistical detectors work better when full text and figures are accessible.

Mitigation:

- model detector missingness;
- stratified audit includes accessible and inaccessible records where legally possible;
- report coverage denominators for every detector;
- sensitivity analysis under missing-not-at-random assumptions.

## 4.4 Detector dependence

Paper mills may trigger text, image, authorship, and peer-review signals simultaneously. Capture-recapture estimators assuming independent lists can be badly biased.

Mitigation:

- Bayesian latent-class model is primary;
- capture-recapture uses interaction terms and is sensitivity only;
- estimate conditional detector correlations in gold-standard subset.

## 4.5 Verification / incorporation bias

If the same detector both selects papers for manual review and becomes the gold-standard criterion, sensitivity/specificity is inflated.

Mitigation:

- random negative sample plus detector-positive oversamples;
- blinded adjudication to detector labels where feasible;
- independent adjudication rubric;
- inverse-probability weighting back to target universe.

## 4.6 Researcher-to-paper ecological conversion

Researcher self-report studies measure people/behaviors over career/time windows, not papers.

Mitigation:

- use as contextual prevalence of behavior only;
- never multiply researcher prevalence by global publication count;
- if used as prior information, explicitly model researcher productivity and per-paper event processes rather than direct conversion.

## 4.7 Retraction reason misclassification

Retractions include honest error, plagiarism, peer-review manipulation, duplicate publication, data fabrication, and publisher/journal problems.

Mitigation:

- reason codebook with multi-label coding;
- separate author-caused scientific unreliability from procedural/publisher corrections;
- adjudicate ambiguous notices;
- report E1 definitions under narrow and broad sensitivity sets.

## 4.8 Time censoring

Recent papers have had less time to be detected/retracted/cited.

Mitigation:

- survival models for correction latency;
- cohort comparisons with equal follow-up windows;
- do not interpret 2026 correction rates as complete;
- primary universe ends at 2025 and lag-sensitive analyses may end earlier.

---

# 5. Latent prevalence model

Primary binary latent state:

```text
Z_i = 1 severe integrity failure materially compromising a claim
      0 otherwise / not established
```

For detector `j`:

`P(D_ij=1 | Z_i=1) = sensitivity_j`

`P(D_ij=0 | Z_i=0) = specificity_j`

Allow detector parameters to vary hierarchically by broad field and access modality when data support it.

Prevalence model:

`logit(pi_i) = alpha + field + publication_period + article_type + journal/publisher effects + selected pre-specified covariates`

Do not use post-treatment variables such as later citation count to estimate the underlying prevalence unless explicitly modeling the detection pathway.

Manual audit likelihood anchors the model.

---

# 6. Gold-standard audit design

Two-stage stratified sampling:

1. **population-random stratum** — required for prevalence calibration;
2. **signal-enriched strata** — oversample detector positives to estimate detector behavior and characterize rare modes.

Weights restore population estimates.

Adjudication should use at least two independent reviewers for the high-stakes severe-integrity label, with disagreement adjudication and a category for **indeterminate** rather than forced classification.

The project does not publish misconduct accusations against individuals based solely on model output.

---

# 7. Propagation model

A citation is an observable link; contamination requires semantic dependence.

For citation edge `a -> b`, classify `K_ab`:

- `0` background / incidental mention;
- `1` critique / warning / retraction discussion;
- `2` method reuse without reliance on target substantive result;
- `3` substantive result/data dependence;
- `4` evidence-synthesis inclusion / pooled use.

Primary contaminated edge: `K >= 3`.

Edge classifier validation uses human-coded samples and reports precision/recall by field.

Correction is an intervention on **visibility/trust**, not literal deletion of past knowledge. Post-correction propagation can persist through intermediary papers that do not themselves carry a visible retraction marker.

---

# 8. Knowledge Ghost Half-Life causal interpretation

Retraction/correction timing is not random. Papers may be retracted precisely when scrutiny/citations surge.

Therefore a naive pre/post decline can confound natural citation aging and detection-triggered attention.

Preferred design:

- matched unretracted/problematic-reference controls with similar pre-event citation trajectory;
- event-time fixed effects;
- paper age and field-time normalization;
- separate critique citations from result-dependent citations;
- placebo event dates;
- sensitivity to retraction reason and visibility.

KGH is descriptive unless these assumptions are credible.

---

# 9. Innovation-delay causal model

Conceptual pathway:

```text
severe unreliable result
    -> attention/funding/citation advantage
    -> follow-up concentration
    -> reduced entry/attention to alternatives
    -> delayed validation/adoption of legitimate alternative
```

Potential confounders:

- underlying topic popularity;
- technological readiness;
- disease burden / market size;
- contemporaneous policy/funding shocks;
- journal attention;
- charismatic/high-status teams;
- genuine early evidence strength.

Preferred identification:

- define integrity shock ex ante by formal correction date;
- build matched topic/control clusters using pre-event trajectories only;
- event-study with pre-trend checks;
- synthetic control for major cases;
- negative-control outcomes/topics;
- report delay estimands before permanent-loss claims.

---

# 10. Sleeping Beauty causal boundary

Observed delayed-recognition models can be trained empirically. The transition from “this paper resembled known future Sleeping Beauties” to “bad science prevented its awakening” is counterfactual and cannot be directly observed.

Therefore:

- first estimate **awakening delay** among papers that eventually awaken;
- only then estimate expected never-awakened counts under a structural/counterfactual model;
- do not name individual uncited papers as lost masterpieces;
- conduct strong placebo and alternative-attention-shock tests.

---

# 11. Financial-cost boundary

A grant linked to a retracted paper may fund many valid outputs. Therefore:

`associated grant dollars != wasted dollars`.

Primary financial estimand is attributable output/project cost under declared allocation rules. Whole-grant amounts can be shown as the funding environment exposed to correction risk, never as direct loss without allocation evidence.

Likewise:

`global R&D spending × misconduct prevalence` is prohibited as a primary estimate.

---

# 12. Causal claim ladder

Every result receives one label:

- **DESCRIPTIVE:** count/rate/association only;
- **MEASUREMENT-MODEL:** latent quantity under calibrated assumptions;
- **QUASI-CAUSAL:** counterfactual design with explicit identifying assumptions;
- **SCENARIO:** transparent what-if calculation, not empirical estimate;
- **EXPLORATORY STRUCTURAL COUNTERFACTUAL:** model-dependent lost-discovery estimate.

No prose may use stronger causal language than the assigned label permits.
