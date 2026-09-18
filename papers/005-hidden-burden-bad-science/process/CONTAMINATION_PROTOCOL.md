# CONTAMINATION PROTOCOL — ARIS4C005

## Purpose

Measure how a source work with a documented serious reliability problem propagates through the scholarly evidence ecosystem **without equating citation with contamination**.

The propagation program has three nested levels:

1. **Citation exposure** — a downstream work cites the source.
2. **Material dependence** — the downstream work substantively relies on the source's data, result, method, or claim.
3. **Conclusion-changing impact** — removing/correcting the source changes a pooled estimate, significance, direction, recommendation, or other material conclusion.

Every reported quantity must identify which level it measures.

---

## Edge ontology

Each source → downstream citation edge receives one primary semantic class.

### `BACKGROUND_MENTION`

The source is cited for general context/history and the downstream argument does not materially require the disputed source claim.

Default contamination weight: 0.

### `METHOD_REUSE`

A method, instrument, algorithm, protocol, dataset construction rule, or other operational element is reused.

This is not automatically harmful. A separate field records whether the reused component is itself implicated by the source problem.

Default contamination weight: unresolved until component materiality is assessed.

### `RESULT_DEPENDENCE`

The downstream work uses the source's empirical result/estimate/claim as supporting evidence, a premise, comparator, parameter, training/evaluation datum, or factual input.

Default contamination weight: 1 for material-dependence counts after adjudication.

### `EVIDENCE_SYNTHESIS_INCLUDE`

The source contributes data/results to a systematic review, meta-analysis, evidence synthesis, pooled model, guideline evidence table, or analogous aggregate.

Default contamination weight: 1.

### `CRITIQUE_OR_CORRECTION`

The source is cited to criticize, correct, retract, reproduce-fail, or discuss the integrity problem.

Default contamination weight: 0; this is corrective propagation, not contamination.

### `CITATION_ONLY_OR_PERIPHERAL`

Citation is bibliographic/peripheral and no material downstream dependence is established.

Default contamination weight: 0.

### `INDETERMINATE`

Context is inaccessible or insufficient.

Never silently recode as non-contaminated.

---

## Separate edge fields

Each edge also records:

- `component_implicated`: YES / NO / UNKNOWN
- `material_to_downstream_claim`: YES / NO / UNKNOWN
- `citation_after_retraction`: YES / NO / UNKNOWN
- `source_retraction_known_in_text`: YES / NO / UNKNOWN
- `downstream_work_type`
- `context_access`: FULLTEXT / ABSTRACT_ONLY / NO_CONTEXT
- `review_confidence`: HIGH / MEDIUM / LOW

A citation after retraction is not automatically misconduct by the citing authors and not automatically contamination.

---

## Three-stage propagation estimands

### P1 — Citation Exposure Footprint (CEF)

Count unique downstream works that cite a source, by time since source publication/retraction.

This is bibliographic exposure only.

### P2 — Scientific Contamination Footprint (SCF)

Count unique downstream works with adjudicated material dependence:

- `RESULT_DEPENDENCE`, or
- `EVIDENCE_SYNTHESIS_INCLUDE`,
- and `material_to_downstream_claim=YES`.

SCF is reported by edge type and generation.

### P3 — Conclusion-Changing Impact (CCI)

For recalculable evidence syntheses:

- remove/correct implicated source;
- re-estimate downstream result;
- compare direction, significance, magnitude and recommendation status.

This follows the logic of VITALITY rather than treating inclusion alone as proof that the conclusion changed.

---

## Knowledge Ghost Half-Life

Two distinct quantities must never be conflated.

### Citation Ghost Half-Life

Time after retraction for **raw citation exposure rate** to fall to 50% of a pre-specified baseline/peak.

This can be estimated from bibliographic data.

### Dependence Ghost Half-Life

Time after retraction for **material-dependence edge rate** to fall to 50%.

This requires semantic edge adjudication.

The paper should prefer the second when enough data exist; the first remains a descriptive precursor.

---

## Pilot source selection

The first engineering pilot intentionally stress-tests high-propagation cases:

- source papers must be in the narrow E1-S screen;
- source must resolve to an OpenAlex work;
- select a fixed number with high `cited_by_count`;
- source-selection rule is stored in provenance;
- no global prevalence or average contamination claim may be made from this high-citation pilot.

Later confirmatory propagation uses probability sampling / stratification over adjudicated source works.

---

## Citation graph limitations

OpenAlex citation links depend on successfully matching references to known works. Reference lists may be missing or incomplete.

Therefore CEF is a database-observed lower-bound graph, not a complete scholarly citation graph.

---

## Semantic adjudication

Reviewer packet must hide any model-predicted semantic class where possible.

At minimum, double-code:

- all `RESULT_DEPENDENCE`;
- all `EVIDENCE_SYNTHESIS_INCLUDE`;
- all disagreements;
- a random subset of background/critique edges.

If an automated/LLM classifier is later used, it is a screening/classification model calibrated against human edge labels. It is not the gold standard.

---

## Generation rules

- generation 0: problematic/adjudicated source;
- generation 1: direct downstream material dependents;
- generation 2+: works materially dependent on prior contaminated nodes.

A generation-2 edge is not contaminated merely because it cites a contaminated generation-1 work. Material semantic dependence must again be established.

---

## No-go rules

Do not:

- count every citation as contamination;
- count critique/correction citations as harm;
- infer that a citing author knew of a problem from timing alone;
- infer misconduct by citing authors;
- use citation volume alone as societal impact;
- merge raw exposure, material dependence and conclusion-changing impact into one count;
- use high-citation pilot sources to infer a global average.
