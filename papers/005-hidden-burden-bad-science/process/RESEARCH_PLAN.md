# RESEARCH PLAN — ARIS4C005

## Working title

**The Hidden Burden of Bad Science: Estimating the Global Scale and Downstream Cost of Research Integrity Failures**

## Stage

**Idea saturated → scope frozen → feasibility/pilot construction.**

No global latent-prevalence, lost-discovery, or Researcher-Life-Years figure is yet treated as an empirical result.

---

# 1. Core question

How much of the global scholarly literature is affected by severe research-integrity failures, how much remains undetected, and how far do those failures propagate into human time, research funding, careers, evidence synthesis, innovation, and downstream societal decisions?

A second, explicitly exploratory question asks whether integrity-related attention/resource distortions delay or prevent recognition of otherwise valuable work, including Sleeping Beauty trajectories.

---

# 2. Scope freeze

The project separates:

- `E1` confirmed severe integrity failure;
- `E2` probable severe integrity failure based on calibrated article-level evidence;
- `E3` broader research waste / evidence distortion without a misconduct claim.

The project does **not**:

- equate retraction with fraud;
- equate irreproducibility with fraud;
- multiply researcher self-report rates by paper counts;
- interpret raw country/journal retraction rates as misconduct prevalence;
- convert all harms into one arbitrary composite score;
- call whole linked grants “waste” without attributable-cost rules;
- identify named low-citation papers as “lost masterpieces” from a model alone.

Primary calendar universe: **2000–2025**.

---

# 3. Paper architecture

The first paper is designed as a modular empirical + measurement paper rather than an everything-at-once grand total.

## Core Module A — Global denominator + detected lower bound

Deliverables:

- versioned global article/review universe;
- detected E1 count/rate;
- reason taxonomy;
- correction-latency distribution;
- field/time variation with detection-bias caveats.

This module is descriptive and should be independently publishable.

## Core Module B — Hidden severe-integrity prevalence

Deliverables:

- stratified article sample;
- multi-detector feature matrix;
- manual adjudication gold set;
- detector sensitivity/specificity estimates;
- hierarchical Bayesian latent-prevalence estimate;
- capture-recapture sensitivity analysis.

This is the methodological core of the global hidden-burden claim.

## Core Module C — Knowledge propagation / evidence contamination

Deliverables:

- citation-context dependence classifier;
- direct Scientific Contamination Footprint;
- evidence-synthesis contamination;
- post-correction propagation decay;
- Knowledge Ghost Half-Life;
- optional Epistemic Reproduction Number.

## Core Module D — Human / financial opportunity cost

Deliverables where calibratable:

- attributable grant cost pilot;
- Researcher-Life-Years framework and calibrated scenarios;
- Integrity Maintenance Debt;
- participant-sacrifice clinical subset;
- collateral career effects.

## Core Module E — Innovation delay

Deliverables:

- integrity-shock topic-cluster design;
- matched controls/synthetic controls;
- Innovation Delay Years or a conclusion that the available data cannot support the metric.

## Extension Module F — Sleeping Beauties

Order of inference:

1. reproduce Sleeping Beauty / Prince detection;
2. model awakening among observed delayed-recognition papers;
3. test awakening delay around integrity/attention shocks;
4. only then estimate Never-Woken Sleeping Beauties as an exploratory structural counterfactual.

---

# 4. Phase 0 — idea saturation [COMPLETE]

The idea-mining stage was stopped after successive searches ceased generating new first-order loss categories.

Frozen loss ontology:

1. production resources;
2. labor/career capital;
3. epistemic/knowledge system;
4. innovation/opportunity;
5. societal/translation.

New concepts retained:

- Researcher-Life-Years;
- Participant Sacrifice Without Knowledge Gain;
- Integrity Maintenance Debt;
- Scientific Contamination Footprint;
- Epistemic Reproduction Number;
- Knowledge Ghost Half-Life;
- Innovation Delay Years;
- Scientific Detour Years;
- Never-Woken Sleeping Beauties;
- Talent Misallocation;
- Trust Tax.

No further free-form expansion unless a new first-order outcome emerges from evidence.

---

# 5. Phase 1 — denominator + Retraction Watch baseline

## 5.1 Freeze data releases

Record:

- OpenAlex snapshot/API retrieval date;
- corpus (`core` primary);
- Crossref retrieval date;
- Retraction Watch CSV commit/date;
- code commit.

## 5.2 Build `works_universe`

Minimum fields:

