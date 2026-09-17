# MANUSCRIPT OUTLINE — ARIS4C005

## Working title

**The Hidden Burden of Bad Science: Measuring Research Integrity Failures and Their Downstream Scientific Opportunity Cost**

Alternative technical title:

**From Retraction to Contamination: A Measurement Framework for the Hidden Burden of Research Integrity Failures**

---

# Abstract architecture

## Background

The scientific literature contains retractions, major errors, misconduct, and broader research waste, but these categories are frequently conflated. Retraction counts provide a detected lower bound rather than a prevalence estimate, and downstream burdens on later science are poorly represented by source-paper counts alone.

## Methods

Construct a versioned global journal-article/review universe; map formal correction events; separate severe scientific unreliability, confirmed misconduct, publication-process failure, and broader research waste; calibrate article-level integrity signals against stratified manual adjudication; estimate latent severe-failure prevalence with a hierarchical measurement model; classify material downstream dependence; quantify correction dynamics and selected human/financial burdens.

## Results

**Do not draft numeric results until Pilot A–C outputs exist.**

Reserved slots:

- global target-universe size;
- detected E1-S/E1-M/E1-P lower bound;
- correction latency;
- calibrated latent prevalence / failure-to-identify result;
- direct Scientific Contamination Footprint;
- post-correction persistence / KGH;
- one validated cost/human-time module.

## Conclusions

Expected framing regardless of direction:

> The burden of research-integrity failures cannot be inferred from retraction rates alone. Measuring it requires separating the latent scientific state from detection/correction systems and tracing whether unreliable claims are materially reused downstream.

No claim that “X% of science is fake” without the calibrated article-level model.

---

# 1. Introduction

## 1.1 The visible tip

Open with the scale of scholarly publishing and formal retractions, but immediately state that:

`retraction != prevalence`.

Crossref/OpenAlex counts illustrate that even the denominator “how many papers exist?” is definition-dependent.

## 1.2 The denominator problem

Explain why:

- database coverage differs;
- works include different object types;
- researcher survey prevalence cannot be converted directly to paper prevalence;
- retraction rates mix underlying failure with detection and governance.

## 1.3 The propagation problem

Scientific harm is cumulative:

```text
source study
 -> follow-up work
 -> systematic review / meta-analysis
 -> guideline / policy / translation
```

Use VITALITY as empirical motivation that retracted trials can alter pooled results and enter clinical guidelines.

## 1.4 The opportunity-cost problem

Introduce the less visible costs:

- researcher time;
- participant contribution;
- reviewer/editor/investigation labor;
- innocent collaborator effects;
- delayed alternative research.

Avoid framing all these as fraud-specific; maintain E1/E2/E3 layers.

## 1.5 Contribution

The paper contributes:

1. a denominator-aware detected lower bound;
2. a calibrated article-level measurement model;
3. a semantic material-dependence propagation framework;
4. burden accounting in natural units rather than a composite score.

Innovation Delay and Sleeping Beauty analyses may be moved to companion work depending on pilot strength.

---

# 2. Methods

## 2.1 Study design

Global meta-research study with:

- bibliometric cohort construction;
- formal correction-event linkage;
- stratified article audit;
- latent-class measurement model;
- citation-context classification;
- quasi-experimental extensions.

## 2.2 Publication universe

Primary:

- OpenAlex core;
- journal article + review;
- publication years 2000–2025;
- Crossref DOI reconciliation.

Sensitivity:

- article only;
- conference inclusion;
- Crossref journal DOI denominator.

## 2.3 Integrity exposure ontology

Report E1-S, E1-M, E1-P, E2, E3 separately.

Primary epistemic-harm exposure: E1-S.

## 2.4 Correction data

Retraction Watch via Crossref/GitLab; deduplicate notices/events; preserve raw multi-label reasons; map narrow/broad definitions; audit ambiguous cases.

## 2.5 Detector / audit sample

Two-phase stratified design:

- population-random stratum;
- detector-enriched strata.

Adjudication label includes indeterminate state and does not infer person-level guilt from article features.

## 2.6 Latent prevalence

Primary binary severe-failure latent state; hierarchical detector sensitivity/specificity; broad field/time partial pooling; explicit detector missingness.

Design-based random-audit prevalence is reported alongside model output.

## 2.7 Downstream dependence

Citation edges classified as:

- background;
- critique;
- method reuse;
- result/data dependence;
- evidence-synthesis inclusion.

Contamination = result/data dependence or evidence-synthesis inclusion.

## 2.8 Correction dynamics

Matched event-study of new material dependence around correction events; control natural citation aging and scrutiny dynamics; estimate KGH only when decay is identifiable.

## 2.9 Burden modules

### Financial

Attributable output/project cost, not whole linked grants.

### Human time

RLY components with empirically calibrated effort distributions or transparent scenario status.

### Integrity Maintenance Debt

Incremental review/editor/investigation/reanalysis labor attributable to problematic outputs.

### Participants

