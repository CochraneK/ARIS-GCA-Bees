---
name: sleeping-beauty-miner
description: Mines scientific literature for delayed-recognition patterns and still-dormant rediscovery candidates using time-safe citation trajectories, semantic and network evidence, Prince-paper analysis, and ARIS4C011 integrity/provenance gating. Use for retrospective Sleeping Beauty analysis, historical-cutoff backtests, or auditable candidate discovery. Produces evidence cards and rankings, never a guarantee of future impact or scientific validity.
compatibility: Python 3.10+ for bundled deterministic utilities. Network access is optional for local SciSciNet slices and required for live OpenAlex enrichment.
metadata:
  author: CochraneK
  project: ARIS4C015
  version: "0.1.0"
  depends_on: ARIS4C011
---

# Sleeping Beauty Miner

## Purpose

Use this skill to identify delayed-recognition citation patterns and to construct auditable shortlists of still-dormant papers that may deserve renewed human attention.

There are three distinct scientific tasks:

1. **Retrospective identification** — measure delayed recognition after enough citation history exists.
2. **Mechanism discovery** — build a case-enriched set of robust Sleeping Beauties and matched controls to study why recognition was delayed and what triggered awakening.
3. **Prospective discovery** — at a historical cutoff T, rank papers using only evidence that existed by T, then evaluate against future outcomes hidden from the model.

Do not conflate them. A random prospective cohort may contain zero genuine Sleeping Beauties; relative top-q outcomes in that cohort are benchmark labels, not mechanism diagnoses.

## Core invariants

1. Never equate citation impact with truth, validity, or intrinsic scientific value.
2. Never call a prospective candidate a breakthrough merely because it ranks highly.
3. Never use information that became available after the prospective cutoff.
4. ABSTAIN / missing evidence is not LOW VALUE.
5. Prefer transparent deterministic baselines before learned ranking models.
6. Institution prestige, country, nationality, journal prestige, and author fame are not intrinsic-value features.
7. Preserve field and publication-age context when comparing citation trajectories.
8. Report multiple reasonable Sleeping Beauty definitions or sensitivity analyses rather than relying on one arbitrary threshold.
9. Reuse ARIS4C011 for integrity/provenance evidence; do not turn anomalies into allegations of misconduct.
10. Integrity findings may quarantine or lower confidence in a candidate, but absence of integrity flags must not add scientific-value points.
11. Every candidate must have a machine-readable Candidate Evidence Card with provenance and uncertainty.
12. Human review is required before promotion into a rediscovery shortlist intended for substantive scientific follow-up.

## Modes

### RETROSPECTIVE

Use when the citation trajectory is observed through a sufficiently long follow-up window.

Compute:
- yearly zero-filled citation history;
- Beauty Coefficient B;
- peak time t_m;
- awakening time t_a;
- sleeping length;
- alternative SB definitions when available;
- candidate Prince papers and awakening-path evidence.

This mode may say that a trajectory is consistent with delayed recognition only under a declared rule. Do not silently invent a threshold.

### MECHANISM

Use when asking why robust delayed-recognition cases slept and later awakened.

Required workflow:
- start from a large retrospective corpus, not a tiny random cohort;
- apply a robust SB gate using converging retrospective evidence;
- construct field/cohort-normalized SLEEPING_BEAUTY / FORGOTTEN / IMMEDIATE_HIT / FADING states;
- match SBs to Forgotten controls on early-life observables;
- separately compare SBs with Immediate Hits;
- analyze reference/network/semantic/Prince mechanisms.

Hard stop:
- if no robust SB cases pass, set mechanism_ready=false;
- do not force top-q benchmark papers to become SB cases;
- do not estimate prospective precision/recall from the enriched mechanism cohort.

See ../../process/MECHANISM_TRACK.md and ../../code/mechanism_cohort.py.

### PROSPECTIVE

Use when asking: "Could this paper have been surfaced at historical cutoff T?"

Only use data demonstrably available on or before T.

Allowed evidence families may include:
- cutoff-safe citation trajectory;
- citation momentum / acceleration;
- semantic novelty measured against the contemporaneous corpus;
- atypical concept combinations;
- network brokerage / bridge structure;
- diversity of citing communities available by T;
- method/data/software reuse known by T;
- patent linkage known by T;
- 011 integrity/provenance evidence known by T.

Forbidden future leakage includes:
- citations after T;
- later retractions, corrections, or expressions of concern;
- later awards or prizes;
- later reviews calling the paper foundational;
- later patent citations;
- later author fame or career outcomes;
- embeddings or corpus features trained on future-only information unless historical reconstruction is validated.

### DISCOVERY_SCAN

Use for a field/cohort search.

Inputs should include:
- corpus definition;
- publication cohorts;
- cutoff year;
- review budget K;
- normalization strata;
- baseline strategy;
- optional validated learned model.

Output:
- ranked Candidate Evidence Cards;
- quarantined candidates separately;
- abstention and missing-data counts;
- audit trail of inclusion/exclusion decisions.

## Data-source strategy

Preferred large-scale backbone: **SciSciNet-v2**, because it is rebuilt on OpenAlex and exposes large publication/citation/linkage resources plus science-of-science metrics.

Use OpenAlex for:
- canonical IDs;
- metadata enrichment;
- topics;
- references;
- bounded citation retrieval;
- validation cases.

Do not use a Work's recent `counts_by_year` as a complete decades-long citation history. Reconstruct the trajectory from incoming citation edges joined to citing-paper publication years, explicitly inserting zero-citation years.

