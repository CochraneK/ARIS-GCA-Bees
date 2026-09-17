# PILOT DESIGN — ARIS4C005

## Pilot objective

Test the minimum chain required for the ambitious project to be credible:

```text
publication universe
 -> correction join
 -> article-level integrity signals
 -> manual adjudication
 -> latent prevalence calibration
 -> downstream material-dependence classification
```

Human/financial/innovation extensions proceed only after this chain works.

---

# Pilot A — denominator + correction join

## Sample / scope

Initial computational scope:

- publication years 2015–2020 for a fast pilot;
- 3 broad fields with different publication/data structures:
  - biomedical/life sciences;
  - social/behavioral sciences;
  - physical/computational sciences;
- journal articles + reviews;
- DOI-bearing works primary, non-DOI works tracked as denominator sensitivity.

This window gives meaningful correction follow-up while keeping data manageable.

## Tests

- OpenAlex ↔ Crossref DOI coverage;
- duplicate/merged records;
- publication-type agreement;
- Retraction Watch join coverage;
- retraction-reason parsing;
- publication-to-correction latency.

## Audit

Randomly inspect at least 200 matched/unmatched/correction records split across strata.

## Go criterion

- correction-event match precision target ≥ 0.98 in audited DOI-resolved records;
- publication-type mismatch quantified and correctable;
- reason labels sufficiently complete to separate clear E1 from E3/ambiguous cases.

If not, fix the universe/join before downstream analysis.

---

# Pilot B — integrity detector feasibility

## Automated sample

Target 5,000–10,000 articles from Pilot A universe.

Create feature matrix with only detectors that can be legally/reproducibly acquired.

Candidate columns:

- formal correction/retraction;
- expression of concern;
- image anomaly signal;
- text/paper-mill signal;
- duplicate-data/text signal;
- statistical-consistency signal;
- public post-publication concern signal;
- access/missingness indicators.

Not every detector applies to every study type.

## Adjudication sample

Target 750–1,500 papers using:

- population-random sample;
- all/oversampled rare high-specificity signals;
- multi-signal positives;
- single-signal positives;
- signal-negative controls.

Sampling probabilities must be stored so weights can restore population inference.

## Blinding

Where practical, reviewers see the article/evidence needed for integrity assessment but not the model's composite risk score.

## Labels

1. `SEVERE_SUPPORTED`
2. `SERIOUS_UNRESOLVED`
3. `HONEST_MAJOR_ERROR`
4. `MINOR_OR_IMMATERIAL`
5. `NO_MATERIAL_PROBLEM_FOUND`
6. `INDETERMINATE`

## Reliability

Double-code:

- all `SEVERE_SUPPORTED` candidates;
- all initial disagreements;
- random ≥20% of remaining adjudicated set if resources permit.

Record agreement and adjudication reasons.

## Go criterion

The latent model proceeds only if at least one independent signal stream plus the population-random audit provides enough information to prevent prevalence from being prior-driven.

---

# Pilot C — latent prevalence

## Primary outcome

Posterior `P(severe integrity failure)` in the pilot target universe.

## Models

1. population-random audit prevalence (design-based benchmark);
2. Bayesian latent-class model;
3. capture-recapture sensitivity where lists permit.

## Diagnostics

- posterior predictive checks;
- prior sensitivity;
- detector sensitivity/specificity posterior;
- detector correlation residuals;
- missing-not-at-random stress tests;
- retraction-included vs retraction-excluded calibration;
- field leave-one-out.

## Go criterion

A global-scale latent estimate is allowed only if:

- the random-audit estimate and latent model are reconcilable;
- posterior width is materially narrower/more informative than the prior;
- results are not dominated by one detector or one field;
- plausible missingness assumptions do not change the estimate by an order of magnitude.

Otherwise publish the measurement limitations rather than a global count.

---

# Pilot D — material citation dependence

## Seed sources

Approximately 100–300 E1 papers across fields, balanced across citation impact and correction latency.

