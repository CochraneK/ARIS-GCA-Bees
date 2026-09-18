# ARIS4C009 · Novelty and failure-mode audit

## Proposed novelty

The broad idea of combining phenomenology and computation is **not novel**.

Existing work already includes:

- computational phenomenology;
- neurophenomenology;
- spatiotemporal psychopathology;
- EASE/EAWE/STEP quantification;
- computational psychiatry;
- digital phenotyping;
- idiographic dynamical modeling.

ARIS4C009 should therefore **not** claim to invent the bridge.

The candidate novelty is narrower and testable:

> Treat representational compression itself as an empirical variable and benchmark psychiatric representations by how much source-grounded phenomenological structure they destroy under a given burden, while keeping fidelity separate from prediction, biological concordance and reliability.

A literature search found uses of rate-distortion theory in cognition and some older theoretical psychiatry, but no clear mature framework matching this exact source-to-representation benchmark. This remains a provisional novelty claim until a formal systematic novelty search is completed.

## Why this is stronger than “digital twin” language

A digital-twin framing can overclaim that the latent model is the patient.

The fidelity-frontier framing instead asks:

- what was observed?
- what was retained?
- what was discarded?
- how uncertain is the translation?
- what additional predictions does the compressed form enable?
- can every inference be traced back to source evidence?

This is scientifically narrower and easier to falsify.

## Major failure modes

### FM1 · Mistaking the richest record for reality

The interview archive is not the experience itself.

Mitigation: call it the source evidence layer, never ground truth mental state.

### FM2 · Circular fidelity metric

If the same ontology generates both the representation and the fidelity questions, the richer representation wins by construction.

Mitigation:

- preregister query banks independently;
- include participant-generated queries;
- use multiple ontologies / raters;
- include domain-general factual and relational questions;
- run adversarial audits for ontology favoritism.

### FM3 · “More text is always better”

A long transcript may win merely because it contains everything.

Mitigation: explicitly model burden and representation rate; compare Pareto efficiency rather than raw fidelity alone.

### FM4 · Rater leakage

Experts who know EASE may ask EASE-shaped questions and favor EASE.

Mitigation: blinded evaluator panels, mixed theoretical backgrounds, participant validation, and independent query construction.

### FM5 · LLM semantic circularity

If an LLM creates the representation and another similar LLM grades it, apparent fidelity may reflect shared model biases.

Mitigation: human primary endpoint; model-family separation; repeated stochastic runs; source-grounded adjudication.

### FM6 · Reification of computational parameters

“Prior precision” can become a new label rather than an explanation.

Mitigation: require discriminating predictions and model comparison; parameter recovery; no one-to-one mapping from a symptom to a parameter by assumption.

### FM7 · Biological reductionism

Neural correspondence may be treated as proof that one phenomenological interpretation is true.

Mitigation: neural data are an independent constraint, not semantic adjudicator.

### FM8 · Cross-cultural collapse

Translations may erase experiential distinctions.

Mitigation: preserve original language, translation provenance and uncertainty; test site/language interactions.

### FM9 · Ethics of total capture

The ideal of “maximum reality” can encourage invasive surveillance.

Mitigation: fidelity is optimized subject to privacy and burden constraints. More data is not automatically better.

### FM10 · Unfalsifiable grand theory

A framework spanning phenomenology, computation, biology and environment can explain everything after the fact.

Mitigation: Paper 009A has a narrow benchmark with explicit primary outcomes and failure thresholds before mechanistic expansion.

## Strong competing explanations

The study should be designed so these can win:

1. **Simple-scale sufficiency:** conventional scales preserve nearly all clinically useful information.
2. **Prediction-first sufficiency:** lost phenomenological detail does not improve any external or future outcome.
3. **Narrative redundancy:** richer interviews mainly add stylistic or verbal redundancy.
4. **Expert artifact:** apparent phenomenological structure depends on specialist interviewing culture rather than reproducible patient-level phenomena.
5. **Dynamic-only account:** temporal density, not phenomenological ontology, explains the added value.
6. **General latent-factor account:** a small number of dimensions preserve nearly all meaningful variance once measurement error is handled correctly.

ARIS4C009 becomes scientifically valuable even if one of these alternatives wins, because the benchmark quantifies where detail is and is not necessary.
