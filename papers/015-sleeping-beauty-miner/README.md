# ARIS4C015 — Sleeping Beauty Miner

## Working title

**Sleeping Beauty Miner: An Integrity-Aware, Time-Safe Agent for Discovering Delayed and Under-Recognized Scientific Work**

## Core objective

Build an auditable agent that does two different jobs without conflating them:

1. **Retrospective identification** — identify papers whose later citation histories already show delayed recognition ("Sleeping Beauties").
2. **Prospective mining** — rank still-dormant papers that may deserve renewed human attention **before** an awakening is visible.

The second task is the more useful and more difficult one. The agent must never present a high ranking as proof that a paper is important or will awaken.

## Relationship to ARIS4C011

015 reuses the architecture of **011 Research Forensics** rather than duplicating it.

011 supplies the evidence-safety layer:

- applicability-aware checks;
- ABSTAIN / NOT_APPLICABLE semantics;
- Evidence Graph representation;
- citation and metadata verification;
- provenance and post-publication-status checks;
- statistical / numerical / image / text / corpus anomaly modules when applicable;
- human-review outputs;
- strict separation between observed anomalies and claims about intent.

015 adds a discovery layer above that foundation.

**Rule:** integrity evidence is primarily a **gate / quarantine / uncertainty modifier**, not a positive "quality score." A paper should not rank highly merely because no problem was detected.

## Relationship to ARIS4C005

005 studies the hidden opportunity cost of bad science. 015 can supply an explicit, auditable set of **never-woken / not-yet-woken candidates** to 005.

The link is exploratory unless a causal design is available:

- 015 may estimate an awakening probability or discovery priority;
- 005 may ask whether bad-science exposure plausibly displaced attention;
- neither project may infer that a specific paper "would have become important" without a defensible counterfactual design.

## Prior art and novelty boundary

The project does **not** claim to invent Sleeping Beauty detection or early prediction.

Key prior work includes:

- Ke, Ferrara, Radicchi & Flammini (2015), *PNAS*, DOI: 10.1073/pnas.1424329112 — Beauty Coefficient and awakening time.
- Du & Wu (2018), *Scientometrics*, DOI: 10.1007/s11192-018-2780-0 — Bcp for under-cited Sleeping Beauties.
- Miura et al. (2021), *Applied Network Science*, DOI: 10.1007/s41109-021-00389-0 — large-scale Sleeping Beauty / Prince extraction.
- *Early identification of breakthrough research from sleeping beauties using machine learning* (2024), *Journal of Informetrics* 18(2):101517 — prospective ML framing.
- SciSciNet (2023), *Scientific Data*, DOI: 10.1038/s41597-023-02198-9 — open science-of-science data including precomputed Sleeping Beauty coefficients.

015 targets the integration gap: **open/reproducible data, time-safe prospective backtesting, multi-signal evidence fusion, integrity-aware quarantine, explainable candidate dossiers, and explicit Prince / awakening-path analysis.**

## Agent outputs

Every paper is assigned one of the following states, with uncertainty:

- **CONFIRMED_DELAYED_RECOGNITION** — retrospective citation history strongly supports delayed recognition.
- **AWAKENING_NOW** — recent acceleration is visible but long-run status is not yet settled.
- **DORMANT_CANDIDATE** — low current recognition plus independent evidence that merits human review.
- **INTEGRITY_QUARANTINED** — potentially interesting, but 011 raises unresolved integrity / provenance concerns.
- **INSUFFICIENT_DATA / ABSTAIN** — required evidence is missing or the task is not applicable.

The atomic artifact is a **Candidate Evidence Card**, not a single opaque score.

## Evidence families

### A. Citation-trajectory evidence
- Beauty Coefficient B.
- Bcp or related parameter-light sensitivity analysis.
- Sleeping length / depth.
- Citation acceleration and burst structure.
- Field- and age-normalized citation uptake.
- Citation inflation sensitivity.

### B. Semantic evidence
- semantic novelty relative to the contemporaneous literature;
- atypical combinations of concepts;
- distance from dominant topic clusters;
- later growth of the paper's semantic neighborhood.

### C. Network evidence
- bridge / brokerage position;
- community diversity of citing papers;
- co-citation emergence;
- reference-network atypicality;
- proximity to newly expanding research communities.