- OpenAlex work ID;
- DOI;
- title hash / normalized title;
- publication year/date;
- work type;
- journal/source;
- topic/field hierarchy;
- authorship IDs;
- institution IDs;
- citation count / references;
- open-access/access metadata;
- PMID where available.

## 5.3 Join correction events

Deduplicate Retraction Watch and publisher updates.

Construct:

- `retraction_reason_raw`;
- `reason_code` multi-label;
- `E1_narrow`;
- `E1_broad`;
- `E3_error`;
- `correction_date`;
- `latency_years`.

## 5.4 Baseline outputs

- annual publication counts;
- annual correction counts by publication cohort and correction cohort;
- detected rate;
- Kaplan-Meier / cumulative correction hazards by publication age;
- sensitivity excluding bulk publisher integrity sweeps.

### Gate 1

Proceed to prevalence modeling only if DOI/title matching and reason coding achieve acceptable coverage/accuracy in an audited subset.

---

# 6. Phase 2 — detector + manual-audit pilot

## 6.1 Sampling

Pilot target:

- `5,000–10,000` works automatically characterized;
- `750–1,500` manually adjudicated;
- random-population stratum + detector-positive enriched strata.

The exact confirmatory sample size is selected after pilot prevalence and detector performance are known.

For intuition only, a simple random-sample prevalence of 1% with ±0.2 percentage-point 95% margin needs about `9,508` observations under a naive binomial calculation; 0.5% with ±0.1 percentage point needs about `19,112`. Stratification, verification error, clustering, and rare-mode calibration make the real design more complex.

## 6.2 Strata

At minimum:

- broad field;
- publication period;
- article type;
- full-text/image accessibility;
- journal/source tier or publisher family;
- detector-signal pattern.

Country is not a primary stratification for fraud ranking because detection/correction systems differ substantially.

## 6.3 Audit rubric

Adjudication outcomes:

- severe integrity failure supported;
- serious scientific problem but intent/integrity status unresolved;
- honest major error;
- minor/immaterial anomaly;
- no identified material problem;
- indeterminate / insufficient evidence.

At least the severe/indeterminate cases receive two independent reviewers where feasible.

### Gate 2

Latent prevalence becomes a primary result only if the gold set can estimate detector performance with useful precision and inter-rater/adjudication reliability is acceptable.

---

# 7. Phase 3 — latent prevalence model

## Primary model

Hierarchical Bayesian binary latent class:

`Z_i in {severe integrity failure, otherwise}`.

Estimate:

- overall posterior prevalence;
- broad-field posterior prevalence;
- period trend;
- posterior hidden-case count;
- detector characteristics.

## Sensitivity

- alternative E1 label definitions;
- alternative priors;
- field-specific detector performance;
- MNAR missing detector outputs;
- capture-recapture with detector interactions;
- excluding retracted papers from detector calibration;
- prevalence estimated from population-random audit alone.

### Gate 3

Do not scale to a global count if posterior results are dominated by prior assumptions or detector missingness.

---

# 8. Phase 4 — citation dependence + contamination

## 8.1 Build seed set

Use E1 and high-posterior E2 works, with reason/field/time strata.

## 8.2 Retrieve first- and second-order citation graph

Primary graph: OpenAlex; biomedical validation: iCite/Scite where useful.

## 8.3 Classify citation dependence

Custom classes:

- background;
- critique;
- method reuse;
- substantive result/data dependence;
- evidence-synthesis inclusion.

Human-code validation set; measure precision/recall.

## 8.4 SCF outcomes

- source-level downstream edge count;
- unique downstream works;
- second-order unique works;
- systematic reviews/meta-analyses;
- guidelines/policies where searchable.

## 8.5 Replicate a known benchmark

Recreate a subset of VITALITY-style contamination before generalizing the classifier.

### Gate 4

Do not call ordinary citations “contamination” unless the dependence classifier validates adequately.

---

# 9. Phase 5 — correction dynamics

For each corrected E1 source:

- pre/post materially dependent citation rate;
- matched paper controls;
- article-age and field-time normalization;
- critique citations separated from reliance citations;
- event-time model.

Estimate:

- residual propagation after correction;
- KGH where decay curve supports it;
- R_E by event time as secondary.

Placebo correction dates test whether apparent decay is just citation aging.

---

# 10. Phase 6 — human and financial burden

## 10.1 NIH cost pilot

Join Retraction Watch/OpenAlex/PubMed to NIH RePORTER.

Reproduce the distinction:

- associated grant exposure;
- attributable direct article/project cost.

Use multiple attribution rules and report ranges.

## 10.2 RLY calibration

