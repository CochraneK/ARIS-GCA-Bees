# ARIS4C015 Research Plan

## Research question

Can an open-data, integrity-aware, temporally reconstructed evidence system identify still-dormant scientific papers that later show delayed recognition more effectively than simple citation-momentum baselines, while remaining auditable and calibrated?

## Study architecture: three tracks

ARIS4C015 separates three questions that require different sampling designs.

### Track A — Retrospective identification

Use large retrospective corpora to identify robust delayed-recognition cases from
complete citation histories.

A robust mechanism case should not be created merely because it is top-q inside
a small random sample. Track A uses converging retrospective evidence such as:

- Beauty Coefficient;
- sleep depth / length / wake intensity;
- source-calibrated B thresholds;
- later-recognition floors;
- sensitivity definitions.

### Track M — Mechanism discovery

Use a case-enriched dataset of robust Sleeping Beauties plus matched controls.

Primary contrasts:

- Sleeping Beauty vs Forgotten: both start low, only one later awakens;
- Sleeping Beauty vs Immediate Hit: both end high, but recognition timing differs.

Mechanism inference is blocked if the corpus contains zero robust SB cases.

See process/MECHANISM_TRACK.md.

### Track B — Prospective rediscovery

Use reproducible random historical cohorts and freeze all predictors at cutoff T.

Relative delayed-recognition outcomes such as top-q future B remain legitimate
benchmark labels here, but they are not retrospective SB diagnoses.

Population prevalence and predictive performance are estimated only from this
random/time-safe track, not from the case-enriched mechanism dataset.

## Main hypothesis family

### H1 — Multi-evidence value
At a fixed review budget, a model combining time-safe semantic, network and citation-trajectory evidence will outperform citation-only baselines in retrieving papers that later show delayed recognition.

### H2 — Independent information
At least one non-citation feature family contributes measurable out-of-time information after controlling for field, cohort, age and citation history.

### H3 — Integrity-aware utility
Routing unresolved integrity/provenance concerns through the 011 quarantine layer improves the usefulness of the human-review shortlist without treating integrity screening as a merit signal.

### H4 — Cross-field robustness
Performance will vary by field and era. A credible model should retain some value under leave-field-out and leave-era-out validation rather than depending entirely on one domain.

### H5 — Cross-source robustness
Delayed-recognition geometry should be distinguishable from bibliographic-database coverage. Absolute Beauty Coefficient values may shift across Web of Science, OpenAlex, SciSciNet and other graphs, but a useful agent should characterize which parts of the signal are stable (for example awakening timing or rank ordering), report source sensitivity explicitly, and avoid treating one source-specific B threshold as universal.

Initial Pilot 0B evidence motivates this hypothesis: three selected classic cases reconstructed from OpenAlex through the 2011 observation endpoint retain the delayed-recognition pattern; absolute B values differ from the published WoS values while awakening timing is much closer. This is a small implementation probe, not yet a general test of H5.

## Non-hypotheses

The project will not test or claim that:
- citations equal truth;
- delayed recognition guarantees scientific importance;
- a candidate will become a breakthrough;
- low citations imply suppression;
- integrity anomalies imply misconduct.

## Phase 0 — Metric fidelity

Implement:
- Beauty Coefficient B;
- awakening time;
- tie-policy tests;
- known synthetic trajectories;
- cross-check against SciSciNet or published examples where feasible.

Exit criterion:
- formulas reproduce hand-calculated / external reference values within numerical tolerance.

## Phase 1 — Corpus and historical snapshots

Start with a bounded pilot:
- one or two well-indexed fields;
- publication cohorts old enough to provide a dormant period plus future evaluation horizon;
- OpenAlex / SciSciNet citation and network data.

Create a normalized schema:

```text
paper_id
publication_year
field
cutoff_year
citation_history_to_cutoff
references_available_to_cutoff
citing_papers_available_to_cutoff
semantic_features_to_cutoff
network_features_to_cutoff
technology_features_to_cutoff
integrity_features_to_cutoff
future_outcomes_hidden_from_model
```

