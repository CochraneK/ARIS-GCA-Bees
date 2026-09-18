# ARIS4C015 Agent Specification v0.1

## 1. Purpose

The Sleeping Beauty Miner is a **scientific-discovery triage agent**.

It does not decide that a paper is true, important, fraudulent, or destined to become influential. It gathers independent evidence about delayed recognition and creates an auditable priority ranking for human review.

## 2. Reuse contract with 011

015 imports the following invariants from ARIS4C011:

- detector / signal applicability is explicit;
- missing or inapplicable evidence returns ABSTAIN / NOT_APPLICABLE;
- evidence is represented separately from interpretation;
- downstream synthesis must preserve provenance;
- post-publication information is forbidden in time-safe tracks if it occurred after the cutoff;
- integrity findings cannot be converted into claims about author intent;
- weak detector families cannot independently justify high-confidence claims;
- feature-family ablation is required to detect shortcut dependence.

### 011 -> 015 adapter

011 finding:

```text
finding_id
paper_id
family
applicable
observed_evidence
confidence
provenance
benign_alternatives
human_review_required
timestamp_available
```

015 consumes it as:

```text
integrity_gate:
  state: CLEAR | CAUTION | QUARANTINE | ABSTAIN
  reasons: [...]
  cutoff_safe: true | false
  confidence_modifier: [...]
```

The adapter may lower confidence or quarantine a candidate. It may not add positive "scientific value" merely because the integrity layer is quiet.

## 3. Main operating modes

### mode=RETROSPECTIVE

Input:
- paper identifier;
- complete citation history through analysis date.

Output:
- Beauty Coefficient B;
- awakening time;
- sensitivity definitions (e.g. Bcp when implemented);
- candidate Prince papers;
- classification as delayed-recognition pattern or not;
- evidence card.

### mode=MECHANISM

Input:
- a large retrospective corpus or prefiltered candidate set;
- complete annual citation histories;
- field/cohort strata;
- optional source-calibrated Sleeping Beauty metrics.

Output:
- robust-SB gate results;
- four-state trajectory classification:
  SLEEPING_BEAUTY / FORGOTTEN / IMMEDIATE_HIT / FADING;
- explicit AMBIGUOUS / LOW_EARLY_HIGH_LATE_UNCONFIRMED states;
- matched SB-vs-Forgotten and SB-vs-Immediate-Hit contrasts;
- candidate Prince / awakening-path evidence;
- mechanism-ready boolean and block reason.

Hard rule:
- if zero robust SB cases are present, return mechanism_ready=false;
- do not manufacture SB cases from cohort-relative top-q labels;
- do not report prospective precision/recall from the case-enriched mechanism sample.

See process/MECHANISM_TRACK.md.

### mode=PROSPECTIVE

Input:
- historical cutoff T;
- only evidence timestamped <= T.

Output:
- candidate priority;
- probability / score only if calibrated;
- evidence-family vector;
- integrity gate;
- missing-evidence map;
- expected reason for priority;
- explicit uncertainty;
- human-readable evidence card.

### mode=DISCOVERY_SCAN

Input:
- corpus query / field / cohort / cutoff;
- review budget K.

Output:
- top-K candidates;
- diversity-aware shortlist;
- excluded / quarantined / abstained counts;
- audit log describing why candidates entered or left the shortlist.

## 4. Evidence Graph

Suggested node types:

- PAPER
- CITATION_YEAR
- CITING_PAPER
- REFERENCE
- TOPIC
- SEMANTIC_CLUSTER
- AUTHOR
- DATASET
- SOFTWARE
- PATENT
- PRINCE_CANDIDATE
- INTEGRITY_FINDING
- POST_PUBLICATION_EVENT
- EVIDENCE_SOURCE
- MODEL_OUTPUT

Suggested edge types:

- CITES
- COCITED_WITH
- SEMANTICALLY_NEAR
- BRIDGES_CLUSTER
- REUSES_METHOD
- REUSES_DATA
- CITES_IN_PATENT
- POSSIBLE_PRINCE_OF
- HAS_INTEGRITY_FINDING
- SUPPORTED_BY_SOURCE
- AVAILABLE_BEFORE_CUTOFF

Every model feature used in Track B should be traceable to timestamped Evidence Graph nodes / edges.

## 5. Prospective signal contract

Each signal returns:

```json
{
  "name": "semantic_novelty",
  "family": "semantic",
  "applicable": true,
  "value": 0.73,
  "direction": "supportive",
  "cutoff_safe": true,
  "provenance": ["..."],
  "uncertainty": "...",
  "notes": "..."
}
```

If a signal is unavailable:

```json
{
  "name": "patent_linkage",
  "family": "technology_transfer",
  "applicable": false,
  "status": "ABSTAIN",
  "reason": "coverage unavailable for this field/cohort"
}
```

## 6. Candidate Evidence Card

Minimum fields:

- canonical paper identifiers;
- publication year and analysis cutoff;
- field / topic strata used for normalization;
- current-at-cutoff citation trajectory;
- retrospective metrics if permitted by mode;
- prospective evidence-family summary;
- candidate Prince information if available before cutoff;
- 011 integrity gate;
- contradictory evidence;
- missing evidence;
- model / rule version;
- rank and uncertainty;
- plain-language explanation;
- explicit statement: "This is a discovery-priority estimate, not a validity or breakthrough judgment."

## 7. Ranking architecture

### Pilot 0
Use transparent deterministic rules / bounded feature aggregation only.

Purpose:
- validate data plumbing;
- expose leakage;
- establish baselines;
- measure coverage.

Pilot 0 ranking must be labeled a **triage heuristic**, not a validated scientific model.

### Learned stage
Candidate models:
- regularized logistic / survival models;
- gradient-boosted ranking;
- survival ranking;
- calibrated ensemble.

Deep models are optional and require evidence of benefit beyond interpretable baselines.

## 8. Benchmark labels

Avoid a single threshold definition.

Recommended outputs:

1. continuous future citation acceleration;
2. future field/age-normalized citation percentile;
3. future Beauty Coefficient / delayed-recognition rank after sufficient follow-up;
4. binary "awakens within H years" label under multiple prespecified definitions;
5. time-to-awakening for survival analysis.

All labels are computed **after** the historical cutoff and are inaccessible to the model.

## 9. Leakage firewall

Forbidden in prospective features when occurring after cutoff T:

- future citations;
- later retractions / corrections / expressions of concern;
- later prizes or awards;
- later review articles naming the paper as foundational;
- later patent citations;
- later journal metadata changes;
- later author fame / career outcomes;
- embeddings trained on future-only corpus states unless explicitly reconstructed and audited.

## 10. Bias / fairness audit

Measure shortlist yield and errors by:

- field;
- publication cohort;
- paper age;
- document type;
- language / indexing coverage;
- open-access availability;
- geographic and institutional strata **for audit only**, not as merit features.

A model that mainly reconstructs visibility or prestige should fail review.

## 11. Integration endpoints

### To 005
Export:
- candidate paper ID;
- cutoff;
- priority / probability;
- evidence vector;
- uncertainty;
- integrity gate;
- counterfactual-use warning.

### From 011
Import:
- timestamped integrity / provenance findings;
- citation-verification findings;
- metadata/post-publication state;
- applicability / ABSTAIN status.

## 12. Definition of done for v1

v1 requires:

- reproducible retrospective B implementation;
- historical-cutoff dataset;
- at least one large open-data source;
- deterministic baselines;
- prospective backtest;
- calibration / ranking metrics;
- 011 integration;
- evidence-card generation;
- feature-family ablations;
- documented failure cases;
- no known post-cutoff leakage in the final benchmark.
