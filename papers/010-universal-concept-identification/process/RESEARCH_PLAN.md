# ARIS4C010 · Research Plan

## 1. Research objective

Build and test a formal framework for **semantic concept identification under finite query budgets**.

The project has two complementary goals:

1. prove clean identifiability and lower-bound statements that separate finite, infinite, closed-world and open-world regimes;
2. empirically measure how much efficiency is lost when arbitrary mathematical partitions are replaced by human-meaningful semantic questions.

## 2. Formal model

Let:

- (C): candidate concepts;
- (p(c)): prior over candidates;
- (Q): admissible questions;
- (R): answer alphabet;
- (A(c,q,x)): oracle response for concept (c), query (q), and frozen context (x);
- (\pi): adaptive policy selecting the next query from history.

### 2.1 Uniform finite-budget impossibility

Any decision tree of depth (b) with at most (r=|R|) answer branches per question has at most (r^b) leaves.

Therefore a fixed (b) cannot uniquely identify more than (r^b) targets. With infinitely many candidate concepts, no uniform finite worst-case bound exists under a finite response alphabet.

### 2.2 Separability

For finite (C), the complete admissible family (Q) supports exact identification iff every pair of candidates is separated by at least one query.

### 2.3 Static versus adaptive optimization

**Static basis problem:** choose the smallest (Q'\subseteq Q) whose joint signatures uniquely identify every candidate. For binary questions this maps directly to Test Cover.

**Adaptive policy problem:** choose questions conditional on previous responses to minimize expected or worst-case total cost.

Both matter: a small universal feature basis and a shallow adaptive decision tree are not the same optimization problem.

## 3. Core metrics

### Information lower bound

For binary noiseless answers and finite (C):

[
L_{LB}=H(C)
]

in expected bit units, with worst-case lower bound (\lceil\log_2 |C|\rceil) under a uniform prior.

### Semantic Query Overhead

[
\Delta_{sem}=E[L^*_{sem}]-E[L^*_{all}]
]

where (Q_{sem}) contains only admissible human-interpretable questions and (Q_{all}) permits arbitrary partitions.

### Semantic efficiency

[
\eta_{sem}=\frac{H(C)}{E[L_{sem}]}
]

for binary unit-cost queries. Report separately for richer response alphabets because one response can encode more than one bit.

### Separation coverage

[
Sep(Q)=\frac{\#\{(i,j):\exists q\in Q, A(c_i,q)\neq A(c_j,q)\}}{\binom{|C|}{2}}.
]

### Collision structure

Count unresolved response-signature equivalence classes, their sizes, and which ontology strata produce them.

### Oracle consistency

For human or model oracles, measure repeated-answer agreement, inter-rater agreement, and contradiction rate by concept/query type.

## 4. Benchmark ladder

### B0 · combinatorial sanity
Synthetic deterministic response matrices. Verify lower bounds, exact decision-tree search, test-cover calculations and collision detection. No semantic claims.

### B1 · concrete-object bridge
Reuse or reconstruct an open object-focused Twenty Questions setting to reproduce established adaptive-query results. The ICML 2025 dataset is a natural comparison target if licensing/access permits.

### B2 · lexical sense
Sample WordNet/BabelNet-style senses rather than strings. Include deliberately ambiguous lemmas so success requires identifying the intended sense.

### B3 · cross-ontological ordinary concepts
Stratified sample across:
- objects/agents/substances;
- events/processes/states;
- properties/relations/roles;
- abstract/formal entities;
- information objects;
- mental/phenomenal concepts;
- social/normative concepts;
- fictional concepts.

### B4 · compositional closure
Generate auditable targets using verified operators:
- negation;
- conjunction/disjunction;
- relational descriptions;
- quantification;
- comparison;
- modality;
- temporal operators;
- counterfactuals;
- higher-order constructions.

### B5 · semantic stress suite
Curated cases:
- empty current reference;
- possible but nonactual;
- fictional;
- impossible/inconsistent;
- vague/sorites-prone;
- indexical/context-dependent;
- homonymous/polysemous;
- presupposition failure;
- self-reference;
- liar-like paradox;
- empirical unknown;
- undecidable problem instance/class;
- weak ineffability / ostensive grounding;
- strong-ineffability boundary statement.

### B6 · open-world test
Withhold a set of legitimate targets from the ontology/question bank. Compare:
- forced closed-world guessing;
- OUT-OF-SUPPORT detection;
- ontology expansion/recovery.

## 5. Competing representations

At minimum compare:

1. **single taxonomy tree** — is-a only;
2. **multi-axis typed ontology** — the design in CONCEPT_ONTOLOGY.md;
3. **lexical-semantic graph** — relations beyond is-a;
4. **dense embedding baseline** — similarity without explicit semantic operators;
5. **hybrid symbolic + embedding**;
6. **unrestricted oracle partitions** — unattainable semantic upper bound / information baseline.

The question is not whether one representation is aesthetically better. It is which supports separation, calibration and efficient querying on held-out targets.

## 6. Query policies

Compare:

- random admissible query;
- fixed handcrafted hierarchy;
- greedy expected information gain;
- generalized-binary-search style split;
- cost-sensitive information gain;
- MCTS/planning where computationally feasible;
- LLM-generated questions with semantic validation;
- oracle optimal decision tree for small benchmark subsets.

A generic cost-sensitive utility is

[
U(q|h)=\frac{I(C;A_q\mid h)}{cost(q)}
]

augmented in semantic experiments with penalties for low answerability, ambiguity or context dependence.

## 7. Human and model oracle design

Generated answer matrices are **not ground truth by default**.

For each semantic stratum:

1. draft candidate questions;
2. validate type correctness;
3. obtain repeated judgments from multiple human raters for a calibration subset;
4. compare humans, lexical resources and multiple LLMs;
5. store disagreement distributions rather than forcing binary labels prematurely;
6. only then freeze benchmark answers or probabilistic response models.

Particularly sensitive strata: vague properties, social/normative concepts, phenomenology, counterfactuals, paradox.

## 8. Main falsification tests

### H1 single-tree insufficiency
Reject if a single taxonomy at matched complexity equals or exceeds the multi-axis representation on held-out separation and semantic query cost across ordinary + stress strata.

### H2 semantic overhead
Reject if semantically admissible queries achieve unrestricted-optimum cost within uncertainty across representative strata.

### H3 pathology-specific overhead
Reject if vague/contextual/compositional/pathological strata do not show systematic additional collision/answer inconsistency/query cost after matching frequency and familiarity.

### H4 enriched response protocol
The claim is not "more labels always win." Test whether P6 lowers contradiction/invalid-answer rates and total interaction cost after accounting for answer-channel information capacity.

### H5 open-world advantage
Reject if OUT-OF-SUPPORT handling does not improve calibration/error under held-out targets.

## 9. Statistical analysis

- bootstrap confidence intervals for expected query counts and overhead;
- hierarchical models with concepts and questions as crossed effects;
- difficulty predictors: ontology stratum, frequency/familiarity, lexicality, context dependence, vagueness, compositional depth;
- pairwise collision analyses;
- calibration curves for posterior target probabilities;
- matched comparisons controlling candidate-set size and prior entropy;
- sensitivity to answer alphabet and oracle noise.

Avoid treating each question path as an independent observation when paths share the same target/question bank.

## 10. Computational work packages

### WP0 formal + code core
Decision-tree solver, information metrics, collision analysis, minimum separating-set solver for small instances.

### WP1 resource harmonization
Map lexical resources and upper-ontology labels into the typed axes.

### WP2 Benchmark v0
Construct balanced ordinary + stress-suite target sample.

### WP3 oracle calibration
Human/model/resource response matrices and disagreement study.

### WP4 query experiments
Run policies and representation ablations.

### WP5 open-world + nonclassical stress
Withheld targets, context requests, vague/unknown/undefined/both states.

### WP6 manuscript
Separate theorem/proposition claims, benchmark evidence, and philosophical boundary arguments.

## 11. Claim boundaries

Do not claim:

- a complete ontology of all possible concepts;
- that every concept is lexicalizable;
- that one ontology is metaphysically correct;
- that LLM judgments establish semantic truth;
- that 20/21 questions can identify an open infinite universe in worst case;
- that paradox, uncertainty, vagueness and undecidability are the same phenomenon;
- that strong ineffability has been empirically represented.

The strongest legitimate end product would be:

> a formal theory and benchmark of **query-identifiability relative to an explicit concept universe, admissible semantic question family, response protocol, context model and oracle**.