## Phase 2 — Label sensitivity

Construct multiple delayed-recognition outcomes.

Candidate label families:
- future B percentile within field/cohort;
- awakening within H years;
- field-normalized future citation acceleration;
- top-q delayed-recognition rank;
- survival time to awakening.

Do not select the final definition after looking at test performance.

## Phase 3 — Baselines

Required:
1. random within age/field strata;
2. current citation count;
3. recent citation momentum;
4. recent acceleration;
5. citation trajectory only;
6. semantic novelty only;
7. network only.

The full model must justify itself against these baselines.

## Phase 4 — Feature families

### Citation
- counts by year through cutoff;
- recent slope / acceleration;
- dormancy length;
- age-normalized and field-normalized uptake;
- citing-paper diversity.

### Semantic
- contemporaneous semantic novelty;
- atypical concept combinations;
- distance to dominant field clusters;
- cross-field semantic bridge score.

### Network
- bibliographic coupling;
- co-citation emergence;
- bridge / brokerage features;
- diversity of citing communities;
- centrality using only cutoff-safe graph state.

### Reuse
- data / code / method reuse where reliably timestamped.

### Technology
- patent / NPL linkage only where legally and reproducibly available.

### Integrity
Imported from 011 as:
- CLEAR;
- CAUTION;
- QUARANTINE;
- ABSTAIN.

Integrity state is not a scientific-value predictor.

## Phase 5 — Prospective backtest

Evaluation design:
- train on older cohorts;
- validate on later cohorts;
- test on a still later untouched cohort;
- repeat by field;
- leave-field-out stress test;
- leave-era-out stress test.

Metrics:
- Precision@K;
- Recall@K;
- NDCG@K;
- AUPRC when class labels are used;
- Brier / calibration error for probabilities;
- lead time;
- review yield per 100 dossiers.

## Phase 6 — Prince analysis

For retrospectively awakened papers:
- identify candidate Prince paper(s);
- test timing;
- semantic proximity;
- network position;
- whether awakening is sudden or distributed;
- whether multiple independent communities contribute.

Do not force every awakening into a single-Prince narrative.

## Phase 7 — 011 integration

Join on DOI / OpenAlex ID / PMID where possible.

Rules:
- findings after cutoff are hidden in Track B;
- unresolved high-severity issues route to QUARANTINE;
- missing integrity coverage returns ABSTAIN;
- 011 evidence appears verbatim/provenanced in the candidate dossier;
- no integrity finding changes a paper into a "bad paper" label.

## Phase 8 — Candidate dossiers and human review

Sample:
- top-ranked candidates;
- near-threshold candidates;
- false positives from backtests;
- false negatives;
- integrity-quarantined high-score candidates;
- low-prestige / low-visibility candidates surfaced by the model.

Human reviewers score:
- plausibility of rediscovery value;
- evidence coherence;
- obvious leakage / metadata artifacts;
- usefulness of explanation;
- time required per dossier.

## Phase 9 — Scale

Only after the pilot passes:
- broaden fields and eras;
- build scheduled refresh;
- add optional patent and software/data reuse sources;
- produce searchable Sleeping Beauty atlas;
- expose machine-readable Evidence Cards.

## Failure criteria

015 should be considered unsuccessful or substantially revised if:
- simple citation momentum performs as well as the full system;
- performance collapses out of field / era;
- rankings are mainly journal / institution prestige proxies;
- labels are unstable across reasonable SB definitions;
- data-source coverage dominates the model;
- historical reconstruction cannot prevent material leakage;
- evidence cards are not useful to human reviewers.

## Deliverables

- `code/sb_metrics.py`
- metric tests
- historical-cutoff dataset builder
- baseline benchmark
- prospective model benchmark
- 011 adapter
- Candidate Evidence Card schema + examples
- manuscript / technical report
- optional public discovery interface after validation