### D. "Prince" evidence
- candidate papers that plausibly trigger renewed attention;
- temporal ordering around awakening;
- semantic and citation relationship between candidate Prince and Sleeping Beauty;
- multiple-Prince and gradual-awakening cases.

### E. Scientific-to-technological transfer
Where licensing and coverage permit:
- patent citations to papers;
- lag from publication to technological citation;
- technology-first vs science-first awakening.

Patent linkage is an optional evidence family, not a mandatory feature, because coverage differs by source and field.

### F. Independent value signals
Only time-safe signals available at the prediction cutoff may be used, such as:
- reproducible method / dataset reuse;
- guideline or standards uptake where timestamped;
- software / data reuse where reliably linked;
- replication or conceptual reuse that is not already captured by raw citation counts.

### G. Integrity / provenance evidence from 011
- retraction / correction / expression-of-concern status;
- citation verification;
- statistical / image / textual / metadata findings when applicable;
- provenance and registration checks;
- corpus-level anomaly signals.

These findings affect confidence and review routing. They do not establish misconduct.

## Two benchmark tracks

### Track A — Retrospective identification

Goal: reproduce known delayed-recognition patterns from citation histories.

Primary outputs:
- B and awakening time;
- alternative SB definitions as sensitivity analyses;
- field / cohort distributions;
- Prince candidates.

This track validates implementation; it is not the main scientific claim.

### Track B — Prospective discovery

At historical cutoff year **T**, the model may use only information available on or before T.

It ranks papers that are dormant at T and evaluates whether they show delayed recognition during a fixed future horizon.

Required safeguards:
- chronological train / validation / test splits;
- no future citation, metadata-update, retraction, award, review, or patent leakage;
- age- and field-matched baselines;
- leave-field-out and leave-era-out stress tests;
- detector-family / feature-family ablations;
- calibration and review-budget metrics.

## Primary estimands

015 is fundamentally a ranking / triage problem.

Primary metrics:

- Precision@K and Recall@K at a fixed human-review budget;
- NDCG@K for ranked delayed-recognition outcomes;
- calibration of future-awakening probabilities when probabilities are emitted;
- median lead time before observed awakening;
- yield per 100 papers manually reviewed.

Benchmark against:
- random age/field-matched ranking;
- raw citation momentum;
- citation acceleration only;
- semantic novelty only;
- network features only;
- historical B-like trajectory features only where time-safe.

## Strong design rules

1. **No future leakage.**
2. **ABSTAIN is not LOW VALUE.**
3. Citation count is an attention signal, not truth or scientific merit.
4. Institution prestige, country, nationality, author fame, and journal prestige are not intrinsic-value features. They may be audited as confounders or bias channels, not used to define merit.
5. A predicted candidate is not called a breakthrough.
6. Integrity anomalies are not allegations of misconduct.
7. Retraction is not synonymous with fraud; reasons are coded separately.
8. Field and publication-age effects must be normalized or explicitly stratified.
9. Multiple Sleeping Beauty definitions must be reported; conclusions may not depend on one arbitrary threshold.
10. Any learned model must be compared against transparent deterministic baselines.
11. Candidate Evidence Cards must expose which evidence families were applicable, missing, supportive, contradictory, or quarantined.
12. The prospective benchmark must freeze the data state at historical cutoffs as closely as available sources permit.

## Open-data-first stack

Preferred sources, subject to current licensing and coverage:

- **OpenAlex** — works, citation graph, topics, authorship metadata and yearly citation information where available.
- **SciSciNet** — large-scale science-of-science tables and precomputed Sleeping Beauty coefficient for implementation cross-checks.
- **Crossref** — DOI metadata and update / relation metadata.
- **OpenCitations** — open citation edges for cross-validation where useful.
- **PubMed / Europe PMC** — biomedical metadata and full-text-linked signals where available.
- patent / NPL sources only where reproducible access and licensing permit.

Commercial or restricted sources may be used for external validation, but the canonical benchmark should remain reproducible from open data if feasible.

## Current state

**PROJECT INITIALIZED / AGENT SPECIFICATION v0.1.**

Immediate next steps:

1. build a deterministic retrospective metric module (B + awakening time);
2. create a tiny known-case implementation test;
3. design a historical-cutoff benchmark schema;
4. implement OpenAlex / SciSciNet ingestion;
5. run Pilot 0 on a bounded field/cohort before scaling;
6. connect 011 integrity evidence as a quarantine / uncertainty layer;
7. only then train prospective ranking models.
