# ARIS4C015 — Sleeping Beauty Miner

## Working title

**Sleeping Beauty Miner: An Integrity-Aware, Time-Safe Agent for Discovering Delayed and Under-Recognized Scientific Work**

## Core objective

Build an auditable agent that does three different jobs without conflating them:

1. **Retrospective identification** — identify papers whose complete citation histories robustly support delayed recognition.
2. **Mechanism discovery** — compare robust Sleeping Beauties with matched Forgotten / Immediate-Hit controls to study why recognition was delayed and what triggered awakening.
3. **Prospective mining** — rank still-dormant papers that may deserve renewed human attention **before** an awakening is visible.

A random prospective cohort is not guaranteed to contain a genuine Sleeping Beauty. Cohort-relative top-q outcomes therefore remain benchmark labels only; they cannot be used to manufacture mechanism cases.

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
- SciSciNet (2023), *Scientific Data*, DOI: 10.1038/s41597-023-02198-9 — large science-of-science benchmark data and precomputed Sleeping Beauty metrics.
- **SciSciNet-v2** — refreshed OpenAlex-based release with substantially larger publication, citation and patent-linkage coverage.

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

## Three research tracks

### Track A — Retrospective identification

Goal: reproduce known delayed-recognition patterns from citation histories.

Primary outputs:
- B and awakening time;
- alternative SB definitions as sensitivity analyses;
- field / cohort distributions;
- Prince candidates.

This track validates implementation; it is not the main scientific claim.

### Track M — Mechanism discovery

Goal: study delayed-recognition mechanisms using a case-enriched retrospective cohort.

Primary design:
- robust SB gate from converging retrospective definitions;
- field/cohort-normalized SLEEPING_BEAUTY / FORGOTTEN / IMMEDIATE_HIT / FADING states;
- SB vs Forgotten matched comparison;
- SB vs Immediate-Hit matched comparison;
- Prince / awakening-path analysis.

Hard rule:
- if zero robust SB cases exist, mechanism analysis is blocked;
- relative top-q benchmark positives are not renamed as Sleeping Beauties.

See process/MECHANISM_TRACK.md.

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

- **SciSciNet-v2 (preferred large-scale backbone)** — refreshed OpenAlex-based science-of-science data with citation and patent linkages.
- **SciSciNet v1** — useful for reproducing published Sleeping Beauty metrics and cross-checking the B implementation.
- **OpenAlex** — canonical IDs, works, references, citations, topics and authorship metadata.
- **Crossref** — DOI metadata and update / relation metadata.
- **OpenCitations** — open citation edges for cross-validation where useful.
- **PubMed / Europe PMC** — biomedical metadata and full-text-linked signals where available.

### Important OpenAlex caveat

The `counts_by_year` field on a Work exposes only roughly the most recent ten years of yearly citation counts and omits zero-citation years. It therefore cannot by itself reconstruct a decades-long Sleeping Beauty trajectory.

For historical SB work, 015 must either:

1. reconstruct yearly citations from citation edges joined to citing-paper publication years; or
2. use a dataset such as SciSciNet / SciSciNet-v2 that contains the necessary graph structure or precomputed metrics.

Commercial or restricted sources may be used for external validation, but the canonical benchmark should remain reproducible from open data if feasible.

## Current state

**PILOT 1 HISTORICAL BENCHMARK + MECHANISM TRACK IMPLEMENTATION.**

Current empirical state:

- 3 classic SB cross-source OpenAlex/WoS probes completed;
- 10 random field/era/seed strata;
- 200 prospective-benchmark target papers;
- 7 delayed-recognition outcome definitions;
- 5 citation baselines;
- seed-sensitivity analysis completed;
- recognition-floor sensitivity completed;
- historical lexical-novelty ablation completed as a negative / insufficient feature-family result;
- OpenAlex 429 retry/backoff and request-reduction hardening implemented.

Citation-only baselines do not show a stable winner for the difficult awakening /
delayed-recognition-consensus outcomes. The strongest result varies by stratum,
which keeps the benchmark non-trivial.

Mechanism Track now adds:

- robust retrospective SB gate;
- source-calibrated B threshold support;
- van-Raan-style sleep/depth/wake gate;
- later-recognition floor;
- four canonical trajectory states;
- deterministic matched controls;
- mechanism_ready hard gate that blocks inference when no robust SB exists.

### Immediate next gates

1. connect a reproducible SciSciNet-v2 / SciSciNet query or slice;
2. use SB_B only as a cheap candidate prefilter, then reconstruct trajectories;
3. build the first empirical robust-SB mechanism cohort;
4. measure SB-vs-Forgotten and SB-vs-Immediate-Hit match yield / balance;
5. add reference-combination and network mechanism features;
6. run Prince / awakening-trigger analysis;
7. return mechanism-derived, cutoff-safe features to the prospective benchmark;
8. train learned models only after independent feature families show stable value.

Canonical execution state: process/STATUS.md  
Mechanism design: process/MECHANISM_TRACK.md  
Pilot 1 citation results: process/PILOT1_RESULTS.md
