# ARIS4C010 · Benchmark v0 specification

## Benchmark name

Working name: **UCID — Universal Concept Identification Dataset / benchmark**

"Universal" means **coverage-oriented and boundary-explicit**, not literally containing every possible concept.

## Unit of analysis

A benchmark record is not just a word.

```text
target_id
surface_form(s)
target_level
sense_or_definition
frozen_context
ontology_axis_labels
composition_expression
existence_status
grounding_mode
epistemic_status
source/provenance
candidate_questions[]
responses[]
response_distribution / agreement
notes
```

A target must have an identity criterion independent of the question-answer path.

## Target strata

### S1 concrete ordinary
Concrete objects, organisms, artifacts, substances.

### S2 events/processes/states
Actions, events, processes, temporal states.

### S3 properties/relations/roles
Colors, dispositions, social and spatial relations, institutional roles.

### S4 abstract/formal
Numbers, sets, mathematical/logical structures, theories, algorithms.

### S5 mental/social/normative
Emotion, belief, institution, right, obligation, rule, social status.

### S6 fictional/hypothetical
Fictional individuals/kinds and explicitly stipulated thought-experiment entities.

### S7 lexical ambiguity
Same surface string, different senses; synonymous forms for one sense.

### S8 compositional
Negation, conjunction, disjunction, quantified, relational, modal, temporal, counterfactual and higher-order targets.

### S9 vague/contextual
Sorites-prone predicates, indexicals, comparison-class dependence, discourse/context dependence.

### S10 semantic stress
Empty descriptions, impossible descriptions, presupposition failures, self-reference, paradox patterns, unknowns, undecidable cases, weak-ineffability/ostension cases.

### S11 open-world held-out
Valid targets absent from the active candidate ontology.

## Sampling

Initial v0 target: **240–400 concepts**, balanced enough for engineering but deliberately not publication-final.

Suggested first pass:
- 30 each from S1–S6 = 180;
- 30 ambiguity/compositional = 60;
- 30 vague/contextual = 30;
- 30 stress/open-world = 30;
- total ≈300.

Within ordinary strata, balance familiarity/frequency so semantic pathology is not confounded with rare vocabulary.

## Query bank

Questions are typed.

### Q-kind
- ontological kind;
- taxonomic membership;
- physical/functional property;
- temporal/event property;
- relational;
- logical/compositional;
- existence/modal;
- contextual;
- lexical/metalinguistic;
- grounding/perceptual;
- epistemic/computability;
- direct identity guess.

### Query admissibility labels
For every target/query pair:
- applicable;
- type error;
- requires missing context;
- answerable but uncertain;
- benchmark-excluded for leakage/triviality.

Questions that literally contain a unique target string or synonym need a separate "direct guess" cost regime.

## Response protocols

### P2
YES / NO only.

### P6
YES / NO / BORDERLINE / UNKNOWN / UNDEFINED / BOTH.

### P6+context
Before returning UNDEFINED for context-sensitive questions, the oracle may request one typed context variable. The context request consumes configurable cost.

## Baselines

### Representation baselines
- flat candidate list;
- single is-a taxonomy;
- WordNet-like lexical relation graph;
- UCID multi-axis typed graph;
- dense semantic embeddings;
- hybrid graph + embeddings;
- unrestricted arbitrary partition oracle.

### Query-policy baselines
- random;
- fixed generic hierarchy;
- frequency-weighted hierarchy;
- greedy entropy reduction;
- generalized binary search;
- cost-sensitive greedy;
- planning/MCTS;
- exact optimal tree for small subsets.

## Primary metrics

1. success@budget;
2. mean / median / p90 questions to exact target;
3. expected and worst-case tree depth on small exact subsets;
4. entropy-normalized efficiency;
5. Semantic Query Overhead;
6. pairwise separation coverage;
7. response-signature collision classes;
8. oracle contradiction/retest rate;
9. invalid/type-error question rate;
10. OOS detection precision/recall/calibration;
11. human–model response agreement by semantic stratum.

## Critical ablations

- remove representation-level axis;
- remove logical operators;
- remove context variables;
- force P6 responses into binary;
- replace multi-axis graph with single taxonomy;
- remove open-world state;
- remove lexical-frequency prior;
- no human calibration;
- LLM-only answer matrix versus human-calibrated matrix.

## Leakage controls

- split by concept family / ontology neighborhood, not random aliases;
- keep synonyms and near-synonyms in the same split where possible;
- compositional targets should hold out operator–base combinations, not just strings;
- direct target guesses are scored separately;
- question generation model should not see held-out target labels during policy evaluation unless the experimental condition explicitly permits it.

## Stress-test examples

Examples are diagnostic templates, not a final gold set.

- "not a mammal" — complement requires an explicit universe;
- "cat or dog" — disjunction;
- "tall" — comparison-class/vagueness;
- "here" — indexical/context;
- "the current king of France" — empty description under current context;
- "unicorn" — fictional/possibly conceivable nonactual kind;
- "round square" — inconsistent/impossible description;
- "bank" — surface-form ambiguity;
- "this sentence is false" — liar-like self-reference;
- a specified program-halting proposition — computability stress;
- an unfamiliar odor quality identifiable only by exemplar — weak linguistic ineffability / grounding.

## Publication gate

Benchmark v0 is exploratory. Promotion to publication-grade data requires:

- documented source/license for every imported target/resource;
- adjudication rules;
- human calibration sample size justified in advance;
- inter-rater reliability/distribution reporting;
- preregistered primary metrics and representation comparisons;
- test-set freeze with hashes;
- no hidden LLM-generated "gold" labels presented as objective semantic truth.