## Edge sample

Retrieve direct citers; stratify citation edges by:

- pre/post correction;
- section/context where available;
- citation age;
- field;
- source reason.

Human-code 1,000–2,000 citation contexts if feasible.

## Edge labels

- background;
- critique;
- method reuse;
- result/data dependence;
- evidence-synthesis inclusion;
- indeterminate.

## Classifier target

Primary metric for `result/data dependence + evidence-synthesis inclusion`:

- precision prioritized because false contamination claims are costly;
- target precision ≥0.90 before large-scale SCF claims;
- recall reported, not hidden.

## Go criterion

If material dependence cannot be classified reliably across fields, restrict SCF to curated clinical evidence-synthesis pathways rather than pretending all citations are contamination.

---

# Pilot E — Knowledge Ghost Half-Life

## Sample

E1 sources with:

- enough pre-correction materially dependent citations;
- visible correction date;
- matched unretracted/control papers with similar pre-event citation trajectory.

## Analysis

Monthly/quarterly hazard/rate of **new material dependence**, not raw citations.

Event window candidate:

-5 years to +8 years where observation permits.

## Placebos

- pseudo-retraction dates among controls;
- critique citations as a negative/contrast outcome;
- ordinary citation aging model.

## Go criterion

Report KGH only if a decay parameter is identifiable and correction-associated change is distinguishable from natural citation aging.

---

# Pilot F — financial + RLY case study

## Funding

Start with NIH-funded biomedical articles because PMID ↔ NIH project linkage is public and mature.

Replicate:

- associated grant exposure;
- at least two attributable-cost rules.

## RLY

For a small case set, reconstruct effort using:

- project duration;
- team size/roles;
- grant person-months if available;
- trial recruitment/duration;
- explicit published staffing or cost data.

Fit broad effort distributions rather than pretend exact person-years are known.

## Go criterion

RLY may be scaled only if effort distributions have empirical anchors across major study types. Otherwise keep RLY as transparent scenario ranges.

---

# Pilot G — Innovation Delay

## Case selection

Select 5–20 large E1 integrity shocks with:

- strong evidence of substantive downstream dependence;
- identifiable topic cluster;
- enough pre/post years;
- plausible untreated matched topic clusters.

## Topic construction

Use only pre-event embeddings/topics/citations to select controls and avoid look-ahead bias.

## Outcomes

- alternative-topic publication share;
- entry of new authors;
- funding;
- citations/attention;
- time to validated contradictory/alternative finding.

## Go criterion

Require acceptable pre-trends and placebo performance. If not, downgrade to descriptive field-trajectory analysis.

---

# Pilot H — Sleeping Beauty extension

Do not start until Pilot G has a plausible attention/resource-displacement signal.

## Step H1

Reproduce an established Sleeping Beauty algorithm on mature cohorts.

## Step H2

Train awakening model and validate temporally.

## Step H3

Among papers that eventually awaken, test whether exposure to local integrity shocks predicts longer sleep after matching.

## Step H4

Only if H1–H3 survive, estimate expected Never-Woken Sleeping Beauties under counterfactual exposure removal.

---

# Pilot precision planning

Naive binomial reference calculations (not final audit design):

- prevalence 1.0%, margin ±0.2 percentage point at 95%: ~9,508 observations;
- prevalence 0.5%, margin ±0.1 percentage point at 95%: ~19,112 observations.

Because manual adjudication is expensive, the project uses two-phase sampling and detector-assisted calibration rather than manually reviewing tens of thousands of papers.

---

# Pilot outputs

A successful pilot leaves behind:

```text
universe_coverage.csv
correction_match_audit.csv
retraction_reason_codebook.csv
detector_features.parquet (or reproducible derived equivalent)
adjudication_protocol.md
adjudication_sample.csv
latent_model_diagnostics/
citation_context_gold.csv
dependence_classifier_metrics.json
pilot_results.md
```

Raw/restricted full text is not committed to the public repository.