Build study-type effort distributions from:

- published project staffing/cost studies;
- grant personnel/period data where available;
- investigator surveys/time-use data;
- trial duration/sample-size proxies;
- manual case studies.

Report RLY as a distribution/scenario until effort calibration is sufficiently empirical.

## 10.3 Integrity Maintenance Debt

Estimate incremental labor from:

- average review hours × verified problematic submissions where submission-level data exist;
- editorial/investigation case studies;
- correction/reanalysis workloads;
- post-publication review/integrity screening.

Avoid applying a global peer-review-hours denominator without a validated problematic-submission fraction.

## 10.4 Participants

Clinical subset joins trial registrations to corrected/problematic publications.

Report invalidated/severely compromised and nonpublished/discontinued trials separately.

---

# 11. Phase 7 — collateral career effects

Replicate/extend known collaborator spillover designs.

Index date: public/formal misconduct finding or correction event.

Controls:

- pre-event productivity;
- field;
- career age;
- collaboration history;
- institution;
- baseline impact;
- topic.

Outcomes:

- citations;
- publication rate;
- funding;
- new collaborators;
- field exit/transition where observable.

Exclude collaborators whose implication status is ambiguous from the innocent-collateral confirmatory sample.

---

# 12. Phase 8 — Innovation Delay pilot

## Unit

Topic cluster / research trajectory, not individual paper.

## Exposure

Large integrity shock with demonstrable pre-correction dependence in the cluster.

## Controls

Matched topic clusters selected using pre-event information only.

## Outcomes

- alternative-topic publication entry;
- alternative-topic share of field attention;
- funding share;
- first high-quality replication/contradiction;
- first adoption threshold.

## Methods

- event study;
- DiD;
- synthetic control for case-intensive analysis;
- placebo shocks;
- negative-control outcomes.

### Gate 5

If pre-trends or control construction fail, retain only descriptive attention/funding shifts and do not report IDY causally.

---

# 13. Phase 9 — Sleeping Beauty extension

## Training corpus

Use mature publication cohorts with sufficient citation follow-up.

Reproduce an established Sleeping Beauty metric and Prince-identification algorithm before custom modeling.

## Analysis order

1. observed SB detection;
2. prediction of awakening within horizon;
3. integrity-shock association with sleep duration among eventual awakeners;
4. counterfactual expected never-awakened count.

## Primary safeguard

The output is an expected number under assumptions, not a list of “great papers the system killed.”

---

# 14. Validation / robustness suite

Required:

- duplicate DOI/title resolution audit;
- manual retraction-reason audit;
- detector calibration/confusion matrices;
- inter-rater reliability/adjudication report;
- weighting diagnostics for enriched audit sample;
- posterior predictive checks;
- prior sensitivity;
- missingness sensitivity;
- capture-recapture interaction sensitivity;
- citation-dependence classifier validation;
- negative controls/placebos for event studies;
- pre-trend plots;
- alternative topic definitions;
- alternative Sleeping Beauty definitions;
- leave-one-field/publisher-out analyses where feasible.

---

# 15. Output package

Planned reproducibility artifacts:

```text
papers/005-hidden-burden-bad-science/
├── paper.json
├── README.md
├── code/
│   ├── build_universe.py
│   ├── classify_retractions.py
│   ├── scenario_model.py
│   ├── latent_prevalence.py
│   ├── contamination_graph.py
│   └── sleeping_beauty.py
├── data/
│   ├── numeric_evidence.csv
│   ├── scenario_parameters.example.json
│   └── README.md
├── manuscript/
└── process/
    ├── IDEA_REPORT.md
    ├── LOSS_ONTOLOGY.md
    ├── ESTIMANDS.md
    ├── CAUSAL_MODEL.md
    ├── DATA_FEASIBILITY.md
    ├── RESEARCH_PLAN.md
    ├── PILOT_DESIGN.md
    ├── AUTO_REVIEW.md
    └── STATUS.md
```

Restricted/raw third-party data will not be committed if redistribution is prohibited.

---

# 16. Definition of success

The project succeeds even if the most speculative outcomes fail.

Minimum publishable success:

1. transparent global publication denominator;
2. detected severe-integrity lower bound with correction-latency analysis;
3. calibrated article-level prevalence pilot showing what can and cannot be inferred;
4. validated downstream-dependence/contamination analysis;
5. at least one human/financial burden module with defensible units;
6. explicit uncertainty and non-identifiability rather than fabricated precision.

The Sleeping Beauty and global opportunity-cost estimates are upside, not requirements for validity.