Clinical subset; E1/E2 invalidation and E3 nonpublication reported separately.

### Career spillover

Uninvolved collaborator effects analyzed neutrally as collateral career effects.

## 2.10 Innovation-delay extension

Topic-level matched event study / synthetic control with pre-trend and placebo tests.

## 2.11 Sleeping Beauty extension

Observed awakening model → awakening delay → exploratory expected permanent non-awakening.

## 2.12 Missing data / bias

Detection bias, governance differences, open-access selection, right censoring, detector applicability, author/entity resolution.

## 2.13 Reproducibility and ethics

Public identifiers + derived aggregate data; no public accusation list of unretracted model-flagged researchers; restricted full text not redistributed.

---

# 3. Results architecture

## Result 1 — How large is the target literature?

Figure 1A: annual global article/review count by frozen universe.

Table 1: denominator definitions and differences.

## Result 2 — What is actually detected?

Figure 1B: detected E1-S/E1-M/E1-P by publication cohort and correction cohort.

Figure 2: correction-latency survival curve.

Emphasize detected lower bound.

## Result 3 — How much may remain hidden?

Figure 3A: detector coverage matrix.

Figure 3B: calibration/confusion matrices.

Figure 3C: design-based audit estimate vs latent posterior.

If identification fails, Result 3 becomes a negative methodological result explaining why the available detectors cannot support global prevalence.

## Result 4 — How far does problematic evidence propagate?

Figure 4: material-dependence cascade / Sankey from E1-S sources to downstream evidence objects.

Report ordinary citations separately from material dependence.

## Result 5 — Does formal correction stop propagation?

Figure 5: event-time rate of new material dependence and KGH if identifiable.

## Result 6 — What does this consume?

Figure 6: burden vector in natural units:

- attributable USD;
- RLY / scenario range;
- correction labor hours;
- participant burden in clinical subset;
- collateral career effect.

No summed score.

## Optional Result 7 — Innovation delay

Only if causal diagnostics pass.

## Optional Result 8 — Sleeping Beauty extension

Exploratory and clearly visually separated from observed/calibrated results.

---

# 4. Discussion

## 4.1 Main interpretation

The visible correction system undercounts the latent scientific-state problem but also reflects governance quality. Retraction is neither a synonym for fraud nor a sufficient prevalence estimator.

## 4.2 Why downstream dependence matters

The same number of problematic source papers can produce radically different burden depending on where they sit in the knowledge graph and whether they enter evidence synthesis/guidelines.

## 4.3 Human opportunity cost

Translate validated RLY into intuitive equivalents only after reporting the original unit and uncertainty.

Example rhetorical structure:

> This corresponds to X researcher-years under the calibrated model — equivalent in duration to Y five-year PhD blocks — not Y individual PhD students whose careers were literally lost.

## 4.4 The unknowable frontier

Discuss delayed recognition and permanent lost discovery as structurally harder than detected waste. This is where Never-Woken Sleeping Beauties belongs.

## 4.5 Limitations

Must foreground:

- detection/governance selection;
- audit uncertainty;
- detector field heterogeneity;
- inaccessible full text;
- causal limits of innovation analysis;
- English/biomedical bias in guideline evidence;
- inability to observe truly never-produced discoveries.

## 4.6 Implications

Focus on measurement and system design rather than naming “bad countries” or individual culprits:

- faster correction propagation;
- machine-readable notices;
- update-aware evidence synthesis;
- independent integrity auditing;
- incentives for correction;
- preserving participant/reviewer/researcher contributions through better transparency.

---

# Planned figures

1. **The denominator iceberg** — global works → target articles/reviews → detected correction events → estimated latent severe failures.
2. **Detection-system DAG** — underlying state vs scrutiny/governance/correction.
3. **Calibration panel** — detector coverage and manual-audit performance.
4. **Scientific Contamination Footprint** — dependency cascade.
5. **Knowledge Ghost Half-Life** — reliance after correction.
6. **Burden vector** — money/time/participants/correction labor without summing units.
7. **Innovation Delay event study** — optional.
8. **Sleeping Beauty counterfactual** — exploratory/companion-paper candidate.

---

# Planned supplementary material

- full reason mapping/codebook;
- manual adjudication form;
- source/version ledger;
- denominator sensitivity;
- capture-recapture sensitivity;
- prior/posterior diagnostics;
- detector missingness analysis;
- citation-classifier benchmark;
- event-study placebo/pre-trend panels;
- alternative Sleeping Beauty definitions.

---

# Manuscript split decision

Default:

### Paper 005A — Hidden burden + propagation

Denominator, detected lower bound, calibrated latent measurement, SCF/KGH, one burden module.

### Paper 005B — Scientific opportunity cost

Innovation Delay, crowding-out, Scientific Detour Years, career/talent allocation.

### Paper 005C — Never-Woken Sleeping Beauties

Delayed-recognition counterfactual, only if the causal chain survives validation.

The ARIS4C ID remains 005 as the umbrella project even if outputs split into multiple manuscripts.