Read references/DATA_CONTRACT.md before adding a new source.

## Workflow

### 1. Establish task and temporal boundary

Record:
- paper/corpus identifier;
- analysis mode;
- publication year;
- observation endpoint;
- prospective cutoff if applicable;
- field/topic stratum;
- source snapshot/version.

If the requested prospective cutoff cannot be reconstructed, return ABSTAIN or mark the feature family unavailable.

### 2. Build a complete citation trajectory

Preferred method:
1. collect incoming citation edges;
2. join each citing work to publication year;
3. aggregate by year;
4. insert missing zero-citation years;
5. record invalid pre-publication citation edges separately;
6. compare reconstructed totals with source totals as a diagnostic.

A source update mismatch is a data-quality warning, not evidence of misconduct.

### 3. Run deterministic retrospective metrics

Compute:
- Beauty Coefficient;
- peak time;
- awakening time.

These are descriptive metrics. Do not automatically label a paper a Sleeping Beauty without an explicit classification policy.

### 4. Freeze the prospective view

For cutoff T:
- truncate the citation graph to <= T;
- truncate metadata/status events to <= T;
- reconstruct semantic/network features from cutoff-safe corpus state;
- exclude any feature with unknown availability when leakage risk is material.

### 5. Run transparent baselines first

Required baseline families:
- current citations at T;
- recent 3-year momentum;
- recent acceleration;
- partial-trajectory Beauty Coefficient;
- simple dormancy.

A learned model must beat these under out-of-time evaluation.

### 6. Add independent evidence families

After baseline plumbing is validated, add:
- semantic novelty;
- atypical combinations;
- network bridge/brokerage;
- citation-community diversity;
- reuse signals;
- technology transfer;
- Prince-related structure when temporally valid.

Do not naively sum incomparable features. Use prespecified normalization and calibrated models where appropriate.

### 7. Apply ARIS4C011 integrity gate

For each 011 finding:
- verify applicability;
- preserve evidence class and dependency group;
- verify the finding was available before T in prospective mode;
- exclude future findings;
- mark unknown-time findings ABSTAIN for prospective use.

Routing:
- CLEAR — applicable cutoff-safe checks have no FLAG;
- CAUTION — unresolved flag(s) need attention;
- QUARANTINE — strong independent or deterministic unresolved findings require human review before discovery promotion;
- ABSTAIN — coverage or timing is insufficient.

Quarantine is not a misconduct verdict.

### 8. Build Candidate Evidence Card

Every card should answer:
- What paper is this?
- What was known at the cutoff?
- Which evidence families were applicable?
- Which signals supported or contradicted rediscovery priority?
- What evidence was missing?
- What did 011 find?
- Was anything quarantined?
- What score/rank is shown, and what does it mean?
- Which source/snapshot produced each feature?
- What should a human reviewer inspect next?

Use assets/candidate-card.schema.json.

### 9. Human-review shortlist

Do not simply take top K if the model is dominated by one field or coverage regime.

Audit:
- field balance;
- cohort/age balance;
- language/indexing coverage;
- open-access coverage;
- institutional/geographic strata for bias diagnosis only.

### 10. Backtest before claiming usefulness

Historical-cutoff benchmark:
- train on older cohorts;
- validate on later cohorts;
- test on untouched later cohorts;
- leave-field-out stress test;
- leave-era-out stress test;
- feature-family ablation.

Primary metrics:
- Precision@K;
- Recall@K;
- NDCG@K;
- calibration if probabilities are emitted;
- lead time;
- yield per 100 human-reviewed candidates.

## Prince analysis

A Prince is a candidate work or event plausibly associated with awakening.

Do not force a single-Prince explanation. Consider:
- multiple Prince papers;
- gradual awakening;
- independent communities;
- review/guideline/technology events;
- semantic proximity and temporal ordering.

A Prince association is descriptive unless a causal design supports stronger language.

## Evidence semantics

Suggested evidence status:
- SUPPORTIVE
- CONTRADICTORY
- NEUTRAL
- ABSTAIN
- QUARANTINED

Each signal records:
- applicability;
- cutoff safety;
- value;
- uncertainty;
- provenance;
- notes.

## Output language

Preferred wording:
- "candidate for rediscovery review"
- "trajectory consistent with delayed recognition under definition X"
- "high priority under baseline/model Y"
- "integrity evidence requires review"

Avoid:
- "this paper is true"
- "this paper will become a breakthrough"
- "the authors committed misconduct"
- "low citation means suppression"

## Bundled resources

- references/DATA_CONTRACT.md — temporal, source, and reconstruction rules.
- assets/candidate-card.schema.json — machine-readable Candidate Evidence Card.
- scripts/orchestrator.py — deterministic reference orchestrator.
- ../../code/sb_metrics.py — Beauty Coefficient and awakening time.
- ../../code/citation_history.py — annual-history reconstruction.
- ../../code/baselines.py — transparent prospective baselines.
- ../../code/integrity_adapter.py — ARIS4C011 routing adapter.
- ../../code/openalex_adapter.py — bounded OpenAlex ingestion.
- ../../code/sciscinet_adapter.py — local SciSciNet-v2 slice adapter.
- ../../code/mechanism_labels.py — robust SB and four-state mechanism labels.
- ../../code/mechanism_matching.py — matched controls for mechanism contrasts.
- ../../code/mechanism_cohort.py — case-enriched mechanism cohort builder.
