# Beyond Twenty Questions: Semantic Limits and Query Complexity of Universal Concept Identification

**Pre-results manuscript scaffold**  
**ARIS4C010**  
**Author:** Cochrane Kang

> This document is intentionally pre-results. Pilot 0–2 evidence is labeled exploratory; confirmatory claims are withheld until human calibration and Benchmark v0 are frozen.

## Abstract

Twenty Questions provides a simple information-theoretic picture of identification: with unrestricted noiseless binary partitions, a finite set of (N) equiprobable targets can be separated in roughly (log_2 N) questions. Human semantic questioning is more constrained. Questions must be interpretable, applicable to the target type, answerable under a specified context and oracle, and robust to lexical ambiguity, vagueness, nonexistence, contradiction, epistemic uncertainty, and open-world targets. We formalize **semantic concept identification** as adaptive search over an explicit target universe under an admissible semantic query family, and define **Semantic Query Overhead** as the additional identification cost relative to unrestricted partitions. We distinguish static separating bases from adaptive decision trees, connect the former to Test Cover, and specify a typed multi-axis representation that does not assume all concepts form one inheritance tree. An exploratory source-derived pilot using 15 Open English WordNet senses finds measurable but small expected semantic overhead under an uncalibrated query matrix. The confirmatory program will calibrate binary versus richer semantic response protocols in humans and evaluate single-taxonomy, graph, multi-axis, embedding, and hybrid representations across ordinary and adversarial concept regimes.

## 1. Introduction

The classic Twenty Questions game hides a target and permits a sequence of binary questions. If arbitrary partitions of a finite candidate set are allowed, identification is fundamentally a coding problem. Real semantic interaction is different: one cannot usually ask an arbitrary subset-membership question such as “Is your concept one of items 1, 4, 7, 13, …?” and still regard the query as a natural conceptual question.

This gap motivates the central question:

> **What additional query cost is imposed when identification questions must be semantically admissible?**

The problem is not equivalent to building a complete taxonomy of everything. Exact identification requires a query family capable of separating candidate targets relative to an explicit universe. A single `is-a` tree may be useful for ordinary object categories, but lexical senses, relations, negation, context-sensitive predicates, fictional or empty descriptions, higher-order constructions, and semantic pathologies cross-cut taxonomic inheritance.

We therefore treat universal concept identification as a **relative** problem: relative to a target universe, query language, response protocol, context model, and oracle.

## 2. Formal framework

Let (C) denote targets, (Q) admissible queries, (R) response states, and (A(c,q,x)) the oracle response under context (x).

For finite (C), exact identification is possible only if every target pair is separated by at least one admissible query.

For unrestricted (r)-ary responses and maximum depth (b), at most (r^b) leaves can be distinguished. Hence an infinite candidate universe cannot admit a uniform finite worst-case budget under a finite response alphabet.

### 2.1 Static separation versus adaptive identification

A static query basis seeks the smallest subset of questions whose joint signatures uniquely identify all candidates. In the deterministic binary case this maps to Test Cover.

An adaptive policy chooses the next query from previous responses. The minimum static basis and the shallowest/lowest-cost adaptive decision tree are distinct optimization objects.

### 2.2 Semantic Query Overhead

Let (L^*_{all}) be optimal expected cost under unrestricted partitions and (L^*_{sem}) optimal expected cost under the semantic query family:

[
Delta_{sem}=L^*_{sem}-L^*_{all}.
]

For unit-cost binary unrestricted questions, the expected optimum is represented by the Huffman-optimal prefix-code length under the target prior.

## 3. Semantic representation

UCID uses a typed factorization rather than claiming a metaphysically final tree. Dimensions include:

1. target/representation level;
2. ontological kind;
3. logical/compositional form;
4. referential/modal status;
5. boundary/gradedness;
6. context dependence;
7. grounding/access mode;
8. epistemic/computability status;
9. reflexivity/pathology;
10. lexicalization/expressibility.

The empirical claim is not that these axes are uniquely correct, but that explicitly cross-cutting semantic structure may improve separation and query validity relative to simpler baselines.

## 4. Response protocols

The strict protocol P2 provides YES/NO only.

P6 distinguishes:
YES, NO, BORDERLINE, UNKNOWN, UNDEFINED, and BOTH.

A P6+context extension additionally permits CONTEXT_REQUEST.

The richer alphabet has greater potential information capacity, but may also impose cognitive and reliability costs. Its value is therefore empirical rather than assumed.

## 5. Prior-art boundary

The project builds on mature work in exact query learning, generalized binary search, Test Cover and separating systems, teaching dimension, referring-expression generation, description-logic concept learning, ontology inseparability, pragmatic reference games, active feature acquisition, clarification questions, lexical ontologies, formal concept analysis, vagueness, non-classical logic, and open-world recognition.

The contribution is not any one optimization method or ontology. The candidate contribution is their integration into a benchmark that explicitly measures semantic admissibility cost across heterogeneous concept regimes and identification failure modes.

## 6. Methods

### 6.1 Evidence ladder

Pilot 0 validates the combinatorial implementation on synthetic binary matrices.

Pilot 1 tests a constructed heterogeneous semantic seed and demonstrates how a coarse taxonomy projection can create response-signature collisions.

Pilot 2 introduces source-derived Open English WordNet senses and separates source-native metadata from unreviewed UCID semantic mappings.

### 6.2 Lexical Calibration60

The first human source pool uses pinned Open English WordNet 2025 via `wn==1.1.1`.

Ten polysemous lemmas contribute six noun senses each:

bank, spring, head, line, point, light, field, board, foot, and case.

All senses sharing a lemma remain one leakage group.

A fixed 24-question generic semantic bank is independent of individual target glosses. A balanced subset yields 720 target-query pairs for initial calibration.

### 6.3 Mixed response-state calibration

A separate constructed packet contains 24 scenarios designed to expose distinctions among borderline application, epistemic uncertainty, missing context, empty reference, inconsistency, stochasticity, undecidability, and oracle-access limitations.

No response is predeclared as gold.

### 6.4 Human form design

Thirty-six balanced base forms are duplicated across P2 and P6.

Each form contains 84 unique main trials and 8 covert retests. One full form cycle provides equalized pair exposure but is not itself a powered sample-size recommendation.

## 7. Exploratory engineering results

### 7.1 Pilot 2

Fifteen source-derived OEWN noun senses were examined: nine senses of `bank` and six of `spring`.

OEWN `lexname` categories alone left five response-signature collision groups, corresponding to pairwise separation coverage of 0.9143.

An exploratory 18-query semantic bank separated all 15 targets. The exact minimum static separating subset contained 12 questions.

Under a uniform prior:

- unrestricted Huffman-optimal expected binary cost: 3.9333;
- exact semantic expected cost: 4.2667;
- exploratory expected Semantic Query Overhead: +0.3333 questions;
- unrestricted worst-case lower bound: 4;
- exact semantic worst-case cost: 6;
- exploratory worst-case overhead: +2.

These values are not confirmatory because the semantic response matrix is machine-mapped and uncalibrated.

## 8. Confirmatory analyses — reserved

This section will report only frozen Benchmark v0 and human-calibrated results.

Primary outcomes:
- pairwise separation coverage;
- collision class structure;
- expected and worst-case semantic query cost;
- Semantic Query Overhead;
- invalid/type-error question rate;
- P2/P6 response reliability and retest consistency;
- open-world calibration.

## 9. Discussion — precommitted interpretation boundaries

A positive result would not establish a final ontology of human thought. It would show that specified semantic structure improves identifiability under a stated query protocol.

A null result in which simpler lexical graphs or embeddings match the multi-axis ontology would narrow the contribution and be reported directly.

If P6 categories cannot be used reproducibly, the response protocol should be simplified rather than preserved for theoretical elegance.

Strong ineffability remains a boundary of ordinary target representation rather than an empirically instantiated row in the benchmark.

## Data and code availability

All current design, source locks, schemas, pilots, CI workflows, and calibration builders are versioned under `papers/010-universal-concept-identification/` in ARIS4C.
